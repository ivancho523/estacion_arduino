# Repo proyecto Calidad de Aire -  Tesina

Este proyecto permite monitorear y visualizar datos de calidad del aire en tiempo real utilizando sensores conectados a un dispositivo Arduino, utiliza un ESP32 para recibir datos desde el Arduino a través de comunicación serial y enviarlos a un servidor MQTT. Los datos son almacenados en una base de datos PostgreSQL. La interfaz web interactiva se desarrolla con Streamlit para facilitar la visualización y el análisis de los datos.

**Configuración del Entorno**

Requisitos Previos

Python 3: Asegúrate de tener instalado Python 3 en tu sistema.

### Servidor MQTT (Mosquitto)

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

### Base de Datos PostgreSQL

**Instalación**

1. **Actualizar los paquetes del sistema:**

   ```bash
   sudo apt-get update

**Instalar PostgreSQL y PostgreSQL Client:**
   ```bash
sudo apt-get install postgresql postgresql-client
   ```

Para incluir instrucciones sobre cómo descargar e iniciar PostgreSQL en tu README de GitHub, sigue estos pasos:

Conectarse a la base de datos y crear la tabla necesaria en PostgreSQL:

### Base de Datos PostgreSQL

**Instalación**

1. **Actualizar los paquetes del sistema:**

   ```bash
   sudo apt-get update
   ```

2. **Instalar PostgreSQL y PostgreSQL Client:**

   ```bash
   sudo apt-get install postgresql postgresql-client
   ```

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
   ALTER USER postgres WITH PASSWORD 'tu_nueva_contraseña';
   ```

   Reemplaza `tu_nueva_contraseña` con la contraseña deseada.

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
   CREATE USER karen WITH ENCRYPTED PASSWORD '12345';
   GRANT ALL PRIVILEGES ON DATABASE datos_estacion TO karen;
   ```

Aquí, `datos_estacion` es el nombre de la base de datos y `karen` es el nombre de usuario con privilegios para acceder y manipular la base de datos.

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
  psql -h localhost -U karen datos_estacion
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

**Ejecución de la Interfaz Web**

Descarga el Código:

**Paso 1: Clonar el Repositorio**

Clona este repositorio en tu máquina local:

Abre tu terminal y ejecuta el siguiente comando para clonar el repositorio desde GitHub:

```bash
git clone https://github.com/tu_usuario/monitoreo-calidad-aire.git
```
Esto creará una copia local del repositorio en tu directorio actual.

**Paso 2: Instalación de Dependencias**

Instala las dependencias necesarias:

Desde la raíz del repositorio clonado, instala las bibliotecas Python requeridas ejecutando:

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
