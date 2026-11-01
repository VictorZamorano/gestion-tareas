from django.apps import AppConfig
from django.db.models.signals import post_migrate


def crear_usuario_admin_default(sender, **kwargs):
    from django.contrib.auth import get_user_model
    User = get_user_model()

    # Crea el usuario admin si no existe aún
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin',
            rol='administrador'
        )
        print("-> Usuario 'admin' (password: 'admin') creado por defecto con hash seguro.")

class TareasConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tareas'

    def ready(self):
        post_migrate.connect(crear_usuario_admin_default, sender=self)

