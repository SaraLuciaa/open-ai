from flask import Flask, request, jsonify
from dotenv import load_dotenv
from openai import OpenAI
import os

load_dotenv()

app = Flask(__name__)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get('message', '')
    if not user_message:
        return jsonify({'error': 'No message provided'}), 400
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Eres un asistente de chat llamado Baymax."},
            {"role": "user", "content": user_message}
        ],
        max_tokens=100,
        temperature=0.7
    )
    return jsonify({'response': response.choices[0].message.content})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 