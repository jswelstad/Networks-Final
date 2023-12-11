/*
Client side rendering and networking of the game
*/

const socket = io("http://127.0.0.1:5555/")
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

//If client clicked, record that initial point and set isDrawing to true
function startDrawing(e) {
    isDrawing = true;
    [lastX, lastY] = [e.clientX - canvas.offsetLeft, e.clientY - canvas.offsetTop];
}

//If they stopped clicking, stop recording points
function stopDrawing() {
    isDrawing = false;
}

//If isDrawing is true (The user clicked), record all points of the mouse
function draw(e) {
    if (!isDrawing) return;

    var [x, y] = [e.clientX - canvas.offsetLeft, e.clientY - canvas.offsetTop];

    ctx.beginPath();
    ctx.moveTo(lastX, lastY);
    ctx.lineTo(x, y);
    data = { lastX, lastY, x, y }
    ctx.stroke();

    [lastX, lastY] = [x, y];
    socket.emit('draw_event', data);    //Send the drawing data to the server
}


// When you connect, send your connect data to server so it can display it to the other clients
socket.addEventListener('open', (event) => {
  socket.emit('connect');
});

//Listens for a draw event from server and draws the received drawing data on the canvas
socket.on('draw_response', function (data) {
    ctx.beginPath();
    ctx.moveTo(data.lastX, data.lastY);
    ctx.lineTo(data.x, data.y);
    ctx.stroke();
});

//Listens for a player join event and adds the new player to the player list
socket.on('player_joined', function (data) {
    playerList = document.getElementById("player-names");
    let newplayer = document.createElement("p");
    console.log(data);
    newplayer.textContent = "test";
    playerList.appendChild(newplayer);
});

document.getElementById("login-btn").addEventListener('click', ()=> {
    username = document.getElementById("")
    socket.emit('connect', data);
});