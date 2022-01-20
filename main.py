import speech_recognition
import os
import sys
import random
import pyttsx3
import webbrowser

commands_dict = {
    'commands': {
        'greeting': ['здраствуй', 'приветствую', 'привет'],
        'create_task': ['добавить задачу', 'создать задачу', 'заметка'],
        'play_music': ['включить музыку', 'включи музыку', 'музыка'],
        'restart_pc': ['перезагрузить компьютер'],
        'shutdown_pc': ['выключить компьютер'],
        'cancel_restart_pc': ['отмена перезагрузки'],
        'cancel_shutdown_pc': ['отмена выключения'],
        'open_browser': ['браузер'],
        'exit': ['выйти', 'завершить работу', 'выход']
    }
}

class Pyatnica():
    def __init__(self):
        self.speaker = pyttsx3.init()
        self.speaker.setProperty('voice', 'russian')
        self.speaker.setProperty('rate', 150)
        self.sr = speech_recognition.Recognizer()
        self.sr.pause_threshold = 0.5

    #функция прослушивания комманды
    def listen_command(self):

        try:
            with speech_recognition.Microphone() as mic:
                self.sr.adjust_for_ambient_noise(source=mic, duration=0.5)
                audio = self.sr.listen(source=mic)
                query = self.sr.recognize_google(audio_data=audio, language='ru-RU').lower()

            return query
        except speech_recognition.UnknownValueError:
            self.speaker.say('повторите пожалуйста, я Вас не понял')
            self.speaker.runAndWait()

    #Приветствие
    def greeting(self):

        self.speaker.say('Здраствуйте хозяин!')
        self.speaker.runAndWait()

    #добавление задач в список дел
    def create_task(self):
        
        self.speaker.say('Что добавим в список дел?')
        self.speaker.runAndWait()

        
        query = self.listen_command()

        with open('todo-list.txt', 'a') as file:
            file.write(f'{query}\n')

        self.speaker.say(f'Задача {query} добавлена в список дел')
        self.speaker.runAndWait()

    #включение случайной песни
    def play_music(self):
        files = os.listdir('music')
        random_file = f'music\{random.choice(files)}'
        os.startfile(f'{random_file}')

        
    def restart_pc(self):
        os.system('shutdown -r +3')
        self.speaker.say('Компьютер будет перезагружен через три минуты. Для отмены введите shutdown -c')
        self.speaker.runAndWait()
    
    def cancel_restart_pc(self):
        os.system('shutdown -c')
        self.speaker.say('Отмена перезагрузки')
        self.speaker.runAndWait()

    def shutdown_pc(self):
        os.system('shutdown +3')
        self.speaker.say('Компьютер будет выключен через три минуты. Для отмены введите shutdown -c')
        self.speaker.runAndWait()
    
    def cancel_shutdown_pc(self):
        os.system('shutdown -c')
        self.speaker.say('Выключение компьютеро успешно отменено')
        self.speaker.runAndWait()

    #открытие браузера
    def open_browser(self):
        self.speaker.say('Какую страницу мне открыть')
        self.speaker.runAndWait()

        query = self.listen_command()
        
        if 'google' in query:
            self.speaker.say('Что мне найти?')
            self.speaker.runAndWait()

            query = self.listen_command()
            query = query.split()

            webbrowser.open('https://www.google.com/search?q=' + '+'.join(query))
            self.speaker.say(f'Поиск по {query} выполнен')
            self.speaker.runAndWait()

            return

        elif 'youtube' in query:
            self.speaker.say('Какой ролик найти?')
            self.speaker.runAndWait()

            query = self.listen_command()
            query = query.split()

            webbrowser.open('https://www.youtube.com/results?search_query?=' + '+'.join(query))
            self.speaker.say(f'Поиск по {query} выполнен')
            self.speaker.runAndWait()

            return

        else:
            self.speaker.say('Я вас не понял')
            self.speaker.runAndWait()

    #прощание
    def exit(self):
        self.speaker.say('До скоро встречи!')
        self.speaker.runAndWait()
        sys.exit()

def main():
    bot = Pyatnica()
    sr = speech_recognition.Recognizer()
    while True:
        try:
            with speech_recognition.Microphone() as mic:
                sr.adjust_for_ambient_noise(source=mic, duration=0.5)
                audio = sr.listen(source=mic)
                query = sr.recognize_google(audio_data=audio, language='ru-RU').lower()
            
            for k,v in commands_dict['commands'].items():
                if query in v:
                    execute = getattr(bot, k)
                    execute()
        
        except Exception as _ex:
            print(_ex, 'Команда не распознана')
            sys.exit()

if __name__ == '__main__':
    main()