import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
from instructions import SYSTEM_INSTRUCTIONS

# Load environment variables
load_dotenv()

# Configure API key securely
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)

# Configure the model
model = genai.GenerativeModel('gemini-pro')

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []
    try:
        context = "Inicio de la conversación"
        initial_prompt = SYSTEM_INSTRUCTIONS.format(
            context=context, 
            question="Saludo inicial"
        )
        st.session_state.chat = model.start_chat(history=[])
        st.session_state.chat.send_message(initial_prompt)
    except Exception as e:
        st.error(f"Error al inicializar el chat: {str(e)}")
        st.stop()

st.title("Radio Lira 88.7 FM - Asistente Virtual")

# Muestra el historial de mensajes
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input del usuario
if prompt := st.chat_input("Escribe tu mensaje aquí"):
    # Agrega mensaje del usuario al historial
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Genera respuesta
    with st.chat_message("assistant"):
        context = "Conversación en curso"
        full_prompt = SYSTEM_INSTRUCTIONS.format(context=context, question=prompt)
        response = st.session_state.chat.send_message(full_prompt)
        st.markdown(response.text)
        
    # Agrega respuesta al historial
    st.session_state.messages.append({"role": "assistant", "content": response.text})
