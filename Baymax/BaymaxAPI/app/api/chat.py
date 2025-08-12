from flask import request, jsonify, Response
import openai
import json
from openai import OpenAI

def chat():
    try: 
        data = request.json

        formatted_message = [
            {
                "role": "system",
                "content": "Eres un asistente llamado Baymax. Responde a las preguntas de los usuarios con claridad."
            }
        ]

        for message in data['messages']:
            if 'image_data' in message:
                # process the image
                content_parts = [{
                    "type": "text", 
                    "text": message['content']
                }]

                for image_data_base64 in message['image_data']:
                    content_parts.append({
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png, base64, {image_data_base64}"
                        }
                    })
                
                formatted_message.append({
                    "role": message['role'],
                    "content": content_parts
                })
            else:
                formatted_message.append({
                    "role" : message['role'],
                    "content": message['content']
                })

        client = OpenAI()

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=formatted_message,
            stream = True
        )

        def generate():
            for chunk in response:
                if chunk.choices[0].delta.content:
                    yield f"data: {json.dumps({'content': chunk.choices[0].delta.content, 'status': 'streaming'})}\n\n"

                if chunk.choices[0].finish_reason == "stop":
                    yield f"data: {json.dumps({'status': 'done'})}\n\n"
                    break
        
        return Response(generate(), mimetype='text/event-stream')
    except Exception as e:
        print(f"Chat request failed: {str(e)}")
        return jsonify({
            "error": str(e),
            "status" : "error"
        }), 500