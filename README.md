# Py-Wallet

## Descripción
Py-Wallet es una billetera digital diseñada para docentes de la UTPL. Su propósito es proporcionar una herramienta segura y accesible para realizar transacciones financieras básicas, gestionar cuentas de ahorro y visualizar reportes financieros.

Este proyecto fue desarrollado utilizando **Django** como framework backend, siguiendo el patrón de diseño **Model-View-Template (MVT)**. La interfaz de usuario fue construida con **Bootstrap**, garantizando una experiencia intuitiva y responsiva.

## Características Principales
- **Módulo de Usuarios**
  - Registro y autenticación de usuarios con Django Auth.
  - Gestión de perfiles y configuración de cuenta.
  - Validación de credenciales y recuperación de contraseñas.

- **Módulo de Wallets**
  - Creación y asociación de billeteras digitales a usuarios.
  - Consulta de saldo en tiempo real.
  - Seguridad en la gestión del balance con transacciones controladas.

- **Módulo de Transacciones**
  - Envío y recepción de dinero entre usuarios.
  - Registro detallado del historial de transacciones.
  - Validación estricta del saldo antes de procesar una transferencia.

## Tecnologías Utilizadas
- **Backend:** Python, Django
- **Frontend:** HTML5, CSS3, Bootstrap
- **Base de Datos:** MySQL
- **Control de Versiones:** Git & GitHub

## Instalación y Configuración
Para ejecutar Py-Wallet en un entorno local, sigue los siguientes pasos:

### 1. Clonar el repositorio
```sh
 git clone https://github.com/tu_usuario/pywallet.git
 cd caja-ahorros-utpl
```

### 2. Crear y activar un entorno virtual
```sh
 python -m venv venv
 source venv/bin/activate  # En Linux/macOS
 venv\Scripts\activate  # En Windows
```

### 3. Instalar las dependencias
```sh
 pip install -r requirements.txt
```

### 4. Configurar la base de datos
Asegúrate de que **MySQL** esté instalado y configurado. Luego, en el archivo `settings.py`, ajusta la conexión con la base de datos:
```python
 DATABASES = {
     'default': {
         'ENGINE': 'django.db.backends.mysql',
         'NAME': 'pywallet_db',
         'USER': 'tu_usuario_mysql',
         'PASSWORD': 'tu_contraseña',
         'HOST': 'localhost',
         'PORT': '3306',
     }
 }
```

Ejecuta las migraciones:
```sh
 python manage.py makemigrations
 python manage.py migrate
```

### 5. Crear un superusuario (opcional)
Para acceder al panel de administración de Django, crea un superusuario:
```sh
 python manage.py createsuperuser
```

### 6. Ejecutar el servidor local
```sh
 python manage.py runserver
```
Accede a la aplicación en tu navegador en `http://127.0.0.1:8000/`

## Uso de la Aplicación
- **Registro y autenticación:** Los usuarios pueden registrarse y autenticarse en la plataforma para acceder a sus billeteras.
- **Gestión de billeteras:** Cada usuario tiene una billetera asociada donde puede consultar su saldo y gestionar transacciones.
- **Transferencias seguras:** Los usuarios pueden realizar transacciones entre sí de forma rápida y segura.
- **Panel de administración:** Accede al panel administrativo en `http://127.0.0.1:8000/admin/` para gestionar usuarios y transacciones.

## Contribución
Si deseas contribuir a este proyecto:
1. Haz un fork del repositorio.
2. Crea una nueva rama con tu funcionalidad (`git checkout -b feature/nueva_funcionalidad`).
3. Realiza tus cambios y haz commit (`git commit -m 'Añadir nueva funcionalidad'`).
4. Envía un pull request.

## Licencia
Este proyecto está bajo la licencia **MIT**. Puedes ver más detalles en el archivo `LICENSE`.

---
