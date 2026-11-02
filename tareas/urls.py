from django.urls import path
from rest_framework_simplejwt.views import TokenBlacklistView

# Importamos las vistas basadas en clases de tu compañero y tus vistas de funciones para tareas
from .views import (
    LoginView,
    PerfilUsuarioView,
    RegistroView,
    VistaExclusivaAdminView,
    detalle_tarea,
    lista_crear_tareas,
    vista_pantalla_perfil,
)

urlpatterns = [
    # --- Endpoints de Usuarios y Autenticación ---
    path('login/', LoginView.as_view(), name='api_login'),
    path('register/', RegistroView.as_view(), name='api_register'),
    path('perfil/', PerfilUsuarioView.as_view(), name='api_perfil'),
    path('logout/', TokenBlacklistView.as_view(), name='api_logout'), # Invalida el refresh token
    path('admin-restringido/', VistaExclusivaAdminView.as_view(), name='api_admin_restringido'),
    path('perfil-vista/', vista_pantalla_perfil, name='pantalla_perfil'),

    # --- Endpoints del CRUD de Tareas ---
    path('tareas/', lista_crear_tareas, name='api_lista_crear_tareas'),
    path('tareas/<int:pk>/', detalle_tarea, name='api_detalle_tarea'),
]