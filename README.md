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

### Credenciales por defecto (Administrador)
* **Usuario:** `admin`
* **Contraseña:** `admin`

### Endpoints principales de la API (para Postman / Bruno)
* **Login (Obtener Token JWT):** `POST http://localhost:8000/api/token/`
* **Registro de usuarios:** `POST http://localhost:8000/api/register/`
* **Perfil del usuario autenticado:** `GET http://localhost:8000/api/perfil/`
* **Cerrar sesión (Invalidar Token):** `POST http://localhost:8000/api/logout/`
* **CRUD de Tareas:** `http://localhost:8000/api/tareas/`