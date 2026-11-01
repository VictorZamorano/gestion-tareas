from django.urls import path
from rest_framework_simplejwt.views import TokenBlacklistView

from . import views
from .views import PerfilUsuarioView, RegistroView, VistaExclusivaAdminView

urlpatterns = [
    # Rutas para la API de usuarios
    path('register/', RegistroView.as_view(), name='api_register'),
    path('perfil/', PerfilUsuarioView.as_view(), name='api_perfil'),
    path('logout/', TokenBlacklistView.as_view(), name='api_logout'), # Invalida el refresh token
    path('admin-restringido/', VistaExclusivaAdminView.as_view(), name='api_admin_restringido'),

    # Rutas para la API de tareas
    path('tareas/', views.lista_tareas, name='lista_tareas'),
    path('tareas/crear/', views.crear_tarea, name='crear_tarea'),
    path('tareas/editar/<int:pk>/', views.editar_tarea, name='editar_tarea'),
    path('tareas/eliminar/<int:pk>/', views.eliminar_tarea, name='eliminar_tarea'),
]