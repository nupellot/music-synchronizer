var socket = io.connect('http://' + document.domain + ':' + location.port);

socket.on('new_message', function(data) {
    var chat = document.getElementById('chat');
    var newMessage = document.createElement('li');
    newMessage.textContent = data;
    chat.appendChild(newMessage);
});

function sendMessage() {
    var messageInput = document.getElementById('message_input');
    var message = messageInput.value;
    socket.emit('new_message', message);
    messageInput.value = '';
}


window.onload = function() {
    player = document.getElementById("Player");
};

function requestPlay() {
    socket.emit('play', player.currentTime);
}

function requestPause() {
    socket.emit('pause', player.currentTime);
}

function requestStop() {
    socket.emit('stop', player.currentTime);
}

function requestSeek() {
    // var time_stamp = document.getElementsByClassName("seeker").value / 1000 * player.duration;
    var time_stamp = $(".seeker").val() / 1000 * player.duration;
    socket.emit('seek', time_stamp);
    console.log("time_stamp " + time_stamp)
}

function incrementSeeker() {
    let seeker = document.getElementById("seeker");
    console.log("seeker.max" + seeker.max)
    seeker.value = player.currentTime / player.duration * seeker.max
}


socket.on("seek", function (time_stamp) {
    player.currentTime = time_stamp;
    let seeker = document.getElementById("seeker");
    console.log("seeker.max" + seeker.max)
    seeker.value = time_stamp / player.duration * seeker.max
})
socket.on("pause", function pause() {
    player.pause();
    clearInterval(incrementSeeker)
})
socket.on("play", function play() {
    player.play();
    setInterval(incrementSeeker, 1000);
})
socket.on("stop", function stop() {
    player.pause();
    player.currentTime = 0;
    clearInterval(incrementSeeker)
})