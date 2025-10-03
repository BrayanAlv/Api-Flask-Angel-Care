# API de AngelCare con Flask y MySQL

Esta es una API RESTful construida con Flask y MySQL para gestionar guarderías, usuarios, y dispositivos de monitoreo. La API utiliza JWT para la autenticación y está documentada con Swagger.

---
## 📋 Prerrequisitos

Antes de comenzar, asegúrate de tener instalado el siguiente software en tu sistema Windows:

1.  **Python (versión 3.8 o superior)**
    * Puedes descargarlo desde la [página oficial de Python](https://www.python.org/downloads/windows/).
    * **Importante:** Durante la instalación, asegúrate de marcar la casilla que dice **"Add Python to PATH"**.

2.  **MySQL Server**
    * Se recomienda instalarlo usando el [MySQL Installer for Windows](https://dev.mysql.com/downloads/installer/).
    * Durante la instalación, guardarás la contraseña de `root` o crearás un nuevo usuario, que necesitarás más adelante.

3.  **Git**
    * Necesario para clonar el repositorio. Descárgalo desde [Git for Windows](https://git-scm.com/download/win).

---
## Instalación

Sigue estos pasos en una terminal de Windows (ya sea `cmd` o `PowerShell`).

1.  **Clona el repositorio:**
    ```bash
    git clone https://github.com/BrayanAlv/Api-Flask-Angel-Care.git
    cd Api-Flask-Angel-Care
    ```

2.  **Crea un entorno virtual:**
    Un entorno virtual aísla las dependencias de tu proyecto.
    ```bash
    python -m venv venv
    ```

3.  **Activa el entorno virtual:**
    Este es el paso clave en Windows. Deberás ver `(venv)` al inicio de la línea de tu terminal.
    ```powershell
    .\venv\Scripts\activate
    ```

4.  **Instala las dependencias:**
    Este comando leerá el archivo `requirements.txt` e instalará todas las librerías necesarias.
    ```bash
    pip install -r requirements.txt
    ```

---
## Configuración

La configuración del proyecto se maneja a través de un archivo de variables de entorno.

1.  **Crea el archivo `.env`:**
    En la raíz del proyecto, crea un nuevo archivo llamado `.env`.

2.  **Añade las variables de entorno:**
    Copia y pega el siguiente contenido en tu archivo `.env` y **reemplaza los valores** con tus propias credenciales.

    ```ini
    # Configuración de la Base de Datos
    DB_HOST=localhost
    DB_USER=root
    DB_PASSWORD=tu_contraseña_de_mysql
    DB_NAME=nombre_de_tu_base_de_datos

    # Clave secreta para firmar los JWT (JSON Web Tokens)
    # ¡Usa una cadena de texto larga, compleja y aleatoria!
    JWT_SECRET_KEY=esta-es-una-clave-muy-secreta-y-debes-cambiarla
    ```

3.  **Configura la Base de Datos:**
    * Asegúrate de que tu servidor MySQL esté corriendo.
    * Crea una base de datos con el nombre que especificaste en `DB_NAME`.
    * Importa el archivo `.sql` con la estructura de las tablas en tu base de datos. Si tu script se llama `schema.sql`, puedes usar un cliente de MySQL o el siguiente comando:
    ```bash
    mysql -u root -p
    create database angelcare;
    exit 
    # Una vez creada la base de datos se puede importar el schema
    mysql -u root -p angelcare < angelcareV1.sql
    ```

---
## Ejecución

Una vez que todo está instalado y configurado, puedes iniciar la API.

1.  **Asegúrate de que tu entorno virtual `(venv)` esté activado.**

2.  **Inicia el servidor de Flask:**
    ```bash
    python app.py
    ```

3.  Si todo va bien, verás un mensaje de confirmación y el servidor estará corriendo:
    ```
    Pool de conexiones creado exitosamente.
     * Running on [http://12.0.0.1:5000](http://12.0.0.1:5000)
    ```

---
## 📚 Uso de la API

La API cuenta con una interfaz de documentación interactiva gracias a Swagger.

1.  **Abre tu navegador web** y ve a la siguiente dirección:
    [http://127.0.0.1:5000/apidocs](http://127.0.0.1:5000/apidocs)

2.  **Autenticación con JWT:**
    * Primero, ve al endpoint `POST /api/login` en la sección de `Auth`.
    * user: admin  pw: admin123
    * Usa el botón "Try it out" para enviar un `username` y `password` de un usuario que ya exista en tu base de datos.
    * Copia el `access_token` que recibas en la respuesta.

3.  **Probar rutas protegidas:**
    * En la parte superior derecha de la página de Swagger, haz clic en el botón **"Authorize"**.
    * En la ventana que aparece, escribe `Bearer ` (con un espacio al final) y pega el `access_token` que copiaste. Ejemplo: `Bearer eyJhbGciOiJIUzI1Ni...`
    * ¡Listo! Ahora puedes probar cualquier endpoint protegido (como `POST`, `PUT`, `DELETE`) directamente desde la documentación.