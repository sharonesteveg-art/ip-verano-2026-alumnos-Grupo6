from django.contrib import admin
from django.urls import path
from . import views # Importa todas las vistas que ya tengo
from .views import registro_usuario  # Importa la función de registro que cree

urlpatterns = [
    path('', views.index_page, name='index-page'),
    path('login/', views.index_page, name='login'),
    path('registro/', registro_usuario, name='registro'),  # <-- Aca es donde el formulario de alta se mostrará y se procesará
    path('home/', views.home, name='home'),
    
    path('buscar/', views.search, name='buscar'),
    path('filter_by_status/', views.filter_by_status, name='filter_by_status'),

    path('favourites/', views.getAllFavouritesByUser, name='favoritos'),
    path('favourites/add/', views.saveFavourite, name='agregar-favorito'),
    path('favourites/delete/', views.deleteFavourite, name='borrar-favorito'),

    path('exit/', views.exit, name='exit'),
]
from django.conf import settings
from django.conf.urls.static import static

# Esto sirve las imágenes durante el desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)