# app.py
import string
import random

from flask import Flask, render_template
from flask_socketio import SocketIO
from database.sql_provider import SQLProvider

app = Flask(__name__)
socketio = SocketIO(app)


class Room:
    def __init__(self):
        current_track = None
        current_time_stamp = None

        self.queue = ["1.mp3"]
        # Генерация 2 случайных цифр
        digits = ''.join(random.choices(string.digits, k=2))
        # Генерация 2 случайных букв
        letters = ''.join(random.choices(string.ascii_letters, k=2))
        # Собираем код из цифр и букв
        random_code = letters + digits
        # Возвращаем сгенерированный код
        self.code = random_code.upper()
        self.messages = [f"Комната {self.code} создана"]




room = Room()


@app.route('/')
def index():
    return render_template('index_chat.html', room=room)

@socketio.on('new_message')
def handle_message(data):

    print('Received message:', data)

    # Добавляем сообщение к глобальной переменной
    room.messages.append(data)

    # Отправляем сообщение всем подключенным клиентам
    socketio.emit('new_message', data)


if __name__ == '__main__':
    socketio.run(app, debug=True)
