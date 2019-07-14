document.addEventListener("DOMContentLoaded", function () {
    const socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);
    let room = document.getElementById("room").value;
    //send message
    document.getElementById("send_message").addEventListener('click', ()=>{
        let message = document.getElementById("message");
        socket.emit("message", {
            'message': message.value,
            'room': room
        })
        message.value = "";
        message.focus();
    })
    socket.on("message", data=> {
        let li = document.createElement('li');
        let text = document.createTextNode(`${data['user']} says: ${data['message']}`);
        li.appendChild(text);
        document.getElementById('messages').appendChild(li);
    })
    // join room
    socket.emit('join', {
        "room": room
    })
    // message to join
    socket.on("join", data => {
        socket.emit("event", {
            "message": `${data['user']} join to ${data['room']}`,
            "room": room
        });
    })
    socket.on("event", data => {
        document.getElementById("events").innerHTML = data['message'];
    })
    //leave
    socket.on("leave", data => {
        socket.emit("event", {
            "message": `${data['user']} left ${data['room']}`,
            "room": room
        });
    })
    document.getElementById("leave").addEventListener("click", () => {
        socket.emit('leave', {
            "room": room
        })
        setTimeout(() => {
            location.assign('/')
        }, 1000); 
    })
});