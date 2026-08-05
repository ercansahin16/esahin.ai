from flask import Flask, render_template, request, jsonify
import requests
import json

app = Flask(__name__)

# 🔑 API Anahtarınızı buraya yazın
API_KEY = "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"
API_URL = "https://integrate.api.nvidia.com/v1/chat/completions"

# Model listesi (direkt Python içinde)
MODELS = [
    {"id": "moonshotai/kimi-k2.6", "name": "Kimi K2.6", "aciklama": "1T multimodal MoE - Kodlama ve aracı işlemler", "ozellik": "Mükemmel kodlama, 262K bağlam"},
    {"id": "deepseek-ai/deepseek-v4-flash", "name": "DeepSeek V4 Flash", "aciklama": "284B MoE - Hızlı kodlama", "ozellik": "Hızlı yanıt, 1M bağlam"},
    {"id": "deepseek-ai/deepseek-v4-pro", "name": "DeepSeek V4 Pro", "aciklama": "MoE mimarili kodlama modeli", "ozellik": "1M bağlam, yüksek kalite"},
    {"id": "nvidia/nemotron-3-nano-omni-30b-a3b-reasoning", "name": "Nemotron 3 Nano Omni", "aciklama": "Görüntü/video/ses anlama + akıl yürütme", "ozellik": "Multimodal, reasoning"},
    {"id": "nvidia/nemotron-3-ultra-550b-a55b", "name": "Nemotron 3 Ultra", "aciklama": "1M bağlam, aracı akıl yürütme", "ozellik": "En güçlü NVIDIA modeli"},
    {"id": "mistralai/mistral-medium-3.5-128b", "name": "Mistral Medium 3.5", "aciklama": "Dengeli performans, kodlama", "ozellik": "Genel amaçlı"},
    {"id": "google/diffusiongemma-26b-a4b-it", "name": "Diffusion Gemma 26B", "aciklama": "Difüzyon tabanlı LLM", "ozellik": "Paralel token üretimi"},
    {"id": "z-ai/glm-5.2", "name": "GLM 5.2", "aciklama": "Aracı iş akışları ve kodlama", "ozellik": "Agentic AI"},
    {"id": "minimaxai/minimax-m3", "name": "MiniMax M3", "aciklama": "Multimodal MoE, kodlama", "ozellik": "Görüntü anlama"},
    {"id": "nvidia/nemotron-3-embed-1b", "name": "Nemotron 3 Embed 1B", "aciklama": "Embedding model - RAG ve arama", "ozellik": "Semantik arama"}
]

@app.route("/")
def index():
    return render_template("index.html", models=MODELS)

@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.json
    model_id = data.get("model")
    messages = data.get("messages", [])
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
        "top_p": 0.95
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=60)
        if response.status_code == 200:
            return jsonify(response.json())
        else:
            return jsonify({"error": f"API Hatası: {response.status_code} - {response.text}"}), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/models")
def get_models():
    return jsonify({"models": MODELS})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
