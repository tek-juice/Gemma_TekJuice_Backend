from ollama import chat

def generate_respponce(messaages, model="gemma4"):
    try:
        response = chat(model=model, messages=messaages)

        return response["message"]["content"]
    
    except Exception as e:
        return str(e)