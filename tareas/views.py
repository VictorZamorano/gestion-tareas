from typing import Any, ClassVar

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, render
from rest_framework import generics, status
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import Tarea
from .permissions import EsAdministrador
from .serializers import RegistroSerializer, TareaSerializer, UsuarioPerfilSerializer

User = get_user_model()


def vista_pantalla_login(request):
    return render(request, 'tareas/login.html')

def vista_pantalla_registro(request):
    return render(request, 'tareas/registro.html')

def vista_pantalla_perfil(request):
    return render(request, 'tareas/perfil.html')

def vista_pantalla_tareas(request):
    return render(request, 'tareas/lista.html')

# -----------------------
# Login JWT Custom Serializer & View
# -----------------------

class MiTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Personaliza la respuesta JSON del Login para incluir los datos del usuario."""
    def validate(self, attrs: dict[str, Any]) -> dict[str, Any]:
        data = super().validate(attrs)
        # Añade la información del usuario junto con los tokens access y refresh
        data["usuario"] = {
            "id": self.user.id,
            "username": self.user.username,
            "email": self.user.email,
            "rol": getattr(self.user, "rol", "cliente"),
        }
        return data


class LoginView(TokenObtainPairView):
    """Endpoint de Login público para obtener tokens JWT y datos del usuario"""
    permission_classes: ClassVar[list] = [AllowAny]
    serializer_class = MiTokenObtainPairSerializer

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
# 1. CONSULTAR Y CREAR TAREAS
@api_view(['GET', 'POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def lista_crear_tareas(request):
    # request.user se completa automáticamente tras validar el token JWT
    if request.method == 'GET':
        tareas = Tarea.objects.filter(usuario=request.user).order_by('-fecha_creacion')
        serializer = TareaSerializer(tareas, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        serializer = TareaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(usuario=request.user)  # Asigna la tarea al usuario del Token
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 2. VER DETALLE, MODIFICAR Y ELIMINAR TAREA
@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def detalle_tarea(request, pk):
    tarea = get_object_or_404(Tarea, pk=pk, usuario=request.user)

    if request.method == 'GET':
        serializer = TareaSerializer(tarea)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        serializer = TareaSerializer(tarea, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        tarea.delete()
        return Response({'mensaje': 'Tarea eliminada correctamente'}, status=status.HTTP_204_NO_CONTENT)