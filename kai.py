import os
import time
import tempfile
import datetime
import webbrowser
import speech_recognition as sr
from gtts import gTTS
import google.generativeai as genai

# ===== CONFIGURACAO DA GEMINI =====
genai.configure(api_key="AIzaSyAZc0OWiQR3ICPjXDoKX8seHTJk-Vqa6VY") 
model = genai.GenerativeModel("gemini-1.5-pro")

# ===== FUNCAO DE VOZ COM gTTS =====
def speak(text):
    print(f"Kai: {text}")
    with tempfile.NamedTemporaryFile(delete=True, suffix=".mp3") as fp:
        tts = gTTS(text=text, lang='pt-br', slow=False)
        tts.save(fp.name)
        os.system(f"mpg123 -q {fp.name}")
        time.sleep(0.3)

# ===== ESCUTA COMANDO DE VOZ =====
def ouvir_comando():
    recognizer = sr.Recognizer()
    mic = sr.Microphone(device_index=1)  # Ajuste o index conforme seu microfone
    with mic as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print("🎤 Ouvindo... (diga algo com 'Kai')")
        audio = recognizer.listen(source, timeout=5, phrase_time_limit=8)
    try:
        comando = recognizer.recognize_google(audio, language='pt-BR')
        print(f"Você disse: {comando}")
        return comando.lower()
    except sr.UnknownValueError:
        speak("Desculpe, não entendi.")
    except sr.RequestError:
        speak("Problema ao acessar o serviço de voz.")
    except sr.WaitTimeoutError:
        print("[⚠️] Nenhuma fala detectada.")
    return ""

# ===== GEMINI - INTERPRETADOR DE COMANDOS =====
def interpretar_comando(pergunta):
    try:
        resposta = model.generate_content(pergunta)
        return resposta.text.strip()
    except Exception as e:
        print(f"[Erro Gemini]: {e}")
        return "Tive um problema ao processar isso."

# ===== EXECUTA AÇÕES PADRÕES =====
def executar_comando(comando):
    if "horas" in comando:
        agora = datetime.datetime.now().strftime("%H:%M")
        speak(f"Agora são {agora}")
    elif "abrir google" in comando:
        speak("Abrindo o Google.")
        webbrowser.open("https://www.google.com")
    elif "tocar música" in comando:
        speak("Tocando uma música.")
        webbrowser.open("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    elif "sair" in comando or "encerrar" in comando:
        speak("Encerrando. Até logo!")
        exit()
    else:
        resposta = interpretar_comando(comando)
        speak(resposta)

# ===== BOAS-VINDAS =====
speak("Olá, eu sou a Kai. Estou pronta pra te ajudar.")

# ===== LOOP PRINCIPAL =====
while True:
    try:
        comando = ouvir_comando()
        if "kai" in comando:
            executar_comando(comando)
    except KeyboardInterrupt:
        speak("Encerrando por aqui. Até mais!")
        break
    except Exception as e:
        print(f"[ERRO FATAL]: {e}")
        speak("Algo deu errado. Pode repetir?")
