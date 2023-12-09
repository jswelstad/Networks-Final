const socket = io("http://localhost:5555/")
// Get the canvas element and its context
let canvas = document.getElementById('drawing-canvas');
let ctx = canvas.getContext('2d');

// Variables to track mouse events
let isDrawing = false;
let lastX = 0;
let lastY = 0;



// Event listeners for mouse events
canvas.addEventListener('mousedown', startDrawing);
canvas.addEventListener('mousemove', draw);
canvas.addEventListener('mouseup', stopDrawing);
canvas.addEventListener('mouseout', stopDrawing);

function startDrawing(e) {
    isDrawing = true;
    [lastX, lastY] = [e.clientX - canvas.offsetLeft, e.clientY - canvas.offsetTop];
}

function stopDrawing() {
    isDrawing = false;
}

function draw(e) {
    if (!isDrawing) return;

    var [x, y] = [e.clientX - canvas.offsetLeft, e.clientY - canvas.offsetTop];

    ctx.beginPath();
    ctx.moveTo(lastX, lastY);
    ctx.lineTo(x, y);
    data = { lastX, lastY, x, y }
    ctx.stroke();

    [lastX, lastY] = [x, y];
    socket.emit('draw_event', data);
}


// automaticly adds 
socket.addEventListener('open', (event) => {
  socket.emit('connect');
});

socket.on('draw_response', function (data) {
    ctx.beginPath();
    ctx.moveTo(data.lastX, data.lastY);
    ctx.lineTo(data.x, data.y);
    ctx.stroke();
});

socket.on('player_joined', function (data) {
    playerList = document.getElementById("player-names");
    let newplayer = document.createElement("p");
    console.log(data);
    newplayer.textContent = "test";
    playerList.appendChild(newplayer);
});



// document.getElementById("login-btn").addEventListener('click', ()=> {
//     username = document.getElementById("")
//     socket.emit('connect', data);
// });