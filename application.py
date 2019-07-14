import os

from flask import Flask
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)

from controller.chat import *

if __name__ == "__main__":
    socketio.run(app,host='0.0.0.0', debug=True)
