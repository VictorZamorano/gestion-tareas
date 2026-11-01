from typing import Any, ClassVar

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .forms import TareaForm
from .models import Tarea
from .permissions import EsAdministrador
from .serializers import RegistroSerializer, UsuarioPerfilSerializer

User = get_user_model()
# -----------------------
# Usuarios API Views
# ------------------------
class RegistroView(generics.CreateAPIView):
    """Permite registrar nuevos usuarios con validación de datos (Público)"""
    queryset = User.objects.all()
    permission_classes: ClassVar[list] = [AllowAny]
    serializer_class = RegistroSerializer

    def create(self, request, *args, **kwargs):
        # Manejo controlado de errores de validación de datos
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "mensaje": "Usuario registrado exitosamente.",
                "usuario": {
                    "id": user.id,
                    "username": user.username,
                    "rol": user.rol
                }
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PerfilUsuarioView(generics.RetrieveAPIView):
    """Permite al usuario autenticado consultar sus propios datos"""
    permission_classes: ClassVar[list] = [IsAuthenticated]
    serializer_class = UsuarioPerfilSerializer

    def get_object(self) -> Any:  # pyright: ignore[reportIncompatibleMethodOverride]
        # Retorna el usuario extraído directamente del token JWT autenticado
        return self.request.user


class VistaExclusivaAdminView(generics.ListAPIView):
    """Ejemplo de endpoint protegido exclusivo para administradores"""
    permission_classes: ClassVar[list] = [IsAuthenticated, EsAdministrador]
    serializer_class = UsuarioPerfilSerializer
    queryset = User.objects.all()


# -----------------------
# Tareas API Views
#------------------------
def obtener_usuario_actual(request):
    """Devuelve el usuario logueado o el primer usuario de la BD para pruebas."""
    if request.user.is_authenticated:
        return request.user
    # Para desarrollo: asigna el primer usuario existente en la BD
    return User.objects.first()

@login_required
def lista_tareas(request):
    usuario = obtener_usuario_actual(request)
    tareas = Tarea.objects.filter(usuario=usuario).order_by('-fecha_creacion')
    return render(request, 'tareas/lista.html', {'tareas': tareas})

@login_required
def crear_tarea(request):
    usuario = obtener_usuario_actual(request)
    if request.method == 'POST':
        form = TareaForm(request.POST)
        if form.is_valid():
            tarea = form.save(commit=False)
            tarea.usuario = usuario  # Asigna la tarea al usuario actual
            tarea.save()
            return redirect('lista_tareas')
    else:
        form = TareaForm()
    return render(request, 'tareas/form_tarea.html', {'form': form, 'titulo_pagina': 'Crear Tarea'})

@login_required
def editar_tarea(request, pk):
    usuario = obtener_usuario_actual(request)
    tarea = get_object_or_404(Tarea, pk=pk, usuario=usuario)
    if request.method == 'POST':
        form = TareaForm(request.POST, instance=tarea)
        if form.is_valid():
            form.save()
            return redirect('lista_tareas')
    else:
        form = TareaForm(instance=tarea)
    return render(request, 'tareas/form_tarea.html', {'form': form, 'titulo_pagina': 'Editar Tarea'})

@login_required
def eliminar_tarea(request, pk):
    usuario = obtener_usuario_actual(request)
    tarea = get_object_or_404(Tarea, pk=pk, usuario=usuario)
    if request.method == 'POST':
        tarea.delete()
        return redirect('lista_tareas')
    return render(request, 'tareas/eliminar_confirmar.html', {'tarea': tarea})