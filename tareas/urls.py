from django.urls import path
from rest_framework_simplejwt.views import TokenBlacklistView

# Importamos las vistas basadas en clases de tu compañero y tus vistas de funciones para tareas
from .views import (
    RegistroView, 
    PerfilUsuarioView, 
    VistaExclusivaAdminView,
    LoginView,
    lista_crear_tareas,
    detalle_tarea
)

urlpatterns = [
    # --- Endpoints de Usuarios y Autenticación ---
    path('login/', LoginView.as_view(), name='api_login'),
    path('register/', RegistroView.as_view(), name='api_register'),
    path('perfil/', PerfilUsuarioView.as_view(), name='api_perfil'),
    path('logout/', TokenBlacklistView.as_view(), name='api_logout'), # Invalida el refresh token
    path('admin-restringido/', VistaExclusivaAdminView.as_view(), name='api_admin_restringido'),

    # --- Endpoints del CRUD de Tareas ---
    path('tareas/', lista_crear_tareas, name='api_lista_crear_tareas'),
    path('tareas/<int:pk>/', detalle_tarea, name='api_detalle_tarea'),
]