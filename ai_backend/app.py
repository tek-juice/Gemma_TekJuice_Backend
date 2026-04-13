from flask import Flask
from routes.chat_routes import chat_bp
from flasgger import Swagger

app = Flask(__name__)

swagger = Swagger(app)

app.register_blueprint(chat_bp, url_prefix="/api/v1")

if __name__=="__main__":
    app.run(debug=True)