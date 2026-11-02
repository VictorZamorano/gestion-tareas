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


## Pruebas
Para poder abrir el

    http://localhost:8000/