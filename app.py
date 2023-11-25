# app.py
import string
import random
from flask import Flask, render_template
from flask_socketio import SocketIO
from mutagen.mp3 import MP3
from database.sql_provider import SQLProvider

app = Flask(__name__)
socketio = SocketIO(app)


class Room:
    def __init__(self):
        self.track = None
        self.time_stamp = 0
        self.is_playing = False

        self.queue = []
        # Генерация 2 случайных цифр
        digits = ''.join(random.choices(string.digits, k=2))
        # Генерация 2 случайных букв
        letters = ''.join(random.choices(string.ascii_letters, k=2))
        # Собираем код из цифр и букв
        random_code = letters + digits
        # Возвращаем сгенерированный код
        self.code = random_code.upper()
        self.messages = [f"Комната {self.code} создана"]

    def add_to_queue(self, title: str, author: str, filename: str):
        print("adding to queue")
        self.queue.append({
            "title": title,
            "author": author,
            "filename": f"static/music/{filename}"
        })
        print("added")
        address = self.queue[-1]["filename"]
        print("address ", address)
        f = MP3(address)
        # print(AudioSegment.from_mp3(self.queue[-1]["filename"]))
        self.queue[-1]["duration"] = f.info.length
        print("duration added")


room = Room()
room.add_to_queue("Ya ebu sobak", "SHaman", "1.mp3")


@app.route('/')
def index():
    return render_template('index_chat.html', room=room)


@socketio.on('new_message')
def new_message(data):
    print('Received message:', data)

    # Добавляем сообщение к глобальной переменной
    room.messages.append(data)

    # Отправляем сообщение всем подключенным клиентам
    socketio.emit('new_message', data)


def update_clients():
    if room.is_playing:
        socketio.emit('play')
    if not room.is_playing:
        socketio.emit('pause')
    socketio.emit('seek', room.time_stamp)


@socketio.on("pause")
def pause(time_stamp):
    room.time_stamp = time_stamp
    room.is_playing = False
    update_clients()


@socketio.on("play")
def play(time_stamp):
    room.time_stamp = time_stamp
    room.is_playing = True
    update_clients()


@socketio.on("seek")
def seek(time_stamp):
    room.time_stamp = time_stamp
    update_clients()


@socketio.on("stop")
def pause():
    room.time_stamp = 0
    room.is_playing = False
    update_clients()


if __name__ == '__main__':
    socketio.run(app, debug=True)
