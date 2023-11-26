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
    socket.emit('stop');
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
    let seeker = document.getElementById("seeker");
    seeker.value = time_stamp / player.duration * seeker.max
    clearInterval(incrementSeeker)
})


function toggleMute() {
    // Переключение между включенным и выключенным состоянием звука
    player.muted = !player.muted;
    if (player.muted) {
        $(".unmuted-icon").style.display = "none"
        $(".muted-icon").style.display = "block"
    }
    if (!player.muted) {
        $(".unmuted-icon").style.display = "block"
        $(".muted-icon").style.display = "none"
    }

    // Вывод значения в консоль (или можно использовать его для чего-то еще)
    // console.log('Audio muted:', player.muted);
}



var uploadContainer = document.getElementById('uploadContainer');
var fileInput = document.getElementById('fileInput');

function handleDragOver(e) {
    e.preventDefault();
    uploadContainer.classList.add('dragover');
}

function handleDragLeave() {
    uploadContainer.classList.remove('dragover');
}

function handleDrop(e) {
    e.preventDefault();
    uploadContainer.classList.remove('dragover');
    var files = e.dataTransfer.files;
    handleFiles(files);
}

function handleFiles(files) {
    // Обработка выбранных файлов
    console.log(files);
}

uploadContainer.addEventListener('dragover', handleDragOver);
uploadContainer.addEventListener('dragleave', handleDragLeave);
uploadContainer.addEventListener('drop', handleDrop);

fileInput.addEventListener('change', function() {
    var files = fileInput.files;
    handleFiles(files);
});

// Добавлен обработчик события click
uploadContainer.addEventListener('click', function() {
    fileInput.click();
});