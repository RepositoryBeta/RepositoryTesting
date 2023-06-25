import openai
import os
from dotenv import load_dotenv
load_dotenv()

def evaluar(orden):
    openai.api_key = os.getenv("API_KEY")
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=orden,
        temperature=0.7,
        max_tokens=250,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        logprobs=5,
        stop=["###"]
    )
    respuesta = response.choices[0].text
    prob_tokens = response.choices[0].logprobs.top_logprobs
    return respuesta, response.usage.total_tokens

def chatGPT():
    openai.api_key = os.getenv("API_KEY")
    response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
            {"role": "user", "content": "Puedes darme un ejemplo de console.log() en javascripts"}
        ]
    )
    print(response.choices[0].message.content)

