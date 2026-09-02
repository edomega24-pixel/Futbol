import streamlit as st
import requests
import json
from datetime import date

# Configuración de tu clave actual
API_KEY = "AQ.Ab8RN6KQjG98rDHVXz-qCGRG4zyfnMXvUecDhn2Rtv9F1wxcdw"

st.set_page_config(page_title="Apuestas Claras y Rápidas", layout="centered")

st.title("⚽ Pronósticos Directos al Grano")
st.markdown("Sin rodeos: ¿Quién gana, cuántos goles habrá y listo.")

with st.form("match_form"):
    col1, col2 = st.columns(2)
    with col1:
        equipo_local = st.text_input("Equipo Local", "Deportivo Pasto")
    with col2:
        equipo_visitante = st.text_input("Equipo Visitante", "Deportivo Pereira")
        
    fecha_partido = st.date_input("Fecha del Partido", value=date.today())
    
    stats_local = st.text_area("Estadísticas Local", "Últimos 5: 2 ganados, 2 empatados. Prom. gol: 1.2")
    stats_visitante = st.text_area("Estadísticas Visitante", "Últimos 5: 1 ganado, 3 empatados. Prom. gol: 1.0")
    
    contexto = st.text_area("Noticias / Lesiones", "Partido clave de la liga local.")
    
    submitted = st.form_submit_button("Obtener Veredicto Directo")

if submitted:
    with st.spinner("Calculando pronóstico directo..."):
        try:
            prompt = f"""
            Actúa como un tipster profesional de apuestas de fútbol ultra directo. 
            Analiza el partido del día {fecha_partido} entre {equipo_local} (Local) y {equipo_visitante} (Visitante).
            
            - Local: {stats_local}
            - Visitante: {stats_visitante}
            - Contexto: {contexto}
            
            NO redactes textos largos ni explicaciones técnicas complejas. Entrega la respuesta exactamente bajo este formato resumido:
            
            🏆 **Ganador Probable:** [Indica quién gana o si hay alta probabilidad de empate]
            📊 **Probabilidades:** [Local X% - Empate X% - Visitante X%]
            ⚽ **Número de Goles:** [Ejemplo: Menos de 2.5 goles / Rango de 1 a 2 goles]
            🎯 **Apuesta Recomendada:** [Una sola recomendación contundente y clara]
            """
            
            # URL del endpoint oficial de Gemini para gemini-3.6-flash
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.6-flash:generateContent?key={API_KEY}"
            
            headers = {
                'Content-Type': 'application/json'
            }
            
            payload = {
                "contents": [{
                    "parts": [{"text": prompt}]
                }]
            }
            
            # Petición HTTP directa que salta cualquier restricción del SDK
            response = requests.post(url, headers=headers, data=json.dumps(payload))
            result = response.json()
            
            if response.status_code == 200:
                # Extraer el texto de la respuesta estructurada de la API
                texto_respuesta = result["candidates"][0]["content"]["parts"][0]["text"]
                st.success("¡Análisis listo!")
                st.subheader(f"Resumen para: {equipo_local} vs {equipo_visitante} ({fecha_partido})")
                st.markdown(texto_respuesta)
            else:
                st.error(f"Error de la API ({response.status_code}): {result}")
                
        except Exception as e:
            st.error(f"Ocurrió un error al procesar la solicitud: {e}")
