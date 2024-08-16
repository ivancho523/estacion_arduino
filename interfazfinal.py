import paho.mqtt.client as mqtt
import psycopg2
from datetime import datetime
import streamlit as st
import pandas as pd
import plotly.graph_objs as go
import pytz

# Configuración de la base de datos PostgreSQL
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "datos_estacion"
DB_USER = "karen"
DB_PASSWORD = "12345"

# Obtener la zona horaria de Montevideo
timezone_Montevideo = pytz.timezone('America/Montevideo')

# Función para convertir la hora a la zona horaria de Montevideo
def convert_to_Montevideo_time(timestamp):
    utc_time = timestamp.replace(tzinfo=pytz.utc)  # Convertir a UTC
    Montevideo_time = utc_time.astimezone(timezone_Montevideo)  # Convertir a la zona horaria de Montevideo
    return Montevideo_time

def connect_db():
    try:
        connection = psycopg2.connect(
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME
        )
        return connection
    except (Exception, psycopg2.Error) as error:
        st.error(f"Error al conectar a la base de datos: {error}")
        return None

# Función para obtener los datos de la base de datos
def get_data():
    connection = None
    try:
        connection = connect_db()
        if connection is None:
            return pd.DataFrame()

        query = """
        SELECT fecha_hora, temperatura, humedad, dioxido_carbono, monoxido_carbono, ozono
        FROM lecturas_sensor
        ORDER BY fecha_hora DESC
        LIMIT 1000
        """
        df = pd.read_sql(query, connection)
        # Convertir la hora a la zona horaria de Montevideo
        df['fecha_hora'] = df['fecha_hora'].apply(convert_to_Montevideo_time)
        return df

    except (Exception, psycopg2.Error) as error:
        st.error(f"Error al obtener los datos de la base de datos: {error}")
        return pd.DataFrame()

    finally:
        if connection:
            connection.close()

# Configuración del cliente MQTT
mqtt_server = "165.227.126.203"
mqtt_port = 1883
mqtt_topic = "datos_estacion"

# Función que se ejecuta cuando se recibe un mensaje MQTT
def on_message(client, userdata, message):
    connection = None
    try:
        payload = message.payload.decode()
        print(f"Mensaje recibido: {payload}")

        # Separar los datos recibidos
        parts = payload.split(";")
        parts = [part for part in parts if part]  # Filtrar las partes vacías

        if len(parts) == 5:
            temperatura, humedad, ozono, monoxido_carbono, dioxido_carbono = map(float, parts)
            fecha_hora = datetime.now()

            # Establecer conexión a la base de datos
            connection = connect_db()
            if connection is None:
                print("Error al conectar a la base de datos")
                return

            cursor = connection.cursor()

            # Insertar datos en la base de datos
            cursor.execute("""
                INSERT INTO lecturas_sensor (fecha_hora, temperatura, humedad, ozono, monoxido_carbono, dioxido_carbono)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (fecha_hora, temperatura, humedad, ozono, monoxido_carbono, dioxido_carbono))

            # Confirmar la transacción y cerrar cursor y conexión
            connection.commit()
            cursor.close()

            print("Datos almacenados en la base de datos")

        else:
            print("Error: número incorrecto de datos recibidos")

    except Exception as e:
        print(f"Error al procesar el mensaje: {e}")

    finally:
        if connection:
            connection.close()

# Configuración del cliente MQTT
client = mqtt.Client()
client.on_message = on_message

client.connect(mqtt_server, mqtt_port, 60)
client.subscribe(mqtt_topic)

# Crear la aplicación Streamlit
st.title("Monitoreo de la calidad del aire en tiempo real")

# Obtener los datos de la base de datos
df = get_data()

# Crear pestañas para mostrar la tabla y los gráficos
tabs = st.tabs(["Tabla de Datos", "Gráfico General", "Temperatura y Humedad", "Dióxido de Carbono", "Monóxido de Carbono", "Ozono"])

# Mostrar los datos en una tabla en la primera pestaña
with tabs[0]:
    if not df.empty:
        st.write("Últimas 1000 lecturas:")
        st.write(df)
    else:
        st.write("No hay datos disponibles en la base de datos.")

# Mostrar los gráficos y resúmenes estadísticos en las pestañas correspondientes
if not df.empty:
    # Gráfico de todas las variables juntas
    with tabs[1]:
        fig_all = go.Figure()
        for column in df.columns[1:]:
            fig_all.add_trace(go.Scatter(x=df["fecha_hora"], y=df[column], mode='lines', name=column, connectgaps=False))

        fig_all.update_layout(title='Lecturas de Sensores (Todas las Variables)',
                              xaxis_title='Fecha y Hora',
                              yaxis_title='Valor',
                              xaxis=dict(
                                    rangeselector=dict(
                                            buttons=list([
                                                    dict(count=1, label="1 minuto", step="minute", stepmode="backward"),
                                                    dict(count=1, label="1 día", step="day", stepmode="backward"),
                                                    dict(count=7, label="1 semana", step="day", stepmode="backward"),
                                                    dict(count=1, label="1 mes", step="month", stepmode="backward"),
                                                    dict(count=3, label="3 meses", step="month", stepmode="backward"),
                                                    dict(count=1, label="Todo", step="all")
                                            ])
                                    ),
                                    rangeslider=dict(visible=True),
                                    type="date"),
                              yaxis=dict(fixedrange=False))
        st.plotly_chart(fig_all)
    # Gráfico de Temperatura y Humedad
    with tabs[2]:
        fig_temp_hum = go.Figure()
        fig_temp_hum.add_trace(go.Scatter(x=df["fecha_hora"], y=df["temperatura"], mode='lines', name='Temperatura', connectgaps=False))
        fig_temp_hum.add_trace(go.Scatter(x=df["fecha_hora"], y=df["humedad"], mode='lines', name='Humedad', connectgaps=False))

        fig_temp_hum.update_layout(title='Lecturas de Temperatura y Humedad',
                                   xaxis_title='Fecha y Hora',
                                   yaxis_title='Valor',
                                   xaxis=dict(
                                        rangeselector=dict(
                                                buttons=list([
                                                        dict(count=1, label="1 minuto", step="minute", stepmode="backward"),
                                                        dict(count=1, label="1 día", step="day", stepmode="backward"),
                                                        dict(count=7, label="1 semana", step="day", stepmode="backward"),
                                                        dict(count=1, label="1 mes", step="month", stepmode="backward"),
                                                        dict(count=3, label="3 meses", step="month", stepmode="backward"),
                                                        dict(count=1, label="Todo", step="all")
                                                ])
                                        ),
                                        rangeslider=dict(visible=True),
                                        type="date"),
                                   yaxis=dict(fixedrange=False))
        st.plotly_chart(fig_temp_hum)

        st.subheader("Resumen Estadístico de Temperatura")
        st.write(df['temperatura'].describe())

        st.subheader("Resumen Estadístico de Humedad")
        st.write(df['humedad'].describe())

    # Gráfico de Dióxido de Carbono
    with tabs[3]:
        fig_co2 = go.Figure()
        fig_co2.add_trace(go.Scatter(x=df["fecha_hora"], y=df["dioxido_carbono"], mode='lines', name='Dióxido de Carbono', connectgaps=False))

        fig_co2.update_layout(title='Lecturas de Dióxido de Carbono (CO2)',
                              xaxis_title='Fecha y Hora',
                              yaxis_title='ppm',
                              xaxis=dict(
                                    rangeselector=dict(
                                            buttons=list([
                                                    dict(count=1, label="1 minuto", step="minute", stepmode="backward"),
                                                    dict(count=1, label="1 día", step="day", stepmode="backward"),
                                                    dict(count=7, label="1 semana", step="day", stepmode="backward"),
                                                    dict(count=1, label="1 mes", step="month", stepmode="backward"),
                                                    dict(count=3, label="3 meses", step="month", stepmode="backward"),
                                                    dict(count=1, label="Todo", step="all")
                                            ])
                                    ),
                                    rangeslider=dict(visible=True),
                                    type="date"),
                              yaxis=dict(fixedrange=False))
        st.plotly_chart(fig_co2)

        st.subheader("Resumen Estadístico de Dióxido de Carbono")
        st.write(df['dioxido_carbono'].describe())

    # Gráfico de Monóxido de Carbono
    with tabs[4]:
        fig_co = go.Figure()
        fig_co.add_trace(go.Scatter(x=df["fecha_hora"], y=df["monoxido_carbono"], mode='lines', name='Monóxido de Carbono', connectgaps=False))

        fig_co.update_layout(title='Lecturas de Monóxido de Carbono (CO)',
                             xaxis_title='Fecha y Hora',
                             yaxis_title='ppm',
                             xaxis=dict(
                                    rangeselector=dict(
                                            buttons=list([
                                                    dict(count=1, label="1 minuto", step="minute", stepmode="backward"),
                                                    dict(count=1, label="1 día", step="day", stepmode="backward"),
                                                    dict(count=7, label="1 semana", step="day", stepmode="backward"),
                                                    dict(count=1, label="1 mes", step="month", stepmode="backward"),
                                                    dict(count=3, label="3 meses", step="month", stepmode="backward"),
                                                    dict(count=1, label="Todo", step="all")
                                            ])
                                    ),
                                    rangeslider=dict(visible=True),
                                    type="date"),
                             yaxis=dict(fixedrange=False))
        st.plotly_chart(fig_co)

        st.subheader("Resumen Estadístico de Monóxido de Carbono")
        st.write(df['monoxido_carbono'].describe())

    # Gráfico de Ozono
    with tabs[5]:
        fig_ozone = go.Figure()
        fig_ozone.add_trace(go.Scatter(x=df["fecha_hora"], y=df["ozono"], mode='lines', name='Ozono', connectgaps=False))

        fig_ozone.update_layout(title='Lecturas de Ozono',
                                xaxis_title='Fecha y Hora',
                                yaxis_title='ppb',
                                xaxis=dict(
                                    rangeselector=dict(
                                            buttons=list([
                                                    dict(count=1, label="1 minuto", step="minute", stepmode="backward"),
                                                    dict(count=1, label="1 día", step="day", stepmode="backward"),
                                                    dict(count=7, label="1 semana", step="day", stepmode="backward"),
                                                    dict(count=1, label="1 mes", step="month", stepmode="backward"),
                                                    dict(count=3, label="3 meses", step="month", stepmode="backward"),
                                                    dict(count=1, label="Todo", step="all")
                                            ])
                                    ),
                                    rangeslider=dict(visible=True),
                                    type="date"),
                                yaxis=dict(fixedrange=False))
        st.plotly_chart(fig_ozone)

        st.subheader("Resumen Estadístico de Ozono")
        st.write(df['ozono'].describe())

# Iniciar el cliente MQTT
client.loop_start()

# Recargar la página cada 60 segundos para obtener los nuevos datos
st.experimental_rerun()
st.experimental_sleep(60)
