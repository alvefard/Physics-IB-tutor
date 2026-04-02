import os
os.environ["OPENAI_API_KEY"] = "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"
from openai import OpenAI
import os

# Correcto: obtiene la variable de entorno
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def preguntar_chatgpt(mensaje_usuario, modelo="gpt-4o-mini"):
    response = client.chat.completions.create(
        model=modelo,
        messages=[
            {"role": "user", "content": mensaje_usuario}
        ]
    )
    return response.choices[0].message.content
