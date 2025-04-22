import speech_recognition as sr
import pyttsx3
import time

# Inicializa o mecanismo de fala
engine = pyttsx3.init()

# Configura voz feminina (se disponível)
voices = engine.getProperty('voices')
for voice in voices:
    if "female" in voice.name.lower() or "feminina" in voice.name.lower():
        engine.setProperty('voice', voice.id)
        break

# Configura fala mais suave
engine.setProperty('rate', 130)  # Velocidade mais lenta
engine.setProperty('volume', 1.0)

def speak(text, pausa=0.8):
    frases = text.split('.')
    for frase in frases:
        frase = frase.strip()
        if frase:
            print(f"Kai: {frase}")
            engine.say(frase)
            engine.runAndWait()
            time.sleep(pausa)  # Pausa entre frases

# Inicializa o reconhecedor de voz
recognizer = sr.Recognizer()

def ouvir_comando():
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print("🎤 Ouvindo... (diga algo com 'Kai')")
        audio = recognizer.listen(source)
    try:
        comando = recognizer.recognize_google(audio, language="pt-BR")
        comando = comando.lower()
        print(f"Você disse: {comando}")
        return comando
    except sr.UnknownValueError:
        speak("Desculpe. Eu não entendi o que você disse.")
    except sr.RequestError:
        speak("Tive um problema ao acessar o serviço de voz.")
    return ""

# Loop principal
if __name__ == "__main__":
    speak("Olá. Eu sou a Kai.", pausa=1.2)
    speak("Estou pronta para te ajudar. É só me chamar.", pausa=1.2)

    while True:
        try:
            comando = ouvir_comando()
            if "kai" in comando:
                resposta = f"Você me chamou. E disse: {comando}"
                speak(resposta)
        except KeyboardInterrupt:
            speak("Até a próxima. Foi bom falar com você!")
            break
        except Exception as e:
            print(f"[Erro]: {e}")
            speak("Ocorreu um erro inesperado.")
