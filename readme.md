# Repo proyecto Calidad de Aire -  Tesina

Este proyecto permite monitorear y visualizar datos de calidad del aire en tiempo real utilizando sensores conectados a un dispositivo Arduino, utiliza un ESP32 para recibir datos desde el Arduino a través de comunicación serial y enviarlos a un servidor MQTT. Los datos son almacenados en una base de datos PostgreSQL. La interfaz web interactiva se desarrolla con Streamlit para facilitar la visualización y el análisis de los datos.

**Configuración del Entorno**
Requisitos Previos
Python 3: Asegúrate de tener instalado Python 3 en tu sistema.

**Instalación de Bibliotecas:**

Ejecuta el siguiente comando para instalar las bibliotecas necesarias:
```bash
pip install streamlit psycopg2 pandas plotly pytz
```

**Configuración del Servidor y la Base de Datos**
Base de Datos PostgreSQL:
Configura y ejecuta una base de datos PostgreSQL en tu entorno local o en un servidor remoto.
Crea una base de datos llamada datos_estacion.

Define las credenciales de conexión en el archivo interfazfinal.py:
```bash
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "datos_estacion"
DB_USER = "tu_usuario"
DB_PASSWORD = "tu_contraseña"
```

**Ejecución de la Interfaz Web**
Descarga el Código:

**Clona este repositorio en tu máquina local:**
git clone https://github.com/tu_usuario/monitoreo-calidad-aire.git

**Ejecuta la Interfaz Web:**
Navega al directorio donde clonaste el repositorio:
```bash
cd monitoreo-calidad-aire
```
**Ejecuta la interfaz web con Streamlit:**
```bash
streamlit run interfazfinal.py
```
