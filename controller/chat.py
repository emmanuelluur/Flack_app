from application import app
import time
from flask import Flask, request, url_for, jsonify, \
    render_template, session, redirect
from flask_socketio import SocketIO, emit, join_room, \
    leave_room, close_room, rooms, disconnect


@app.route("/")
def index():
    return render_template("index.html", title='Flack')

if __name__ == "__main__":
    pass