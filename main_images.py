"""
    - https://ai.google.dev/gemini-api?hl=pt-br
    - https://ai.google.dev/gemini-api/docs/get-started/tutorial?hl=pt-br&lang=python#generate_text_from_text_inputs

    Criar ambiente (Windows):
    python -m venv .venv

    Ativa ambiente virtual:
    venv\Script\activate

    Instalar dependencias:
    pip install -r requirements.txt
    
    Rodar script:
    python main_images.py
"""

import google.generativeai as genai

import PIL.Image
import os
import json
from dotenv import load_dotenv
import time

PATH_RESULT_GEMINI = r'data_output'
PATH_IMAGES = r'data_input'

# carrega credenciais
load_dotenv()
genai.configure(api_key="--")

# define modelo
model_name = 'gemini-1.5-pro'
model = genai.GenerativeModel(model_name=model_name)

# define o prompt
prompt = r'''
Preencha os campos do response abaixo baseando-se na imagem:
response = {
    "caracteres_numericos": STRING,
    "caracteres_alfabeticos": STRING,
    "simbolos": STRING
}

caracteres_numericos: é a string que contém todos os caracteres numéricos únicos presentes na imagem;
caracteres_alfabeticos: é a string que contém todos os caracteres alfabeticos únicos presentes na imagem;
simbolos: é a string que contém todos os símbolos únicos presentes na imagem. Ignorar emojis.

garanta que as letras, números e símbolos incluídos no response estejam na imagem.

remova carateres e símbolos duplicados.

Responda apenas com o response preenchido.
'''

# loop da solução
image_list = os.listdir(PATH_IMAGES)
t0 = time.time()
for file_name_item in image_list:
    try:
        # lê imagem
        file_name = os.path.join(PATH_IMAGES, file_name_item)
        img = PIL.Image.open(file_name)        
        # chama api
        api_response = model.generate_content([prompt, img])
        api_response_text = api_response.text
        # formata output - remove caracteres indesejados
        api_response_text = (
            api_response_text
            .strip()
            .replace(r'json', '')
            .strip(r'`')
        )
        # salva o output
        name_json = file_name_item.split('.')[0]
        file_name_json = f'{os.path.join(PATH_RESULT_GEMINI, name_json)}.json'
        with open(file_name_json, 'w', encoding='utf-8') as output:
            api_response_text = api_response_text.replace('response = ', '').strip()
            output.write(api_response_text)

    except Exception as e:
        print(f'Exception: {e}')

t1 = time.time()
n_ = len(image_list)
print(f'Tempo total: {t1-t0:.2f}s')
print(f'Tempo médio: {(t1-t0)/n_:.2f}s por item')

