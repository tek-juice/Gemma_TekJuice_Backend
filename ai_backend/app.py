from flask import Flask
from routes.chat_routes import chat_bp, admin_bp
from flasgger import Swagger
import os

load_dotenv()


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] =False

swagger = Swagger(app)

app.register_blueprint(chat_bp, url_prefix="/api/v1")
app.register_blueprint(admin_bp, url_prefix="/api/v1")

if __name__=="__main__":
    app.run(debug=True)