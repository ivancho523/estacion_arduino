# Repo proyecto Calidad de Aire -  Tesina

Este proyecto permite monitorear y visualizar datos de calidad del aire en tiempo real utilizando sensores conectados a un dispositivo Arduino, utiliza un ESP32 para recibir datos desde el Arduino a través de comunicación serial y enviarlos a un servidor MQTT. Los datos son almacenados en una base de datos PostgreSQL. La interfaz web interactiva se desarrolla con Streamlit para facilitar la visualización y el análisis de los datos.

**Configuración del Entorno**

Requisitos Previos

Python 3: Asegúrate de tener instalado Python 3 en tu sistema.


## Instrucciones para Replicar el Proyecto

### Paso 1: Clonar el Repositorio

1. **Clona este repositorio en tu máquina local:**

   Abre tu terminal y ejecuta el siguiente comando para clonar el repositorio desde GitHub:

   ```bash
   git clone https://github.com/ivancho523/estacion_arduino.git
   ```

   Esto creará una copia local del repositorio en tu directorio actual.

### Paso 2: Crear un Entorno Virtual

2. **Crea un entorno virtual:**

   Es recomendable utilizar un entorno virtual para gestionar las dependencias del proyecto. Para crear un entorno virtual, navega hasta el directorio del proyecto clonado y ejecuta los siguientes comandos:

   ```bash
   cd estacion_arduino
   python -m venv entorno
   ```

   Esto creará un directorio llamado `entorno` en tu proyecto.
   
En Linux:

     ```bash
     source entorno/bin/activate
     ```


### Paso 3: Configuración del Servidor MQTT con Mosquitto

#### Instalación

1. **Actualizar los paquetes del sistema:**

   ```bash
   sudo apt-get update

**Instalar Mosquitto y Mosquitto Clients:**
```bash
    sudo apt-get install mosquitto mosquitto-clients
```

**Configuración**

Habilitar Mosquitto como servicio:
```bash
    sudo systemctl enable mosquitto
```
**Iniciar el servicio Mosquitto:**
```bash
    sudo systemctl start mosquitto
```
**Verificación**

Para verificar que Mosquitto está funcionando correctamente, puedes ejecutar los siguientes comandos:

Verificar el estado de Mosquitto:
```bash
    sudo systemctl status mosquitto
```

### Paso 4: Configuración de la Base de Datos PostgreSQL

**Instalación**

1. **Actualizar los paquetes del sistema:**

   ```bash
   sudo apt-get update

**Instalar PostgreSQL y PostgreSQL Client:**
   ```bash
sudo apt-get install postgresql postgresql-client
   ```

Conectarse a la base de datos y crear la tabla necesaria en PostgreSQL:

#### Configuración Inicial

1. **Iniciar el servidor PostgreSQL:**

   ```bash
   sudo service postgresql start
   ```

2. **Acceder a la consola de PostgreSQL como usuario `postgres`:**

   ```bash
   sudo -u postgres psql
   ```

3. **Crear una nueva contraseña para el usuario `postgres`:**

   ```sql
   ALTER USER postgres WITH PASSWORD 'tucontraseña';
   ```

   Reemplaza `tucontraseña` con la contraseña deseada.

4. **Salir de la consola de PostgreSQL:**

   ```sql
   \q
   ```

#### Creación de una Base de Datos y Usuario

1. **Acceder nuevamente a la consola de PostgreSQL como usuario `postgres`:**

   ```bash
   sudo -u postgres psql
   ```

2. **Crear una nueva base de datos y un nuevo usuario:**

   ```sql
   CREATE DATABASE datos_estacion;
   CREATE USER karen WITH ENCRYPTED PASSWORD 'tucontraseña';
   GRANT ALL PRIVILEGES ON DATABASE datos_estacion TO usuario;
   ```

Aquí, `datos_estacion` es el nombre de la base de datos y `usuario` es el nombre de usuario con privilegios para acceder y manipular la base de datos.

3. **Conectarse a la base de datos `datos_estacion`:**

   ```sql
   \c datos_estacion
   ```

4. **Crear una tabla para almacenar las lecturas del sensor:**

   ```sql
   CREATE TABLE lecturas_sensor (
       fecha_hora TIMESTAMP,
       temperatura NUMERIC,
       humedad NUMERIC,
       dioxido_carbono NUMERIC,
       monoxido_carbono NUMERIC,
       ozono NUMERIC
   );
   ```

Esta tabla almacenará los datos de temperatura, humedad, dióxido de carbono, monóxido de carbono y ozono junto con su fecha y hora correspondiente.

5. **Salir de la consola de PostgreSQL:**

   ```sql
   \q
   ```

#### Verificación

Para verificar que PostgreSQL está instalado y configurado correctamente, puedes realizar las siguientes acciones:

- **Iniciar sesión en PostgreSQL como usuario creado:**

  ```bash
  psql -h localhost -U usuario datos_estacion
  ```

  Se te solicitará que ingreses la contraseña que estableciste para el usuario `karen`.

- **Verificar la estructura de la tabla:**

  ```sql
  \d lecturas_sensor
  ```

  Deberías ver la estructura de la tabla `lecturas_sensor` listada.

- **Salir de la consola de PostgreSQL:**

  ```sql
  \q
  ```

### Paso 5: Ejecución de la Interfaz Gráfica

**Instalación de Dependencias**

Instala las dependencias necesarias:
```bash
pip install streamlit pandas plotly pytz
```
**Ejecuta la interfaz gráfica:**

Una vez que todas las dependencias estén instaladas y la base de datos esté configurada correctamente, puedes ejecutar la interfaz gráfica utilizando Streamlit. 

Navega al directorio donde clonaste el repositorio:

```bash
cd monitoreo-calidad-aire
```

**Ejecuta la interfaz web con Streamlit:**

```bash
streamlit run interfazfinal.py
```
### Información del Servidor

El servidor utilizado para este proyecto tiene la siguiente configuración:

```plaintext
 Ubuntu 24.04 LTS
```






