from ollama import chat
from flask import Response, stream_with_context

def generate_stream(messages, model="gemma4"):
    stream = chat(model=model, messages=messages, stream=True)

    for chunk in stream:
        content = chunk["message"]["content"]
        yield content