# capa de servicio/lógica de negocio

import random
from ..transport import transport
from ..persistence import repositories
from ..utilities import translator
from django.contrib.auth import get_user
    # """
    # Obtiene todas las imágenes de personajes desde la API y las convierte en objetos Card.
    
    # Esta función debe obtener los datos desde transport, transformarlos en Cards usando 
    # translator y retornar una lista de objetos Card.
    # """

def getAllImages():
    json_images = transport.getAllImages()
    print("JSON IMAGES:", len(json_images))

    #cards es una lista de las cards
    cards = []

    for character in json_images:
        card = translator.fromRequestIntoCard(character)
        cards.append(card)
    print("CARDS:", len(cards))

    return cards

def filterByCharacter(name):
    """
    Filtra las cards de personajes según el nombre proporcionado.
    
    Se debe filtrar los personajes cuyo nombre contenga el parámetro recibido. Retorna una lista de Cards filtradas.
    """
    # Obtener todas las cards (vienen de la API via transport y translator)
    all_cards = getAllImages()

    # Hacer comparación case-insensitive: si el nombre del personaje contiene 'name'
    filtered = []
    needle = name.strip().lower()
    for card in all_cards:
        if card.name and needle in card.name.lower():
            filtered.append(card)

    return filtered

def filterByStatus(status_name):
    """
    Filtra las cards de personajes según su estado (Alive/Deceased).
    
    Se deben filtrar los personajes que tengan el estado igual al parámetro 'status_name'. Retorna una lista de Cards filtradas.
    """
    # Obtener todas las cards y filtrar por el campo status exactamente igual.
    all_cards = getAllImages()
    filtered = [card for card in all_cards if card.status == status_name]
    return filtered

# añadir favoritos (usado desde el template 'home.html')
def saveFavourite(request):
    """
    Guarda un favorito en la base de datos.
    
    Se deben convertir los datos del request en una Card usando el translator,
    asignarle el usuario actual, y guardarla en el repositorio.
    """
    # Crear una Card a partir de los datos enviados desde el template (request.POST)
    # translator.fromTemplateIntoCard espera el objeto request para leer POST.
    card = translator.fromTemplateIntoCard(request)

    # Asignar el usuario actual al objeto card antes de guardarlo.
    card.user = request.user

    # Guardar usando el repositorio de persistencia.
    repositories.saveFavourite(card)
    return True

def getAllFavourites(request):
    """
    Obtiene todos los favoritos del usuario autenticado.
    
    Si el usuario está autenticado, se deben obtener sus favoritos desde el repositorio,
    transformarlos en Cards usando translator y retornar la lista. Si no está autenticado, se retorna una lista vacía.
    """
    # Si el usuario no está autenticado, retornar lista vacía (no hay favoritos).
    user = request.user
    if not user or not user.is_authenticated:
        return []

    # Obtener los favoritos desde el repositorio como diccionarios y mapear a Card.
    repo_list = repositories.getAllFavourites(user)
    cards = []
    for repo_dict in repo_list:
        cards.append(translator.fromRepositoryIntoCard(repo_dict))
    return cards

def deleteFavourite(request):
    """
    Elimina un favorito de la base de datos.
    
    Se debe obtener el ID del favorito desde el POST y eliminarlo desde el repositorio.
    """
    # Obtener id del favorito enviado por POST. Aceptamos 'id' o 'favId'.
    fav_id = request.POST.get('id') or request.POST.get('favId')
    if not fav_id:
        return False

    try:
        repositories.deleteFavourite(int(fav_id))
        return True
    except Exception:
        return False