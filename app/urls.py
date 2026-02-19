from django.contrib import admin
from django.urls import path
from . import views # Importa todas las vistas que ya tengo
from .views import registro_usuario  # Importa la función de registro que cree
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index_page, name='index-page'),
    #path('login/', views.index_page, name='login'),
    path('registro/', registro_usuario, name='registro'),  # <-- Aca es donde el formulario de alta se mostrará y se procesará
    path('home/', views.home, name='home'),
    
    path('buscar/', views.search, name='buscar'),
    path('filter_by_status/', views.filter_by_status, name='filter_by_status'),

    path('favourites/', views.getAllFavouritesByUser, name='favoritos'),
    path('favourites/add/', views.saveFavourite, name='agregar-favorito'),
    path('favourites/delete/', views.deleteFavourite, name='borrar-favorito'),

    path('exit/', views.exit, name='exit'),
    
    
    # Login y Logout
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
from django.conf import settings
from django.conf.urls.static import static

# Esto sirve las imágenes durante el desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)