import pyttsx3
import speech_recognition as sr
import streamlit as st

class Echo_bot:
    def __init__(self):
        self.speaker = pyttsx3.init()
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.voices = self.speaker.getProperty('voices')
        self.selected_voice_index = 2  # Індекс вибраного голосу
        self.speaker.setProperty('voice', self.voices[self.selected_voice_index].id)
        self.volume = 1.0  # Гучність голосу
        self.speed = 150    # Швидкiсть голосу
        self.output_mode = 1 # виведення голосом за умовчуванням

    def set_voice(self, voice_index):
        if 0 <= voice_index < len(self.voices):
            self.selected_voice_index = voice_index
            self.speaker.setProperty('voice', self.voices[voice_index].id)
        else:
            st.write("Невiрний iндекс голосу")

    def set_volume(self, volume_level):
        if 0.0 <= volume_level <= 1.0:
            self.volume = volume_level
            self.speaker.setProperty('volume', volume_level)
        else:
            st.write("Невiрний рiвень гучностi")

    def set_speed(self, speed):
        self.speed = speed
        self.speaker.setProperty('rate', speed)

    def set_output_mode(self, output_mode):
        if 1 <= output_mode <= 3:
            self.output_mode = output_mode
        else:
            st.write("Мод виведення встановлено неправильно! Значення має бути від 1 до 3")

    def listen_for_input(self):
        with self.microphone as source:
            audio = self.recognizer.record(source, duration=3)
        try:
            user_input = self.recognizer.recognize_google(audio, language="uk-UA")
            return user_input
        except sr.UnknownValueError:
            st.write("Не розпiзнано")
            return " "

    def convert(self, text: str, filename: str = "hello.mp3"):
        self.speaker.save_to_file(text, filename)
        self.speaker.runAndWait()

    def output(self, text):
        if self.output_mode==1:
            self.convert(text=text)
            with open('hello.mp3', 'rb') as audio_file:
                audio_bytes = audio_file.read()
            st.audio(audio_bytes, format='audio/mp3')
        elif self.output_mode==2:
            if text == None:
                text = "Hello!"
            st.write("Бот: " + text)
        elif self.output_mode==3:
            st.write("Бот: " + text)
            self.convert(text=text)
            with open('hello.mp3', 'rb') as audio_file:
                audio_bytes = audio_file.read()
            st.audio(audio_bytes, format='audio/mp3')

    def run(self):
        while True:
            col1, col2 = st.columns(2)

            with col2:
                input_in = st.radio("Введення здійснити: 👇", ["голосом", "текстом", "голосом та текстом"])

                input = st.radio( "Виведення здійснити: 👇", ["голосом", "текстом", "голосом та текстом"] )
                if input == "голосом":
                    self.set_output_mode(1)
                elif input == "текстом":
                    self.set_output_mode(2)
                else:
                    self.set_output_mode(3)

                if input != "текстом":
                    speed = st.slider('Встановити швидкість: 👇', 0, 1000, 150)
                    self.set_speed(speed)

                    volume_level = st.slider('Встановити гучність: 👇', 0.0, 1.0, 1.0)
                    self.set_volume(volume_level)

                    voice = st.radio("Встановити голос: 👇", ["Natalia :woman:", "Anatol :man:", "Zira :woman: (English)"])
                    if voice=="Natalia :woman:":
                        voice_index=3
                    elif voice=="Anatol :man:":
                        voice_index=2
                    else:
                        voice_index=1
                    self.set_voice(voice_index)

            with col1:
                if input_in == "голосом":
                    if st.button('Натисніть для прослуховування'):
                        user_input = self.listen_for_input()
                elif input_in == "текстом":
                    user_input = st.chat_input("Введіть текст: ")
                else:
                    user_input = st.chat_input("Введіть текст: ")
                    if st.button('Натисніть для прослуховування'):
                        user_input = self.listen_for_input()
                if user_input:
                    self.output(user_input)

# Створюємо об'єкт класу Echo_bot та запускаємо його
bot = Echo_bot()
bot.run()
