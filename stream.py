import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt

# Configurar la URL base de la API
API_URL = "http://localhost:5100/hobbies/get-activity-log/"

# Título de la aplicación
st.title("Visualización de Datos de Actividades")

# Realizar una solicitud GET a la API para obtener los datos
response = requests.get(API_URL)
if response.status_code == 200:
    data = response.json()
    # Convertir los datos a un DataFrame de pandas
    df = pd.DataFrame(data)
    
    # Mostrar el DataFrame en la aplicación Streamlit
    st.write("Datos obtenidos de la API:")
    st.write(df)
    
    # Crear una visualización simple usando Matplotlib
    st.write("Gráfico de Calificaciones por Fecha:")
    fig, ax = plt.subplots()
    df['date'] = pd.to_datetime(df['date'])  # Asegúrate de que la columna de fechas esté en formato datetime
    df = df.sort_values('date')  # Ordenar por fecha
    ax.plot(df['date'], df['rating'], marker='o')
    ax.set_xlabel('Fecha')
    ax.set_ylabel('Calificación')
    ax.set_title('Calificaciones a lo largo del tiempo')
    st.pyplot(fig)
else:
    st.error("Error al obtener datos de la API")
