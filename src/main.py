import streamlit as st
import pandas as pd
import requests
import sys
import random
import vertexai
from vertexai.preview.vision_models import Image, ImageGenerationModel
from vertexai.preview.generative_models import (
    GenerationConfig,
    GenerativeModel,
    Image,
    Part,
)
from PIL import Image
import concurrent.futures

app_formal_name = "Imagen 3 Moodboard"

# Start the app in wide-mode
st.set_page_config(
    layout="wide", page_title=app_formal_name,
)


prompt = """
Generate 16 creative prompts, for Imagen to create images illustrating the input topics.
One prompt per line without a number a dash or a bullet.
New line for every prompt.
Just the prompt.
The goal is to create a mood board.
Prompts should mix and match the topics and be as diverse and as creative as possible.
I want to generate images of clothings, matters, objects, arts, etc.

Topics:
{topics}


Prompts:
"""

title_element = st.empty()
gemini_element = st.empty()
imagen_element = st.empty()


title = f"Design Moodboard"
title_element.title(title)
gemini_element.write("Prompts generated by Gemini 1.5 based on the topics :")
topics = st.text_input('Topics', 'Summer, Diaphanous, Sculptural Volumes, Elongated Silhouette, Metallics, Black, Polo Shirt, Roses, Feathery Touches')
imagen_element.write("Images generated by Imagen 3")

print("INIT VERTEX")
vertexai.init(project="svc-demo-vertex", location="us-central1")


textmodel = GenerativeModel("gemini-1.5-pro")

generation_config = GenerationConfig(
    temperature=0.9,
    top_p=1.0,
    top_k=32,
    candidate_count=1,
    max_output_tokens=8192,
)

model = ImageGenerationModel.from_pretrained("imagen-3.0-generate-001")


prompt_element = st.empty()

def generate_image(prompt: str):
    print(prompt)
    try:
        images = model.generate_images(
          prompt=prompt,
          number_of_images=1,
        )
        print("DONE")
        return prompt, images[0]._as_base64_string()
    except Exception as e:
        print(f"Error fetching data from {prompt}: {e}")
        return None
    
if st.button('Generate'):
    prompts = textmodel.generate_content(prompt.format(topics=topics), generation_config=generation_config).text.splitlines()
    prompts = list(filter(None, prompts))
    prompt_element.write(prompts)
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Use executor.map to parallelize the calls
        results = list(executor.map(generate_image, prompts))


    b64s = [result for result in results if result]
    prompt_element.write('')
    print(len(b64s))

    # Uses CSS Masonry from 
    # https://w3bits.com/labs/css-masonry/

    divs = [
        f"""
        <div class="brick">
            <img src="data:image/png;base64, {b64[1]}" style="max-width:100%; height:auto;" title="{b64[0]}" />
        </div>
        """
        for b64 in b64s
    ]
    divs = "\n".join(divs)

    with open("css/labs.css") as FIN:
        css0 = FIN.read()

    with open("css/masonry.css") as FIN:
        css1 = FIN.read()


    html = """
    <html>
      <base target="_blank" />
      <head>
        <style> %s </style>
        <style> %s </style>
      </head>
      <body>
      <div class="masonry gutterless">
      %s
      </div>
      </body>
    </html>
    """ % (
        css0,
        css1,
        divs,
    )
    st.components.v1.html(html, height=2400, scrolling=True)
else:
    st.components.v1.html("<html></html>", height=2400, scrolling=True)