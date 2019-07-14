document.addEventListener("DOMContentLoaded", function () {
    const socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);
    let room = document.getElementById("room").value;
    // join room
    socket.emit('join', {
        "room": room
    })
    // message to join
    socket.on("join", data=> {
        socket.emit("event", {"message" : `${data['user']} join to ${data['room']}`, "room": room });
    })
    socket.on("event", data=> {
        document.getElementById("events").innerHTML = data['message'];
    })
});