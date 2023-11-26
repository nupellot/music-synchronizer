# app.py
import math
import string
import random
import time

from flask import Flask, render_template
from flask_socketio import SocketIO
from mutagen.mp3 import MP3
import qrcode
from database.sql_provider import SQLProvider

app = Flask(__name__)
socketio = SocketIO(app)


class Room:
    def __init__(self):
        self.time_stamp = 0
        self.is_playing = False
        self.last_pressed_play = 0
        self.queue = []
        # Генерация 2 случайных цифр
        digits = ''.join(random.choices(string.digits, k=2))
        # Генерация 2 случайных букв
        letters = ''.join(random.choices(string.ascii_letters, k=2))
        # Собираем код из цифр и букв
        random_code = letters + digits
        # Возвращаем сгенерированный код
        self.code = random_code.upper()
        self.create_QRCode()
        self.messages = [f"Комната {self.code} создана"]
        self.add_to_queue("Elegant Name", "Author Unknown", "1.mp3")
        self.current_track = self.queue[0]

    def create_QRCode(self):
        # Создание объекта QRCode
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=15,
            border=2,
        )

        # Добавление данных в объект QRCode
        qr.add_data(self.code)
        qr.make(fit=True)

        # Создание изображения QR-кода
        img = qr.make_image(
            fill_color="red",
            back_color="white"
        )

        # Сохранение изображения
        img.save(f"static/QRCodes/{self.code}.png")

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
        self.queue[-1]["duration"] = str(math.floor(f.info.length / 60)) + ":" + str(math.floor(f.info.length % 60))
        print("duration added")


room = Room()
room.add_to_queue("Ya russkiy", "SHaman", "1.mp3")
room.add_to_queue("Despacito", "Some spanish dude", "2.mp3")


@socketio.on('connect')
def new_connection(data):
    print('New connection:', data)
    update_clients()


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
    room.time_stamp += time.time() - room.last_pressed_play
    socketio.emit('seek', room.time_stamp)


@socketio.on("pause")
def pause():
    room.is_playing = False
    update_clients()


@socketio.on("play")
def play():
    room.is_playing = True
    room.last_pressed_play = time.time()
    update_clients()


@socketio.on("seek")
def seek(time_stamp):
    room.time_stamp = time_stamp
    if room.is_playing:
        room.last_pressed_play = time.time()
    update_clients()


@socketio.on("stop")
def pause():
    room.time_stamp = 0
    room.is_playing = False
    update_clients()


@socketio.on("ended")
def ended():
    room.time_stamp = 0
    room.current_track = room.queue[(room.queue.index(room.current_track) + 1) % len(room.queue)]
    with open(room.current_track["filename"], "rb") as file:
        next_track = file.read()
        socketio.send(next_track)
    play()


if __name__ == '__main__':
    socketio.run(app, debug=True)
