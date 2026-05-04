from flask import Blueprint, request, Response, stream_with_context
from config.services.ollama_services import generate_stream

chat_bp = Blueprint("chat", __name__)

@chat_bp.route("/chat", methods=["POST"])
def chat():
    """
    Chat with Gemma 4
    ---
    tags:
      - Chat
    parameters:
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
              example: gemma4
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
        schema:
          type: object
          properties:
            response:
              type: string
              example: Hello! How can I help you?
      400:
        description: Bad request
    """
    data = request.get_json()

    messages = data.get("messages", [])
    model = data.get("model", "gemma4")

    if not messages:
        return {"error": "Messages are required"}, 400

    def stream():
        try:
            for chunk in generate_stream(messages, model):
                # Send chunk immediately to frontend
                yield chunk
        except Exception as e:
            yield f"\n[ERROR]: {str(e)}"

    return Response(
        stream_with_context(stream()),
        content_type="text/plain"
    )