from flask import Flask, render_template, request, jsonify, Response, stream_with_context
import requests
import json
import time

app = Flask(__name__)

# 🔑 API Anahtarınız (Güvenli saklayın!)
API_KEY = "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"
API_URL = "https://integrate.api.nvidia.com/v1/chat/completions"

# Model listesini yükle
with open("models.json", "r", encoding="utf-8") as f:
    MODELS = json.load(f)["modeller"]

@app.route("/")
def index():
    """Ana sayfa - tüm modelleri göster"""
    return render_template("index.html", models=MODELS)

@app.route("/api/chat", methods=["POST"])
def chat():
    """Sohbet API'si - seçilen model ile konuş"""
    data = request.json
    model_id = data.get("model")
    messages = data.get("messages", [])
    stream = data.get("stream", False)
    temperature = data.get("temperature", 0.7)
    max_tokens = data.get("max_tokens", 2048)

    if not model_id:
        return jsonify({"error": "Model seçilmedi"}), 400

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "messages": messages,
        "model": model_id,
        "max_tokens": max_tokens,
        "temperature": temperature,
        "top_p": 0.95,
        "stream": stream
    }

    # Akışlı yanıt (Streaming)
    if stream:
        def generate():
            response = requests.post(API_URL, headers=headers, json=payload, stream=True)
            for line in response.iter_lines():
                if line:
                    line = line.decode("utf-8")
                    if line.startswith("data:"):
                        yield f"data: {line[5:]}\n\n"
            yield "data: [DONE]\n\n"
        return Response(stream_with_context(generate()), mimetype="text/event-stream")
    
    # Normal yanıt
    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=60)
        if response.status_code == 200:
            return jsonify(response.json())
        else:
            return jsonify({"error": response.text}), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/models")
def get_models():
    """Tüm modelleri listele"""
    return jsonify({"models": MODELS})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)