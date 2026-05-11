from flask import Flask
from routes.chat_routes import chat_bp
from routes.admin_route import admin_bp
from routes.user_route import user_bp
from routes.user_show import usershow_bp
from routes.apikey import api_key_create_bp
# from routes.auth_chat_route import chat_secure_bp
from routes.get_api_key import api_key_fetch_bp
from flasgger import Swagger
import os
from config.services.extensions import db
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate

from dotenv import load_dotenv
from config.services.extensions import mail
load_dotenv()


app = Flask(__name__)

CORS(app)

# Database 
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] =False
app.config["JWT_SECRET_KEY"] = "super-secret-key"

jwt = JWTManager(app)

db.init_app(app)

migrate = Migrate(app, db)

swagger = Swagger(app)

# Email code
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USE_SSL"] = False
app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")
app.config["MAIL_DEFAULT_SENDER"] = os.getenv("MAIL_USERNAME")
mail.init_app(app)

app.register_blueprint(chat_bp, url_prefix="/api/v1")
app.register_blueprint(admin_bp, url_prefix="/api/v1")
app.register_blueprint(user_bp, url_prefix="/api/v1")
app.register_blueprint(usershow_bp, url_prefix="/api/v1")
app.register_blueprint(api_key_create_bp, url_prefix="/api/v1")
# app.register_blueprint(chat_secure_bp, url_prefix="/api/v1")
app.register_blueprint(api_key_fetch_bp, url_prefix="/api/v1")


if __name__=="__main__":
    app.run(debug=True)