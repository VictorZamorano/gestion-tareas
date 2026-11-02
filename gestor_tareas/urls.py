"""
URL configuration for gestor_tareas project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from tareas.views import (
    vista_pantalla_login,
    vista_pantalla_registro,
    vista_pantalla_tareas,
)

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', vista_pantalla_login, name='pantalla_login'),
    path('registro/', vista_pantalla_registro, name='pantalla_registro'),
    path('tareas/', vista_pantalla_tareas, name='pantalla_tareas'),

    # Endpoints de Autenticación JWT (Login)
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Rutas de la app tareas
    path('api/', include('tareas.urls')),
]
