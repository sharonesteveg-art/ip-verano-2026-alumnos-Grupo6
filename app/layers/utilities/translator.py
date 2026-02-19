# translator: se refiere a un componente o conjunto de funciones que se utiliza para convertir o "mapear" datos de un formato o estructura a otro. Esta conversión se realiza típicamente cuando se trabaja con diferentes capas de una aplicación, como por ejemplo, entre la capa de datos y la capa de presentación, o entre dos modelos de datos diferentes.

from app.layers.utilities.card import Card
from ...config import config
import random

# Usado cuando la información viene de la API, para transformarla en una Card.
def fromRequestIntoCard(object):
    portrait_path = object.get('portrait_path', '')
    
    base_url = config.SIMPSONS_CDN_BASE_URL
    image_size = config.SIMPSONS_IMAGE_SIZE
    image_url = base_url + '/' + image_size + portrait_path
    
    # FIX: Si la API provee varias frases, elegir una al azar para mostrar UNA sola.
    #      Esto evita que el template muestre listas y hace la experiencia más limpia.
    raw_phrases = object.get('phrases', [])
    if isinstance(raw_phrases, (list, tuple)):
        phrase = random.choice(raw_phrases) if raw_phrases else ''
    else:
        phrase = raw_phrases or ''

    card = Card(
        name=object.get('name'),
        gender=object.get('gender'),
        status=object.get('status'),
        phrases=phrase,
        occupation=object.get('occupation'),
        image=image_url,
        age=object.get('age')
    )
    return card


# Usado cuando la información viene del template, para transformarla en una Card antes de guardarla en la base de datos.
def fromTemplateIntoCard(templ): 
    card = Card(
        name=templ.POST.get("name"),
        gender=templ.POST.get("gender"),
        status=templ.POST.get("status"),
        phrases=templ.POST.get("phrases"),
        occupation=templ.POST.get("occupation"),
        image=templ.POST.get("image"),
        age=templ.POST.get("age")
    )
    return card


# Cuando la información viene de la base de datos, para transformarla en una Card antes de mostrarla.
def fromRepositoryIntoCard(repo_dict):
    card = Card(
        id=repo_dict.get('id'),
        name=repo_dict.get('name'),
        gender=repo_dict.get('gender'),
        status=repo_dict.get('status'),
        phrases=repo_dict.get('phrases', ''),
        occupation=repo_dict.get('occupation'),
        image=repo_dict.get('image'),
        age=repo_dict.get('age')
    )
    return card
