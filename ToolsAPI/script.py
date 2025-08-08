import os 
from dotenv import load_dotenv
from openai import OpenAI
import requests
import json

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_weather(latitude: float, longitude: float) -> str:
    print("Getting weather...")
    url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current_weather=true"
    response = requests.get(url)
    weather_data = response.json()

    return json.dumps(weather_data)

messages = [
    {
        "role": "system", 
        "content": "Eres un asistente que entrega datos sobre el clima del mundo en tiempo real"
    },
    {
        "role": "user",
        "content": "Cual es el clima en Tulsa, Oklahoma?"
    }
        
]

functions = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Usa esta funcion para obtener información sobre el clima",
            "parameters": {
                "type": "object",
                "properties": {
                    "latitude": {
                        "type": "number",
                        "description": "Latitud de la ubicación"
                    },
                    "longitude": {
                        "type": "number",
                        "description": "Longitud de la ubicación"
                    }
                },
                "required": ["latitude", "longitude"]
            },
            "output": {
                "type": "string",
                "description": "Clima de la ubicación pedida por el usuario"
            }
        }
    }
]

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=messages,
    tools=functions,
    temperature=0.7
)

assistant_message = response.choices[0].message
print("---------------")
print(assistant_message.content)


# El siguiente bloque es necesario porque maneja la llamada a la función sugerida por el modelo.
# Cuando el modelo detecta que debe usar una función (en este caso, get_weather), retorna una "tool_call".
# Aquí se ejecuta realmente la función get_weather con los argumentos proporcionados por el modelo,
# y luego se agrega la respuesta al historial de mensajes para que el modelo pueda generar una respuesta en texto natural.
# Sin este paso, el modelo no tendría acceso a los datos reales del clima y no podría responder correctamente al usuario.
if assistant_message.tool_calls:
    for tool_call in assistant_message.tool_calls:
        if tool_call.type == "function":
            function_name = tool_call.function.name
            function_args = json.loads(tool_call.function.arguments)
           
            if function_name == "get_weather":
                print(f"Llamada a la funcion: {function_name} con argumentos: {function_args}")
                weather_data = get_weather(
                    latitude=function_args.get("latitude"),
                    longitude=function_args.get("longitude")
                )

                messages.append(assistant_message)
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": function_name,
                    "content": weather_data
                })

second_response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=messages,
)

final_response = second_response.choices[0].message.content

print("---------------")
print(final_response)