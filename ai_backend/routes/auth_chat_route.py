from flask import Blueprint, request, jsonify, Response, stream_with_context
from models.apikey import ApiKey
from config.ollama_services import generate_stream

chat_secure_bp = Blueprint("chat_secure", __name__)

@chat_secure_bp.route("/chat/secure", methods=["POST"])
def chat_secure():
    """
Authenticated Chat with AI
---
tags:
  - Chat

parameters:
  - name: x-api-key
    in: header
    required: true
    type: string
    description: User API key

  - name: body
    in: body
    required: true
    schema:
      type: object
      required:
        - messages
      properties:
        model:
          type: string
          example: gemma3:1b
        messages:
          type: array
          items:
            type: object
            properties:
              role:
                type: string
                example: user
              content:
                type: string
                example: Hello AI

responses:
  200:
    description: AI response
  401:
    description: Unauthorized
"""
    api_key_value = request.headers.get("x-api-key")

    if not api_key_value:
        return {"error": "API key required"}, 401

    api_key = ApiKey.query.filter_by(
        key=api_key_value,
        is_active=True
    ).first()

    if not api_key:
        return {"error": "Invalid API key"}, 401

    user = api_key.user

    data = request.get_json() or {}

    messages = data.get("messages", [])
    model = data.get("model", "gemma3:1b")

    if not messages:
        return {"error": "Messages are required"}, 400

    # 3. STREAM FUNCTION
    def stream():
        try:
            for chunk in generate_stream(messages, model):
                yield chunk 
        except Exception as e:
            yield f"\n[ERROR]: {str(e)}"

    return Response(
        stream_with_context(stream()),
        content_type="text/plain"
    )