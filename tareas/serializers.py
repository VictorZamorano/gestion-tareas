from typing import ClassVar

from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()

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
        # El método create_user asegura que la contraseña se guarde mediante HASH (PBKDF2)
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            rol=validated_data.get('rol', 'usuario') # Por defecto se crea como usuario común
        )
        return user


class UsuarioPerfilSerializer(serializers.ModelSerializer):
    """Serializador para consultar los datos del usuario autenticado sin exponer la contraseña"""
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'rol', 'date_joined')
        read_only_fields = ('id', 'date_joined')