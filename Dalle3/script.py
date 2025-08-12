import os 
from dotenv import load_dotenv
from openai import OpenAI
import json

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_image(prompt: str, quality: str = "standard") -> str:
    try:
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            quality=quality,
            n=1
        )
        return response.data[0].url
    except Exception as e:
        print(f"Error generating image: {e}")
        return ""
    
prompt = "Un gato viendo el atardecer"
quality = "standard"

print(generate_image(prompt, quality))