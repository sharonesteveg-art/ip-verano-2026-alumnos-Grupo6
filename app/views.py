# capa de vista/presentación

from django.shortcuts import redirect, render
from .layers.services import services
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.core.paginator import Paginator
from django.urls import reverse
from urllib.parse import urlencode

def index_page(request):
    return render(request, 'index.html')

def home(request):
    """
    Vista principal que muestra la galería de personajes de Los Simpsons.

    Esta función debe obtener el listado de imágenes desde la capa de servicios
    y también el listado de favoritos del usuario, para luego enviarlo al template 'home.html'.
    Recordar que los listados deben pasarse en el contexto con las claves 'images' y 'favourite_list'.
    """
    q = request.GET.get('q', '').strip()
    status = request.GET.get('status', '').strip()

    # Obtener todas las imágenes y aplicar filtros en memoria (minimalista)
    images = services.getAllImages()

    # FIX: si el filtro viene como 'all' (botón TODOS), asegurarse explícitamente
    #      de recargar todas las imágenes para evitar que queden filtros previos.
    if status and status.lower() == 'all':
        images = services.getAllImages()

    if q:
        needle = q.lower()
        images = [img for img in images if img.name and needle in img.name.lower()]

    if status and status.lower() not in ('all', ''):
        # aceptamos 'Alive' o 'Deceased' (según transport/translator)
        # comparar case-insensitive y sin espacios para no perder personajes
        images = [img for img in images if getattr(img, 'status', None) and img.status.strip().lower() == status.strip().lower()]

    # --- Cambio: paginación mínima para mantener filtros al paginar ---
    # Si status == 'all' mostramos todos en una página para asegurarnos de
    # que no queden personajes (p. ej. fallecidos) ocultos por la paginación.
    if status and status.lower() == 'all':
        per_page = max(1, len(images))
    else:
        # Mostrar más resultados por página para filtros (evita ocultar vivos en la primera página)
        per_page = 20
    paginator = Paginator(images, per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    favourite_list = services.getAllFavourites(request)

    return render(request, 'home.html', {
        'images': page_obj.object_list,
        'favourite_list': favourite_list,
        'page_obj': page_obj,
        'q': q,
        'status': status,
    })

def search(request):
    """
    Busca personajes por nombre.

    Se debe implementar la búsqueda de personajes según el nombre ingresado.
    Se debe obtener el parámetro 'query' desde el POST, filtrar las imágenes según el nombre
    y renderizar 'home.html' con los resultados. Si no se ingresa nada, redirigir a 'home'.
    """
    # FIX: Había una indentación extra en las líneas siguientes (causaba IndentationError).
    #      Unifiqué la indentación a 4 espacios y eliminé la indentación inesperada.
    # --- Cambio: recibir POST antiguo y redirigir a la vista 'home' con GET param q ---
    query = request.POST.get('query', '').strip()
    status = request.POST.get('status', '').strip()
    if not query and not status:
        return redirect('home')

    # Construir params para mantener también el filtro de status si viene
    params = {}
    if query:
        params['q'] = query
    if status:
        params['status'] = status

    qs = urlencode(params)
    # Redirige a home con la query en la URL para mantener filtros y paginación
    return redirect(f"{reverse('home')}?{qs}")




def filter_by_status(request):
    """
    Filtra personajes por su estado (Alive/Deceased).
    
    Se debe implementar el filtrado de personajes según su estado.
    Se debe obtener el parámetro 'status' desde el POST, filtrar las imágenes según ese estado
    y renderizar 'home.html' con los resultados. Si no hay estado, redirigir a 'home'.
    """
    # --- Cambio: recibir POST antiguo y redirigir a 'home' con GET param status ---
    # --- Cambio: recibir POST antiguo y redirigir a 'home' con GET param status ---
    status = request.POST.get('status', '').strip()
    q = request.POST.get('q', '').strip()
    if not status and not q:
        return redirect('home')

    # Construir params para mantener también la búsqueda por nombre si viene
    params = {}
    if status:
        params['status'] = status
    if q:
        params['q'] = q

    qs = urlencode(params)
    # Redirige a home con el filtro de status (y q si aplica)
    return redirect(f"{reverse('home')}?{qs}")

# Estas funciones se usan cuando el usuario está logueado en la aplicación.
@login_required
def getAllFavouritesByUser(request):
    """
    Obtiene todos los favoritos del usuario autenticado.
    """
    # TODO: obtener favoritos del usuario logueado
    favourite_list =  services.getAllFavourites(request) # Lista de objetos favoritos va agregando a la carpeta favoritos 
    
    return render(request, 'favourites.html', {
        'favourite_list': favourite_list
    })

@login_required
def saveFavourite(request):
    """
    Guarda un personaje como favorito.
    """
    if request.method == "POST":
        services.saveFavourite(request)

    return redirect('home')


@login_required
def deleteFavourite(request):
    """
    Elimina un favorito del usuario.
    """
    if request.method == "POST":
        services.deleteFavourite(request)

    return redirect('home')
@login_required
def exit(request):
    logout(request)
    return redirect('home')

#funcion de alta y baja de usuario 
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import RegistroForm
from django.core.mail import send_mail
from django.conf import settings

def registro_usuario(request):
    """
    Vista para registrar un nuevo usuario en la aplicación.
    
    Funciona así:
    1. Si el usuario envía el formulario (POST), valida los datos.
    2. Si todo es correcto, guarda el usuario en la base de datos.
    3. Envía un email de bienvenida con las credenciales.
    4. Muestra mensaje de éxito y redirige al login o home.
    """
    if request.method == "POST": # Verifica si se envió el formulario
         
         form = RegistroForm(request.POST)  # Crea el formulario con los datos enviados
         
         if form.is_valid():  # Valida que todos los campos sean correctos
         
            user = form.save(commit=False)  # Crea el usuario pero no lo guarda todavía
            password = form.cleaned_data['password']  # Guardamos la contraseña temporal
            user.set_password(password)  # Encripta la contraseña antes de guardar
         
            user.save()  # Guarda el usuario en la base de datos (db.sqlite3)

         
            # Enviar email de bienvenida
         
            send_mail(
         
                "Registro exitoso",  # Asunto del email
         
                f"Bienvenido!\n\nUsuario: {user.username}\nContraseña: {password}",  # Mensaje
         
                settings.EMAIL_HOST_USER,  # Remitente (desde settings.py)
                [user.email],  # Destinatario
                fail_silently=False,  # Mostrar error si falla el envío
            )

            # Mensaje que se muestra en la web
            messages.success(request, "Usuario registrado correctamente.")

            # Redirige a la página de login o home
            return redirect("home")  
    else:
        # Si no se envió el formulario (GET), crea uno vacío
        form = RegistroForm()

    # Renderiza el template 'registro.html' con el formulario
    return render(request, "registro.html", {"form": form})