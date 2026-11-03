from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Tarea

User = get_user_model()

PASSWORD = 'ClaveSegura123!'


class GestionTareasAdminTests(APITestCase):
    """Pruebas del listado de usuarios y de la asignación de tareas."""

    def setUp(self):
        self.admin = User.objects.create_user(
            username='admin_test',
            email='admin_test@example.com',
            password=PASSWORD,
            rol='administrador',
        )
        self.juan = User.objects.create_user(
            username='juan_test',
            email='juan_test@example.com',
            password=PASSWORD,
            rol='usuario',
        )
        self.ana = User.objects.create_user(
            username='ana_test',
            email='ana_test@example.com',
            password=PASSWORD,
            rol='usuario',
        )
        self.inactivo = User.objects.create_user(
            username='inactivo_test',
            email='inactivo_test@example.com',
            password=PASSWORD,
            rol='usuario',
            is_active=False,
        )

    def autenticar(self, usuario):
        token = RefreshToken.for_user(usuario).access_token
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    # --- Listado de usuarios (panel de administración) ---

    def test_admin_lista_usuarios_incluye_is_active(self):
        self.autenticar(self.admin)

        response = self.client.get('/api/admin/usuarios/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('is_active', response.data[0])

    def test_usuario_normal_no_puede_listar_usuarios(self):
        self.autenticar(self.juan)

        response = self.client.get('/api/admin/usuarios/')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # --- Creación de tareas ---

    def test_admin_crea_tarea_para_otro_usuario(self):
        self.autenticar(self.admin)

        response = self.client.post(
            '/api/tareas/',
            {
                'titulo': 'Comprar pan',
                'descripcion': 'Encargo para Juan',
                'usuario_id': self.juan.id,
            },
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        tarea = Tarea.objects.get(pk=response.data['id'])
        self.assertEqual(tarea.usuario, self.juan)
        self.assertEqual(response.data['usuario_id'], self.juan.id)
        self.assertEqual(response.data['usuario_username'], 'juan_test')

    def test_usuario_normal_no_puede_asignar_tarea(self):
        self.autenticar(self.juan)

        response = self.client.post(
            '/api/tareas/',
            {'titulo': 'Intento', 'usuario_id': self.ana.id},
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertFalse(Tarea.objects.filter(titulo='Intento').exists())

    def test_usuario_normal_crea_tarea_para_si_mismo(self):
        self.autenticar(self.juan)

        response = self.client.post(
            '/api/tareas/', {'titulo': 'Mi tarea'}, format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        tarea = Tarea.objects.get(pk=response.data['id'])
        self.assertEqual(tarea.usuario, self.juan)

    def test_no_se_puede_asignar_a_usuario_inactivo(self):
        self.autenticar(self.admin)

        response = self.client.post(
            '/api/tareas/',
            {'titulo': 'Para inactivo', 'usuario_id': self.inactivo.id},
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertFalse(Tarea.objects.filter(titulo='Para inactivo').exists())

    def test_usuario_id_invalido_devuelve_400(self):
        self.autenticar(self.admin)

        response = self.client.post(
            '/api/tareas/',
            {'titulo': 'Tarea', 'usuario_id': 'abc'},
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('usuario_id', response.data)

    # --- Visibilidad de tareas ---

    def test_admin_ve_todas_las_tareas(self):
        Tarea.objects.create(titulo='De juan', usuario=self.juan)
        Tarea.objects.create(titulo='De admin', usuario=self.admin)
        self.autenticar(self.admin)

        response = self.client.get('/api/tareas/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        propietarios = {tarea['usuario_username'] for tarea in response.data}
        self.assertEqual(propietarios, {'juan_test', 'admin_test'})

    def test_usuario_normal_solo_ve_sus_tareas(self):
        Tarea.objects.create(titulo='De juan', usuario=self.juan)
        Tarea.objects.create(titulo='De ana', usuario=self.ana)
        self.autenticar(self.juan)

        response = self.client.get('/api/tareas/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['titulo'], 'De juan')

    # --- El admin no puede editar ni eliminar tareas ajenas ---

    def test_admin_no_puede_editar_tarea_ajena(self):
        tarea = Tarea.objects.create(titulo='De juan', usuario=self.juan)
        self.autenticar(self.admin)

        response = self.client.patch(
            f'/api/tareas/{tarea.id}/',
            {'titulo': 'Cambiada por el admin'},
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        tarea.refresh_from_db()
        self.assertEqual(tarea.titulo, 'De juan')

    def test_admin_no_puede_eliminar_tarea_ajena(self):
        tarea = Tarea.objects.create(titulo='De juan', usuario=self.juan)
        self.autenticar(self.admin)

        response = self.client.delete(f'/api/tareas/{tarea.id}/')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(Tarea.objects.filter(pk=tarea.id).exists())

    def test_patch_no_permite_reasignar_propietario(self):
        tarea = Tarea.objects.create(titulo='De juan', usuario=self.juan)
        self.autenticar(self.juan)

        response = self.client.patch(
            f'/api/tareas/{tarea.id}/',
            {'usuario_id': self.ana.id},
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        tarea.refresh_from_db()
        self.assertEqual(tarea.usuario, self.juan)
