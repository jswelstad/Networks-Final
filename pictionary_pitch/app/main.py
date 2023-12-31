from flask import Flask, render_template
from flask import request
import os
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app)

#Render the index.html file
@app.route('/')
def index():
    return render_template('index.html')

#When a client connects, notify all clients that someone connected
@socketio.on("connect")
def handle_connect(data):
    print(f"data: {data}")
    socketio.emit('player_joined', data)

@socketio.on("disconnect")
def handle_disconnect():
    pass

#When server recieves draw data, transmit that data to all clients
@socketio.on('draw_event')
def handle_draw(data):
    socketio.emit('draw_response', data)


if __name__ == '__main__':
    #Bind the port
    port = int(os.environ.get('PORT', 5555))
    app.run(debug=True, host='0.0.0.0', port=port)