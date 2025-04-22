import speech_recognition as sr
import pyttsx3
import datetime

audio = sr.Recognizer()
machine = pyttsx3.init()
# machine.say('Opa, eu sou a Kai')
# machine.say('como posso')
# machine.runAndWait()

def command_execut():
    try:
        with sr.Microphone() as source:
            print('Ouvindo...')
            voice = audio.listen(source)
            command = audio.recognizer_google(voice, language='pt-BR')
            command = command.lower()
            if 'kai' in command:
                # print(command)
                command = command.replace('kai', '')
                machine.say(command)
                machine.runAndWait()
    except:
        print('Erro ao escutar, fale novamente!')
    return command

    def user_command_voice():
        command = command_execut()
    