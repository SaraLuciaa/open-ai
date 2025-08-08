from flask import Flask
from flask_cors import CORS
import openai
import os
from dotenv import load_dotenv
from app.api.chat import chat

def create_app():
    load_dotenv()
    app = Flask(__name__)
    CORS(app)
    app.add_url_rule('/api/chat', 'chat', chat, methods=['POST'])
    return app