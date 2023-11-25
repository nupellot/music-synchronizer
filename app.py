# app.py
from flask import Flask, render_template
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app)

# Глобальная переменная для хранения сообщений
messages = []

@app.route('/')
def index():
    return render_template('index_chat.html', messages=messages)

@socketio.on('message')
def handle_message(data):
    print('Received message:', data)

    # Добавляем сообщение к глобальной переменной
    messages.append(data)

    # Отправляем сообщение всем подключенным клиентам
    socketio.emit('message', data)

if __name__ == '__main__':
    socketio.run(app, debug=True)
