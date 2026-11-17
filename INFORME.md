# Desarrollo de un Gestor de Tareas Web con Django y Apoyo de Inteligencia Artificial

**Informe de trabajo práctico**

- **Asignatura:** [Completar]
- **Integrantes:** [Completar]
- **Docente:** [Completar]
- **Fecha:** [Completar]

---

## 1. Introducción

La organización de tareas es una necesidad habitual en equipos de estudio, proyectos académicos y trabajos colaborativos. En muchos casos, la gestión se realiza con notas sueltas, planillas o mensajes, lo que dificulta saber quién es responsable de cada tarea, cuál es su estado y quién puede modificarla. Cuando además intervienen distintos niveles de responsabilidad, aparece la necesidad de distinguir entre usuarios comunes y administradores que supervisan el trabajo del resto.

Para abordar esa necesidad se desarrolló **Gestor de Tareas**, una aplicación web construida con **Django** y **Django REST Framework (DRF)** que permite registrarse, iniciar sesión, administrar tareas personales y, en el caso de los administradores, gestionar usuarios y tareas de otros. La autenticación se implementó con **JSON Web Tokens (JWT)** mediante SimpleJWT, y la interfaz se construyó con plantillas HTML, Tailwind CSS y JavaScript sin frameworks adicionales.

El propósito de utilizar inteligencia artificial durante el desarrollo fue acelerar las tareas repetitivas y mejorar la calidad del código: análisis del repositorio, implementación de funcionalidades, revisión de medidas de seguridad, generación de pruebas automatizadas y documentación. La IA se utilizó como un asistente técnico dentro del editor, no como un reemplazo del criterio del grupo. Cada cambio propuesto fue revisado, ejecutado y validado con pruebas antes de darlo por definitivo.

---

## 2. Objetivos

### 2.1 Objetivo general

Desarrollar una aplicación web para la gestión de tareas personales con autenticación basada en JWT y control de acceso por roles, incorporando herramientas de inteligencia artificial como apoyo en el análisis, la implementación y la verificación del código.

### 2.2 Objetivos específicos

1. Modelar usuarios con roles diferenciados y tareas asociadas a un propietario.
2. Implementar el registro, el inicio y el cierre de sesión utilizando JWT.
3. Desarrollar el CRUD de tareas con permisos basados en el propietario del recurso.
4. Construir un panel de administración para consultar usuarios y modificar su rol o estado.
5. Permitir que el administrador cree, visualice, complete y elimine tareas de cualquier usuario.
6. Aplicar medidas de seguridad tanto en el backend como en el frontend.
7. Verificar el funcionamiento mediante pruebas automatizadas y documentar el proceso de desarrollo asistido por IA.

---

## 3. Desarrollo

### 3.1 Problema o necesidad abordada

El problema central es la falta de una herramienta sencilla que permita organizar tareas personales y, al mismo tiempo, ofrecer una visión administrativa del conjunto. La aplicación debía resolver dos necesidades complementarias:

- Que cada usuario pudiera crear, consultar, completar y eliminar sus propias tareas.
- Que un administrador pudiera supervisar a los usuarios, asignarles tareas y colaborar en su gestión.

Se definieron los siguientes requisitos funcionales:

| Código | Requisito |
|---|---|
| RF1 | Registro de usuarios con validación de datos y contraseña. |
| RF2 | Inicio de sesión con JWT y datos del usuario en la respuesta. |
| RF3 | Consulta del perfil del usuario autenticado. |
| RF4 | CRUD de tareas propias. |
| RF5 | Panel de administración para listar usuarios y cambiar su rol o estado. |
| RF6 | El administrador puede crear tareas para otros usuarios. |
| RF7 | El administrador puede ver, completar y eliminar tareas ajenas. |
| RF8 | Cierre de sesión con invalidación del refresh token. |

Como requisitos no funcionales se priorizaron la seguridad, la claridad del código, la separación de responsabilidades y la facilidad para ejecutar el proyecto en un entorno académico.

### 3.2 Lenguaje y framework utilizados

La aplicación se desarrolló con las siguientes tecnologías:

| Tecnología | Versión | Uso |
|---|---|---|
| Python | 3.x | Lenguaje principal. |
| Django | 6.1.2 | Framework web, ORM, autenticación y migraciones. |
| Django REST Framework | 3.18.3 | Serializadores, vistas y permisos de la API. |
| djangorestframework-simplejwt | 5.5.1 | Autenticación mediante JWT. |
| SQLite | Incluida en Django | Base de datos del proyecto. |
| HTML5 + Tailwind CSS | CDN | Interfaz de usuario. |
| JavaScript | Vanilla | Consumo de la API y lógica del frontend. |

Se eligió Django por su ORM, su sistema de autenticación integrado, su soporte de migraciones y sus mecanismos de seguridad por defecto. DRF permitió separar la lógica de la API mediante serializadores y permisos reutilizables. SimpleJWT se utilizó para que el frontend pudiera autenticarse con tokens en lugar de sesiones, lo que facilita el refresco automático y el cierre de sesión controlado.

### 3.3 Base de datos utilizada

Se utilizó **SQLite**, con el archivo `db.sqlite3` en la raíz del proyecto. Es una base adecuada para un trabajo académico porque no requiere un servidor adicional y permite ejecutar la aplicación con un solo comando. En un despliegue real se recomendaría PostgreSQL.

El modelo de datos se compone de dos entidades:

**Usuario** (`tareas/models.py`): extiende `AbstractUser` e incorpora el campo `rol`.

| Campo | Tipo | Descripción |
|---|---|---|
| `username`, `email`, `password` | Heredados | Datos de autenticación. |
| `rol` | `CharField` con opciones | `administrador` o `usuario`. Por defecto, `usuario`. |

**Tarea**: representa una tarea asociada a un usuario.

| Campo | Tipo | Descripción |
|---|---|---|
| `titulo` | `CharField(200)` | Título de la tarea. |
| `descripcion` | `TextField` | Detalle opcional. |
| `completada` | `BooleanField` | Estado de finalización. |
| `usuario` | `ForeignKey(Usuario)` | Propietario. `on_delete=CASCADE`, `related_name='tareas'`. |
| `fecha_creacion` | `DateTimeField(auto_now_add)` | Fecha de alta. |
| `fecha_actualizacion` | `DateTimeField(auto_now)` | Última modificación. |

La relación es **uno a muchos**: un usuario puede tener muchas tareas y cada tarea pertenece a un único usuario.

### 3.4 Arquitectura o estructura general

La aplicación sigue el patrón **MVT** de Django para las vistas HTML y una **API REST** para la comunicación con el frontend. La estructura general es:

```text
gestor_tareas/
├── manage.py
├── requirements.txt
├── db.sqlite3
├── gestor_tareas/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
└── tareas/
    ├── models.py
    ├── serializers.py
    ├── views.py
    ├── permissions.py
    ├── urls.py
    ├── tests.py
    ├── apps.py
    ├── templates/tareas/
    │   ├── login.html
    │   ├── registro.html
    │   ├── lista.html
    │   └── perfil.html
    └── static/tareas/js/
        └── api.js
```

El flujo de una petición es el siguiente:

```text
Plantilla HTML + JS
        │  fetch con Bearer token
        ▼
Vista DRF (views.py)
        │  valida JWT y permisos
        ▼
Serializer (serializers.py)
        │  valida y transforma datos
        ▼
Modelo / ORM (models.py)
        ▼
SQLite
```

El frontend guarda el access token y el refresh token en `localStorage`. La función `apiFetch` de `api.js` agrega el encabezado `Authorization`, y si recibe un `401` intenta renovar el token una sola vez antes de reintentar la petición.

Los endpoints principales son:

| Método | Ruta | Acceso | Función |
|---|---|---|---|
| POST | `/api/login/` | Público | Login y datos del usuario. |
| POST | `/api/register/` | Público | Registro. |
| POST | `/api/token/refresh/` | Público | Renovar access token. |
| GET | `/api/perfil/` | Autenticado | Perfil propio. |
| POST | `/api/logout/` | Autenticado | Invalidar refresh token. |
| GET | `/api/tareas/` | Autenticado | Listar tareas. |
| POST | `/api/tareas/` | Autenticado | Crear tarea. |
| GET/PUT/PATCH/DELETE | `/api/tareas/<id>/` | Autenticado | Detalle y gestión. |
| GET | `/api/admin/usuarios/` | Administrador | Listar usuarios. |
| PATCH | `/api/admin/usuarios/<id>/` | Administrador | Cambiar rol o estado. |

### 3.5 Funcionalidades implementadas

- **Registro con validación:** se exige una contraseña de al menos 8 caracteres, se aplican los validadores de Django y se confirma con `password2`. El rol enviado por el cliente se ignora y siempre se asigna `usuario`.
- **Login con JWT:** el serializador personalizado devuelve `access`, `refresh` y los datos básicos del usuario.
- **Perfil:** el usuario autenticado consulta sus propios datos.
- **Logout real:** se envía el refresh token a `/api/logout/` para incluirlo en la lista negra y luego se limpia el almacenamiento local.
- **CRUD de tareas:** creación, listado, consulta, edición, marcado como completada y eliminación.
- **Permisos por propietario:** un usuario normal solo accede a sus tareas; si intenta acceder a una ajena recibe `404`.
- **Panel de administración:** listado de usuarios con rol, estado y última conexión; cambio de rol y activación/desactivación.
- **Gestión administrativa de tareas:** el administrador ve todas las tareas con su propietario, puede crear tareas para otros usuarios, completarlas y eliminarlas, pero no editar su título ni descripción.
- **Refresco automático del token:** si el access token expira, se renueva con el refresh token y se reintenta la petición.
- **Pruebas automatizadas:** 16 pruebas que cubren autenticación, permisos, visibilidad y gestión de tareas.

### 3.6 Herramientas de inteligencia artificial utilizadas

Se utilizó **OpenCode**, un agente de código integrado en el entorno de desarrollo, con un modelo de lenguaje de la familia **Big Pickle**. A diferencia de un autocompletado tradicional, el agente puede leer archivos del repositorio, proponer cambios en varios archivos, ejecutar comandos y analizar los resultados de las pruebas.

Las capacidades utilizadas fueron:

- Lectura y análisis del proyecto completo.
- Edición de archivos Python, HTML y JavaScript.
- Ejecución de `manage.py check`, `makemigrations`, `manage.py test` y `node --check`.
- Explicación de errores y propuesta de correcciones.
- Generación de pruebas automatizadas.
- Modo de planificación para discutir un cambio antes de escribir código.

### 3.7 Forma en que se utilizaron los prompts

Los prompts se redactaron en español y siguieron una estructura incremental:

1. **Contexto:** indicar el framework, los archivos involucrados y el comportamiento actual.
2. **Objetivo:** describir el resultado esperado.
3. **Restricciones:** aclarar qué no debía modificarse (por ejemplo, mantener la simplicidad o no tocar la configuración de desarrollo).
4. **Criterio de aceptación:** definir cómo se comprobaría el resultado.
5. **Verificación:** pedir explícitamente que se ejecutaran las comprobaciones y las pruebas.

También se utilizó el **modo Plan** del agente para analizar alternativas antes de modificar archivos. Esto permitió acordar el alcance con el grupo y evitar cambios innecesarios. Cuando una propuesta crecía demasiado, se ajustó el prompt para reducir el alcance, por ejemplo: «la idea es dejarlo sencillo y entendible».

### 3.8 Ejemplos de prompts utilizados

| Prompt | Intención | Resultado |
|---|---|---|
| «El punto 1 lo hice, verificalo, y hazme el punto 3, 4, 5, 6 y 7» | Verificar un cambio previo e implementar varias mejoras. | Validación de contraseñas, logout con blacklist, corrección de XSS, refresco de JWT y protección del administrador. |
| «Ahora mismo hay un problema que la api /api/admin/usuarios no manda el is_active» | Diagnosticar un dato faltante en la API. | Se detectó que la vista reutilizaba `UsuarioPerfilSerializer` y se creó `AdminUsuarioListSerializer`. |
| «Necesito que el form crear una tarea no solo sea para el mismo, sino que puede crear tareas para otros usuarios» | Ampliar la creación de tareas al administrador. | Se agregó el selector de usuarios y la validación de `usuario_id` en el backend. |
| «La idea es dejarlo sencillo y entendible, ¿es posible que el admin pueda crear solo tareas para los demás usuarios, sin editar ni eliminar?» | Reducir el alcance de una propuesta. | Se simplificó el diseño y se separaron las responsabilidades. |
| «También necesito que las pueda completar, las tareas ajenas» | Permitir al administrador cambiar el estado de tareas ajenas. | Se habilitó `PATCH` con el campo `completada` y se bloqueó la edición del resto de los campos. |
| «El html que tenga una sección exclusiva está bien, ¿no hay problema de seguridad con eso?» | Revisar si ocultar HTML era suficiente. | Se explicó que la seguridad depende del backend y se verificó el `403` para usuarios normales. |
| «El punto 2 lo dejo así, porque es un trabajo de universidad y no irá a producción» | Documentar una decisión consciente. | Se mantuvieron `DEBUG=True`, la `SECRET_KEY` y el usuario `admin/admin` como configuración académica. |

### 3.9 Código o funcionalidades generadas con apoyo de IA

La IA generó borradores de varios fragmentos. Todos fueron revisados y adaptados por el grupo. Algunos ejemplos representativos:

**Validación de contraseñas en el registro:**

```python
def validate(self, attrs):
    password = attrs.get('password')
    password2 = attrs.pop('password2', None)

    if password != password2:
        raise serializers.ValidationError(
            {'password2': 'Las contraseñas no coinciden.'}
        )

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
```

**Propietario de solo lectura en las tareas:**

```python
class TareaSerializer(serializers.ModelSerializer):
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
```

**Asignación de tareas a otros usuarios, validada en el backend:**

```python
if 'usuario_id' in datos:
    if not _es_administrador(request.user):
        return Response(
            {'usuario_id': [
                'Solo un administrador puede asignar tareas a otros usuarios.'
            ]},
            status=status.HTTP_403_FORBIDDEN,
        )

    usuario_destino = get_object_or_404(
        User, pk=int(datos.pop('usuario_id')), is_active=True
    )
```

**Permisos del administrador sobre tareas ajenas:**

```python
if request.method in ('PUT', 'PATCH') and tarea.usuario_id != request.user.id:
    if not _es_administrador(request.user):
        return Response(status=status.HTTP_403_FORBIDDEN)

    campos_no_permitidos = set(request.data) - {'completada'}
    if campos_no_permitidos:
        return Response(
            {'detail': 'Solo puedes cambiar el estado de completada.'},
            status=status.HTTP_403_FORBIDDEN,
        )
```

**Refresco automático del token en el frontend:**

```javascript
if (response.status === 401 && reintentar) {
  const nuevoAccess = await refreshAccessToken();

  if (nuevoAccess) {
    return apiFetch(url, options, false);
  }

  clearSession();
  redirectToLogin();
}
```

La IA también generó el esqueleto de las 16 pruebas automatizadas, que luego se ejecutaron y ajustaron hasta obtener un resultado exitoso.

### 3.10 Modificaciones realizadas por el grupo

El grupo no aceptó el código de forma automática. Se realizaron las siguientes modificaciones y decisiones:

- Se verificó que el registro ignorara el rol enviado por el cliente y se eliminó un `return` inalcanzable.
- Se decidió que el administrador **vea todas las tareas**, pero que solo pueda **editar las propias**. Para las ajenas puede cambiar el estado de completada y eliminarlas.
- Se descartó una propuesta inicial más amplia (gestión total de tareas ajenas) para mantener el proyecto comprensible.
- Se corrigió la línea redundante que impedía que el administrador accediera a tareas ajenas.
- Se cambió `ListCreateAPIView` por `ListAPIView` en la gestión de usuarios, para evitar la creación de cuentas sin contraseña.
- Se corrigió `STATIC_URL` y se centralizó la lógica de autenticación en `api.js`.
- Se cambió `LANGUAGE_CODE` a `es` para que los mensajes de validación se mostraran en español.
- Se mantuvo la configuración de desarrollo (`DEBUG=True`, `SECRET_KEY` fija y usuario `admin/admin`) por tratarse de un trabajo académico, dejando constancia de la limitación.

### 3.11 Problemas detectados en el código generado

| Problema | Síntoma | Causa | Solución |
|---|---|---|---|
| `is_active` ausente | Todos los usuarios aparecían como «Desactivado». | El listado reutilizaba `UsuarioPerfilSerializer`, que no incluía el campo. | Se creó `AdminUsuarioListSerializer` y se usó en la vista. |
| Riesgo de XSS | Datos del servidor insertados con `innerHTML`. | Concatenación de HTML con valores dinámicos. | Se reemplazó por `createElement` y `textContent`. |
| Creación de usuarios sin contraseña | `POST /api/admin/usuarios/` devolvía `405` o permitía datos incompletos. | La vista heredaba de `ListCreateAPIView`. | Se cambió a `ListAPIView`. |
| `return` inalcanzable | Código muerto en `RegistroSerializer`. | Se dejó un `return` después de otro. | Se eliminó. |
| `STATIC_URL` relativa | El archivo `api.js` no se resolvía correctamente. | `STATIC_URL = 'static/'` sin barra inicial. | Se cambió a `/static/`. |
| Rol por defecto incorrecto | El login devolvía `"cliente"` si faltaba el rol. | Valor de respaldo heredado. | Se cambió a `"usuario"`. |
| Administrador bloqueado | El admin recibía `404` en tareas ajenas. | Un `get_object_or_404` previo filtraba por propietario antes de la comprobación de rol. | Se eliminó la línea redundante. |
| Condición de carrera en el frontend | Los botones no aparecían al cargar la lista. | `cargarTareas()` se ejecutaba antes de conocer el `currentUserId`. | Se encadenaron las llamadas de forma secuencial. |
| Ausencia de pruebas | `manage.py test` encontraba 0 tests. | No se habían creado pruebas. | Se agregaron 16 pruebas. |
| Sin soporte de `PATCH` | El frontend no podía actualizar parcialmente una tarea. | La vista solo aceptaba `PUT`. | Se añadió `PATCH`. |

### 3.12 Medidas de seguridad implementadas

- **Contraseñas:** se utiliza el hash de Django, validadores de `AUTH_PASSWORD_VALIDATORS`, longitud mínima de 8 caracteres y confirmación mediante `password2`.
- **JWT:** access token de 15 minutos, refresh token de 1 día, rotación de refresh y lista negra tras la rotación. El logout invalida el refresh token.
- **Autorización en el backend:** el permiso `EsAdministrador` protege los endpoints de administración. La seguridad no depende de ocultar HTML.
- **Propiedad de los recursos:** las tareas se filtran por `usuario=request.user` para los usuarios normales. Las tareas ajenas devuelven `404` para no revelar su existencia.
- **Rol no escribible:** el registro ignora cualquier `rol` enviado por el cliente y fuerza `usuario`.
- **Protección del administrador:** no puede cambiarse el propio rol ni desactivar su cuenta, y el sistema impide quedarse sin al menos un administrador activo.
- **Reasignación bloqueada:** `usuario` no es un campo escribible del serializador; un `PATCH` no puede cambiar el propietario.
- **XSS:** el frontend construye el DOM con `createElement` y `textContent`, sin interpolar datos del servidor en `innerHTML`.
- **Asignación de tareas:** solo un administrador puede enviar `usuario_id`; un usuario normal recibe `403`.

**Limitaciones asumidas:** al ser un trabajo académico que no se despliega en producción, se mantuvieron `DEBUG=True`, una `SECRET_KEY` fija y el usuario `admin/admin`. En un entorno real se usarían variables de entorno, `DEBUG=False`, HTTPS, `createsuperuser` y una base de datos como PostgreSQL.

### 3.13 Capturas de pantalla

> **Figura 1. Pantalla de inicio de sesión.**
> *Cómo obtenerla:* ejecutar `python manage.py runserver`, abrir `http://localhost:8000/` y capturar la pantalla completa.

> **Figura 2. Registro con validación de contraseña.**
> *Cómo obtenerla:* abrir `/registro/`, ingresar una contraseña débil y capturar el mensaje de error.

> **Figura 3. Lista de tareas de un usuario normal.**
> *Cómo obtenerla:* iniciar sesión con un usuario común y capturar la lista con sus tareas.

> **Figura 4. Panel de administración y selector «Asignar a».**
> *Cómo obtenerla:* iniciar sesión como administrador y capturar el panel junto con el formulario de creación.

> **Figura 5. Administrador viendo tareas ajenas.**
> *Cómo obtenerla:* crear una tarea para otro usuario y capturar la etiqueta «Propietario» y los botones disponibles.

> **Figura 6. Perfil del usuario autenticado.**
> *Cómo obtenerla:* abrir «Mi Perfil» y capturar los datos mostrados.

> **Figura 7. Pruebas automatizadas en ejecución.**
> *Cómo obtenerla:* ejecutar `python manage.py test` y capturar la terminal con el resultado `Ran 16 tests ... OK`.

> **Figura 8. Interacción con la herramienta de IA.**
> *Cómo obtenerla:* capturar el chat del agente mostrando un prompt del informe y la respuesta generada.

> **Figura 9. Código generado y revisado.**
> *Cómo obtenerla:* capturar el diff o el fragmento final de `detalle_tarea` o `TareaSerializer`.

---

## 4. Conclusión

El desarrollo permitió obtener una aplicación funcional que cubre los requisitos planteados: registro y autenticación con JWT, gestión de tareas con permisos por propietario, panel de administración y gestión de tareas ajenas por parte del administrador. La incorporación de 16 pruebas automatizadas permitió verificar el comportamiento de los endpoints y detectar regresiones durante los cambios.

El uso de inteligencia artificial aportó velocidad en tareas como el análisis del repositorio, la generación de borradores de código y la escritura de pruebas. Sin embargo, también evidenció que el código generado debe revisarse con criterio: aparecieron problemas como un campo faltante en un serializador, una línea redundante que bloqueaba al administrador, riesgos de XSS y una condición de carrera en el frontend. Ninguno de esos problemas se habría detectado solo leyendo el código de forma superficial; fue necesario ejecutar comprobaciones y pruebas.

Las principales dificultades estuvieron relacionadas con el alcance del proyecto y con la matriz de permisos. Fue necesario acordar qué podía hacer cada rol sobre cada recurso y ajustar el backend para que esa lógica no dependiera del frontend. También fue importante distinguir entre «editar» una tarea y «cambiar su estado», ya que el administrador debía poder completar tareas ajenas sin modificar su contenido.

Los aprendizajes más relevantes fueron:

- La IA acelera el desarrollo, pero no reemplaza la revisión técnica ni las pruebas.
- Los prompts funcionan mejor cuando incluyen contexto, restricciones y criterios de aceptación.
- La seguridad debe implementarse en el backend; ocultar elementos en el HTML no es un control de acceso.
- Las pruebas automatizadas son la mejor red de seguridad frente a cambios generados por IA.
- Documentar las decisiones y las limitaciones es parte del trabajo, especialmente cuando se opta por una configuración académica en lugar de una de producción.

---

## 5. Referencias

- Django Software Foundation. *Django Documentation*. https://docs.djangoproject.com/
- Encode OSS Ltd. *Django REST Framework Documentation*. https://www.django-rest-framework.org/
- Jazzband. *djangorestframework-simplejwt Documentation*. https://django-rest-framework-simplejwt.readthedocs.io/
- OWASP Foundation. *OWASP Top 10*. https://owasp.org/www-project-top-ten/
- Mozilla Developer Network. *Fetch API*. https://developer.mozilla.org/es/docs/Web/API/Fetch_API
