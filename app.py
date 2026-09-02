import streamlit as st
from google import genai
from datetime import date

# Cliente moderno con tu API key
client = genai.Client(api_key="AQ.Ab8RN6KujP4ma5SacCmWm009IJF32R7e3oKpXK3fhGZjxn6XZA")

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
            
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt,
            )
            
            st.success("¡Análisis listo!")
            st.subheader(f"Resumen para: {equipo_local} vs {equipo_visitante} ({fecha_partido})")
            st.markdown(response.text)
            
        except Exception as e:
            st.error(f"Ocurrió un error al conectar con la IA. Detalle: {e}")
