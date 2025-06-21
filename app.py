import streamlit as st
import requests
import openai
import time

# Leer claves desde secrets.toml
openai.api_key = st.secrets["OPENAI_API_KEY"]
DEEPSEEK_API_KEY = st.secrets["DEEPSEEK_API_KEY"]

DEEPSEEK_URL = "https://api.deepseek.com/v1/chat/completions"
HEADERS_DEEPSEEK = {
    "Authorization": f"Bearer " + DEEPSEEK_API_KEY,
    "Content-Type": "application/json"
}

# Función para GPT (OpenAI)
def call_openai(messages):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Puedes usar "gpt-4" si tienes acceso
            messages=messages,
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"Error con OpenAI: {e}")
        return "Error"

# Función para DeepSeek
def call_deepseek(messages):
    try:
        payload = {
            "model": "deepseek-chat",
            "messages": messages,
            "temperature": 0.7
        }
        response = requests.post(DEEPSEEK_URL, headers=HEADERS_DEEPSEEK, json=payload)
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        st.error(f"Error con DeepSeek: {e}")
        return "Error"

# Interfaz de usuario
st.title("🤖 Self-chat entre GPT y DeepSeek")
start_message = st.text_input("Frase inicial", "Hola, ¿cómo estás?")

if st.button("Iniciar conversación"):
    messages = [{"role": "user", "content": start_message}]
    st.session_state.chat_log = []
    turno = "openai"

    for i in range(10):  # puedes cambiar a más rondas
        if turno == "openai":
            respuesta = call_openai(messages)
            speaker = "🧠 GPT (OpenAI)"
        else:
            respuesta = call_deepseek(messages)
            speaker = "🔬 DeepSeek"

        messages.append({"role": "assistant", "content": respuesta})
        st.session_state.chat_log.append((speaker, respuesta))

        # La respuesta será la próxima pregunta
        messages.append({"role": "user", "content": respuesta})
        turno = "deepseek" if turno == "openai" else "openai"
        time.sleep(1)

    for speaker, texto in st.session_state.chat_log:
        st.markdown(f"**{speaker}:** {texto}")
