# capa de vista/presentación

from django.shortcuts import redirect, render
from .layers.services import services
from app.layers.services.services import getAllImages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

def index_page(request):
    return render(request, 'index.html')

def home(request):
    # Vista principal que muestra la galería de personajes de Los Simpsons.
    # Esta función debe obtener el listado de imágenes desde la capa de servicios
    # y también el listado de favoritos del usuario, para luego enviarlo al template 'home.html'.
    # Recordar que los listados deben pasarse en el contexto con las claves 'images' y 'favourite_list'.
    # Obtener todas las imágenes usando la capa de servicios.
    # Esto cumple la consigna: "La vista home() debe llamar al servicio y pasar los datos al template.".
    images = getAllImages()

    # Obtener la lista de favoritos del usuario (si está autenticado).
    favourite_list = services.getAllFavourites(request)

    # Renderizar el template 'home.html' con las imágenes y la lista de favoritos.
    return render(request, 'home.html', {
        'images': images,
        'favourite_list': favourite_list
    })

def search(request):
    """
    Busca personajes por nombre.
    
    Se debe implementar la búsqueda de personajes según el nombre ingresado.
    Se debe obtener el parámetro 'query' desde el POST, filtrar las imágenes según el nombre
    y renderizar 'home.html' con los resultados. Si no se ingresa nada, redirigir a 'home'.
    """
    # Obtener el término de búsqueda enviado por el formulario (input name='query').
    query = request.POST.get('query', '').strip()

    # Si no hay término, redirigir a la página principal (home).
    if not query:
        return redirect('home')

    # Usar la capa de servicios para filtrar por nombre.
    images = services.filterByCharacter(query)
    favourite_list = services.getAllFavourites(request)

    # Renderizar los resultados en el mismo template 'home.html'.
    return render(request, 'home.html', {
        'images': images,
        'favourite_list': favourite_list
    })

def filter_by_status(request):
    """
    Filtra personajes por su estado (Alive/Deceased).
    
    Se debe implementar el filtrado de personajes según su estado.
    Se debe obtener el parámetro 'status' desde el POST, filtrar las imágenes según ese estado
    y renderizar 'home.html' con los resultados. Si no hay estado, redirigir a 'home'.
    """
    # Obtener el estado desde el formulario POST (hidden input name='status').
    status = request.POST.get('status', '').strip()
    if not status:
        return redirect('home')

    # Filtrar usando la capa de servicios.
    images = services.filterByStatus(status)
    favourite_list = services.getAllFavourites(request)

    # Renderizar resultados filtrados.
    return render(request, 'home.html', {
        'images': images,
        'favourite_list': favourite_list
    })

# Estas funciones se usan cuando el usuario está logueado en la aplicación.
@login_required
def getAllFavouritesByUser(request):
    """
    Obtiene todos los favoritos del usuario autenticado.
    """
    # Devuelve la lista de favoritos del usuario autenticado en formato JSON o render.
    # Aquí optamos por renderizar la misma plantilla con la lista (consistencia con home).
    favourite_list = services.getAllFavourites(request)
    images = []
    return render(request, 'home.html', {
        'images': images,
        'favourite_list': favourite_list
    })

@login_required
def saveFavourite(request):
    """
    Guarda un personaje como favorito.
    """
    # Guarda un favorito usando la capa de servicios y redirige a home.
    if request.method == 'POST':
        services.saveFavourite(request)
    return redirect('home')

@login_required
def deleteFavourite(request):
    """
    Elimina un favorito del usuario.
    """
    if request.method == 'POST':
        services.deleteFavourite(request)
    return redirect('home')

@login_required
def exit(request):
    logout(request)
    return redirect('home')