const responses = (type, response) => {
    let div = document.createElement("div");
    div.setAttribute("class", type);
    let txt = document.createTextNode(response);
    div.appendChild(txt);
    return div;
}

document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById("app_room");
    const socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);
    form.addEventListener("click", el => {
        if (el.target.getAttribute("id") == 'btn_create') {
            let data = new FormData(form);
            let room = document.getElementById("room");


            post('/create/room', data)
                .then(response => {
                    let data = JSON.parse(response);
                    let content = document.getElementById("responses");
                    let type = "alert alert-success";
                    content.innerHTML = '';
                    if (data.type == "error") {
                        type = "alert alert-danger";
                        content.appendChild(responses(type, data.response));
                    } else {
                        content.appendChild(responses(type, data.response));
                        // with socket room uodate un realtime
                        socket.emit('create_room', {
                            "room": document.getElementById("room").value
                        });
                    }
                })
                .then(() => {
                    room.value = '';
                    room.focus();
                })
                .catch(err => {
                    console.log(err);
                })

        }
    });
    // update Rooms
    socket.on("room_created", data => {
        let content = document.getElementById("rooms");
        let roomContent = document.createElement("p");
        let room = document.createTextNode(data['room']);
        roomContent.appendChild(room);
        content.appendChild(roomContent);
    })
});