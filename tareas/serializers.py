from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers

from tareas.models import Tarea

# Obtenemos el modelo de usuario personalizado (si existe) o el modelo de usuario predeterminado de Django
User = get_user_model()

# Serializador para registrar nuevos usuarios con validación estricta de datos
class RegistroSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        min_length=8,
        error_messages={
            'min_length': 'La contraseña debe tener al menos 8 caracteres.',
        },
    )
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'password2')

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.pop('password2', None)

        if password != password2:
            raise serializers.ValidationError(
                {'password2': 'Las contraseñas no coinciden.'}
            )

        # create_user() hashea la contraseña, pero no ejecuta los validadores
        # configurados en AUTH_PASSWORD_VALIDATORS. Los aplicamos aquí.
        usuario_temporal = User(
            username=attrs.get('username', ''),
            email=attrs.get('email', ''),
        )
        try:
            validate_password(password, user=usuario_temporal)
        except DjangoValidationError as exc:
            raise serializers.ValidationError(
                {'password': list(exc.messages)}
            ) from exc

        return attrs

    def create(self, validated_data):
        return User.objects.create_user(
            **validated_data,
            rol='usuario',  # nunca desde el cliente
            is_active=True,
        )

# Serializador para consultar los datos del usuario autenticado sin exponer la contraseña
class UsuarioPerfilSerializer(serializers.ModelSerializer):
    """Serializador para consultar los datos del usuario autenticado sin exponer la contraseña"""
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'rol', 'date_joined')
        read_only_fields = ('id', 'date_joined')

# Serializador para las tareas
class TareaSerializer(serializers.ModelSerializer):
    # Datos de solo lectura del propietario. El campo "usuario" NO es
    # escribible, así que una tarea no se puede reasignar con un PATCH.
    usuario_id = serializers.IntegerField(source='usuario.id', read_only=True)
    usuario_username = serializers.CharField(
        source='usuario.username', read_only=True
    )

    class Meta:
        model = Tarea
        fields = [
            'id', 'titulo', 'descripcion', 'completada',
            'usuario_id', 'usuario_username',
            'fecha_creacion', 'fecha_actualizacion',
        ]
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
        if not request or not self.instance:
            return attrs

        es_uno_mismo = request.user.id == self.instance.id
        nuevo_rol = attrs.get('rol', self.instance.rol)
        nuevo_estado = attrs.get('is_active', self.instance.is_active)

        if es_uno_mismo:
            if 'rol' in attrs and attrs['rol'] != self.instance.rol:
                raise serializers.ValidationError({
                    'rol': 'Por seguridad, no puedes cambiar tu propio rol.'
                })
            if 'is_active' in attrs and not attrs['is_active']:
                raise serializers.ValidationError({
                    'is_active': 'Por seguridad, no puedes desactivar tu propia cuenta.'
                })

        # Protección adicional: si el usuario editado es el último administrador
        # activo, no se le puede quitar el rol ni desactivar.
        era_admin_activo = (
            self.instance.rol == 'administrador' and self.instance.is_active
        )
        seguira_siendo_admin_activo = (
            nuevo_rol == 'administrador' and nuevo_estado
        )
        if era_admin_activo and not seguira_siendo_admin_activo:
            otros_admins = User.objects.filter(
                rol='administrador', is_active=True
            ).exclude(pk=self.instance.pk)
            if not otros_admins.exists():
                raise serializers.ValidationError(
                    'Debe existir al menos un administrador activo en el sistema.'
                )

        return attrs

class AdminUsuarioListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
            'rol',
            'is_active',
            'date_joined',
            'last_login',
        )
        read_only_fields = fields