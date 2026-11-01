from django.contrib.auth.models import AbstractUser
from django.db import models


class Usuario(AbstractUser):
  """Modelo de Usuario personalizado que extiende el sistema de autenticación

  nativo de Django para incluir roles (Administrador y Usuario).
  Garantiza el almacenamiento seguro de contraseñas mediante hash de forma automática.
  """

  ROLES = (
      ('administrador', 'Administrador'),
      ('usuario', 'Usuario'),
  )

  rol = models.CharField(
      max_length=20,
      choices=ROLES,
      default='usuario',
      help_text='Define los permisos de acceso en la aplicación.',
  )

  def __str__(self):
        # pyright: ignore[reportAttributeAccessIssue]
        return f'{self.username} ({self.get_rol_display()})'


class Tarea(models.Model):
  """Modelo para la gestión de tareas de los usuarios.

  Cada tarea está asociada de forma relacional a un usuario específico.
  """

  titulo = models.CharField(
      max_length=200, help_text='Título o nombre principal de la tarea.'
  )
  descripcion = models.TextField(
      blank=True, null=True, help_text='Detalles adicionales de la tarea.'
  )
  completada = models.BooleanField(
      default=False, help_text='Estado de finalización de la tarea.'
  )
  usuario = models.ForeignKey(
      Usuario,
      on_delete=models.CASCADE,
      related_name='tareas',
      help_text='Usuario propietario de la tarea.',
  )
  fecha_creacion = models.DateTimeField(auto_now_add=True)
  fecha_actualizacion = models.DateTimeField(auto_now=True)

  def __str__(self):
    return self.titulo