from django.urls import path
from . import views

urlpatterns = [
    path('tareas/', views.lista_tareas, name='lista_tareas'),
    path('tareas/crear/', views.crear_tarea, name='crear_tarea'),
    path('tareas/editar/<int:pk>/', views.editar_tarea, name='editar_tarea'),
    path('tareas/eliminar/<int:pk>/', views.eliminar_tarea, name='eliminar_tarea'),
]