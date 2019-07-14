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
    if 'user' in session:
        return redirect(url_for('me', me=session['user']))
    
    return render_template("index.html", title='Flack')

# method post
@app.route("/user/join", methods=['POST'])
def join_user():
    if request.method == 'POST':
        username = request.form['username']
        if username in users:
            return "User Already Exist"
        users.append(username)
        session['user'] = username
        return redirect(url_for('me', me=session['user']))


@app.route("/flack/<me>")
def me(me):
    if me is None:
        return redirect(url_for('index'))
    if not('user' in session):
        return redirect(url_for('index'))
    if not (me in users):
        return redirect(url_for('index'))
    return render_template("user.html", title='Flack', user=me, rooms=rooms)

@app.route("/create/room", methods = ['POST'])
def create_room():
    if request.method == 'POST':
        room = request.form['room']
        if len(room) < 2:
            return jsonify({"type:": "error", "response": "Must be higher than 1 letters"})
        #rooms.append(room)
        return jsonify({"type:": "success", "response": "Room Created"})
    return jsonify({})
@app.route("/logout")
def logout():
    if len(users) > 0:
        users.remove(session['user'])
    session.clear()
    return redirect("/", code=302)


if __name__ == "__main__":
    pass
