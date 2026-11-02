from typing import ClassVar

from django.contrib.auth import get_user_model
from rest_framework import serializers

from tareas.models import Tarea

# Obtenemos el modelo de usuario personalizado (si existe) o el modelo de usuario predeterminado de Django
User = get_user_model()

# Serializador para registrar nuevos usuarios con validación estricta de datos
class RegistroSerializer(serializers.ModelSerializer):
    """
    Serializador para registrar nuevos usuarios con validación estricta de datos.
    Asegura el hashing seguro de la contraseña mediante create_user.
    """
    password = serializers.CharField(write_only=True, min_length=4, error_messages={
        'min_length': 'La contraseña debe tener al menos 4 caracteres.',
        'required': 'La contraseña es obligatoria.'
    })

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'rol')
        extra_kwargs: ClassVar[dict[str, dict[str, object]]] = {
            'email': {'required': True, 'allow_blank': False},
            'rol': {'required': False}
        }

    def validate_username(self, value):
        """Valida que el nombre de usuario no contenga espacios ni caracteres extraños peligrosos"""
        if not value.isalnum():
            raise serializers.ValidationError("El nombre de usuario solo puede contener letras y números.")
        return value

    def create(self, validated_data):
        # Se agrega is_active=True para garantizar que el usuario pueda autenticarse inmediatamente con JWT
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            rol=validated_data.get('rol', 'usuario'),
            is_active=True
        )
        return user

# Serializador para consultar los datos del usuario autenticado sin exponer la contraseña
class UsuarioPerfilSerializer(serializers.ModelSerializer):
    """Serializador para consultar los datos del usuario autenticado sin exponer la contraseña"""
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'rol', 'date_joined')
        read_only_fields = ('id', 'date_joined')

# Serializador para las tareas
class TareaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tarea
        fields = ['id', 'titulo', 'descripcion', 'completada', 'fecha_creacion', 'fecha_actualizacion']
        read_only_fields = ['id', 'fecha_creacion', 'fecha_actualizacion']

# Serializador para que el administrador pueda modificar roles o desactivar usuarios
class AdminUsuarioUpdateSerializer(serializers.ModelSerializer):
    """Serializador para que el administrador pueda modificar roles o desactivar usuarios"""
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'rol', 'is_active')
        read_only_fields = ('id', 'username', 'email')

    def validate(self, attrs):
        request = self.context.get('request')
        # Verificar si el usuario autenticado está intentando editar su propia cuenta
        if request and self.instance and request.user.id == self.instance.id:
            # Si intenta cambiar el rol
            if 'rol' in attrs and attrs['rol'] != self.instance.rol:
                raise serializers.ValidationError({"rol": "Por seguridad, no puedes cambiar tu propio rol de administrador."})
        return attrs