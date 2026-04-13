from flask import Blueprint, request, jsonify
from services.ollama_services import generate_respponce

chat_bp = Blueprint("chat", __name__)


@chat_bp.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    
    messages = data.get("messages", [])
    model = data.get("model", "gemma4")

    if not messages:
        return jsonify({"error": "Messages are required"}), 400
    
    response = generate_respponce(messages, model)

    return jsonify({
        "response": response
    })