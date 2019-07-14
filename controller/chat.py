from application import app
import time
from flask import Flask, request, url_for, jsonify, \
    render_template, session, redirect
from flask_socketio import SocketIO, emit, join_room, \
    leave_room, close_room, rooms, disconnect

socketio = SocketIO(app)
# variables
users = []
rooms = ['public']
user_room = []
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
    if len(user_room) == 1:
            return redirect(url_for('chat_room', room=user_room[0]))

    return render_template("user.html", title='Flack', user=me, rooms=rooms)


@app.route("/rooms/<room>")
def chat_room(room):
    if room is None:
        return redirect(url_for('me', me=session['user']))
    if not(room in rooms):
        return redirect(url_for('me', me=session['user']))
    if len(user_room) == 0:
        user_room.append(room)
    return render_template('chat.html', title='Flack', room=room, rooms=rooms)


@app.route("/create/room", methods=['POST'])
def create_room():
    if request.method == 'POST':
        room = request.form['room']
        if len(room) < 2:
            return jsonify({"type": "error", "response": "Must be higher than 1 letters"})
        if room in rooms:
            return jsonify({"type": "error", "response": "Room already registered"})
        rooms.append(room)
        return jsonify({"type": "success", "response": "Room Created"})
    return jsonify({})


@app.route("/logout")
def logout():
    if "user" in session:
        if len(users) > 0:
            users.remove(session['user'])
    session.clear()
    return redirect("/", code=302)


@socketio.on("create_room")
def created_room(data):
    message = data['room']
    emit("room_created", {"room": message}, broadcast=True)


@socketio.on("join")
def join(data):
    room = data['room']
    join_room(room)
    emit("join", {"room": room,
                  "user": session['user']}, room=room, broadcast=True)


@socketio.on("leave")
def room_leave(data):
    room = data['room']
    if room in user_room:
        user_room.remove(room)

    leave_room(room)
    emit("leave", {"room": room,
                   "user": session['user']}, room=room, broadcast=True)


@socketio.on("event")
def event(data):
    message = data['message']
    room = data['room']
    emit("event", {"message": message, "room": room},
         room=room, broadcast=True)


if __name__ == "__main__":
    pass
