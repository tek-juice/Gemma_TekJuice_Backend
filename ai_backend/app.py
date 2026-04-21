from flask import Flask
from routes.chat_routes import chat_bp
from routes.admin_route import admin_bp
from routes.user_route import user_bp
from routes.user_show import usershow_bp
from routes.apikey import api_key_create_bp
from routes.auth_chat_route import chat_secure_bp
from flasgger import Swagger
import os
from config.services.extensions import db
from flask_cors import CORS

from dotenv import load_dotenv

load_dotenv()


app = Flask(__name__)

CORS(app)

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] =False

db.init_app(app)

swagger = Swagger(app)

app.register_blueprint(chat_bp, url_prefix="/api/v1")
app.register_blueprint(admin_bp, url_prefix="/api/v1")
app.register_blueprint(user_bp, url_prefix="/api/v1")
app.register_blueprint(usershow_bp, url_prefix="/api/v1")
app.register_blueprint(api_key_create_bp, url_prefix="/api/v1")
app.register_blueprint(chat_secure_bp, url_prefix="/api/v1")

with app.app_context():
    db.create_all()

if __name__=="__main__":
    app.run(debug=True)