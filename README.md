# Gestor de tareas

## Iniciarlizar
Haz uso del comando para crear el entorno con python.

    python -m venv venv
    .\venv\Scripts\Activate.ps1

    pip install -r requirements.txt

## Ejecución
Aplica las migraciones de la base de datos e inicia el servidor de desarrollo:

    python manage.py migrate
    python manage.py runserver


## Pruebas y Uso
Una vez que el servidor esté activo, puedes acceder a la interfaz web en tu navegador:

    http://localhost:8000/

### Credenciales por defecto
* **Rol: Administrador**
* **Usuario:** `admin`
* **Contraseña:** `admin`

* **Rol: Usuario**
* **Usuario:** `usuario2`
* **Contraseña:** `usuario2`

Los usuarios estan añadidos en el archivo db.sqlite para pruebas, recuerda ignorarlo en el archivo **.gitignore** si no deseas subir TU base de datos.

### Endpoints principales de la API (para Postman / Bruno)
* **Login (Obtener Token JWT):** `POST http://localhost:8000/api/token/`
* **Registro de usuarios:** `POST http://localhost:8000/api/register/`
* **Perfil del usuario autenticado:** `GET http://localhost:8000/api/perfil/`
* **Cerrar sesión (Invalidar Token):** `POST http://localhost:8000/api/logout/`
* **CRUD de Tareas:** `http://localhost:8000/api/tareas/`
* **Gestión de usuarios (Solo Admin - Listar):** `GET http://localhost:8000/api/admin/usuarios/`
* **Modificar rol o estado de un usuario (Solo Admin):** `PATCH http://localhost:8000/api/admin/usuarios/<id>/`