# Crear contenedor en el pc en el docker 
docker-compose up --build
# CasaMobler - Sistema de Gestión Inmobiliaria

Sistema de gestión inmobiliaria desarrollado en **Django** con interfaz moderna, autenticación de usuarios, gestión de pedidos, remisiones y generación de PDFs.

---

## 🚀 Características

- Autenticación de usuarios con roles
- Gestión de clientes, productos y pedidos
- Generación de remisiones en PDF (con `reportlab`)
- Interfaz moderna con Bootstrap 5 y tema "Soft UI Dashboard"
- Compatible con Docker

---

## 🛠️ Requisitos previos

- [Python 3.9+](https://www.python.org/)
- [Docker](https://www.docker.com/) y [Docker Compose](https://docs.docker.com/compose/)
- (Opcional) `virtualenv` si no usas Docker

---

## 📦 Instalación local (sin Docker)

1. **Clonar el repositorio**
   ```bash
   git clone https://github.com/tu-usuario/casamobler.git
   cd casamobler

python -m venv venv
source venv/bin/activate        # Linux/Mac
# o
venv\Scripts\activate           # Windows

pip install -r requirements.txt

python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
   ```

2. **Configurar el servidor**

   - Abrir el archivo `settings.py` y modificar las siguientes variables:

     ```python
     DATABASES = {
         'default': {
             'ENGINE': 'django.db.backends.sqlite3',
             'NAME': BASE_DIR / 'db.sqlite3',
         }
     }
     ```

   - Crear un archivo `db.sqlite3` en la carpeta `c:/Users/tu_usuario/Downloads/RAELG/`
   - Abrir la terminal y ejecutar los siguientes comandos:

     ```bash
     cd c:/Users/tu_usuario/Downloads/RAELG/
     python manage.py migrate
     python manage.py createsuperuser
     python manage.py runserver
     ```

---

## 📦 Instalación con Docker

1. **Clonar el repositorio**

   ```bash
   git clone https://github.com/tu-usuario/casamobler.git
   cd casamobler
   ```

2. **Crear un archivo `docker-compose.yml`**

   ```yaml
   version: '3.8'

   services:
     app:
       build: .
       command: python manage.py runserver 0.0.0.0:8000
       volumes:
         - .:/code
       ports:
         - "8000:8000"
   ```

3. **Crear un archivo `Dockerfile`**

   ```dockerfile
   FROM python:3.9-slim-buster

   ENV PYTHONUNBUFFERED 1

   RUN mkdir /code
   WORKDIR /code

   COPY requirements.txt /code/
   RUN pip install -r requirements.txt

   COPY . /code/
   ```

4. **Crear un archivo `requirements.txt`**

   ```txt
   Django
   reportlab==4.2.5
   ```

5. **Ejecutar los comandos**

   ```bash
   docker-compose up --build
   ```

---

## 📝 Licencia

Este proyecto está licenciado bajo la licencia MIT. Consulta el archivo [LICENSE](LICENSE) para más detalles.    

---

## 📄 Autor

👤 **Carlos Giraldo**

