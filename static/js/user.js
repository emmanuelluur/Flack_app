document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById("app_room");
    const socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);
    form.addEventListener("click", el => {
        if (el.target.getAttribute("id") == 'btn_create') {
            let data = new FormData(form);
            post('/create/room')
            .then(response => {
                let data = JSON.parse(response);
                console.log(data)
            })
            .catch(err => {
                console.log(err);
            })
            room.value = '';
            room.focus();   
        }
    })
});