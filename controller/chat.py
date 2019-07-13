from application import app
import time
from flask import Flask, request, url_for, jsonify, \
    render_template, session, redirect
from flask_socketio import SocketIO, emit, join_room, \
    leave_room, close_room, rooms, disconnect

# variables
users = []
rooms = ['public']
#routes & controllers
@app.route("/")
def index():
    return render_template("index.html", title='Flack')

#method post
@app.route("/user/join", methods=['POST'])
def join_user():
    if request.method == 'POST':
        username = request.form['username']
        if username in users:
            return "User Already Exist"
        users.append(username)
        session['user'] = username
        return session['user']

@app.route("/logout")
def logout():
    if len(users) > 0:
        users.remove(session['user'])
    session.clear()
    return redirect("/", code=302)

if __name__ == "__main__":
    pass