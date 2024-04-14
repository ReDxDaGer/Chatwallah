from flask import Flask, render_template , session , redirect , request
from flask_socketio import join_room , leave_room , send , SocketIO
import random
from string import ascii_uppercase

app = Flask(__name__)

app.config["SECRET_KEY"] = "your_secret_key"
socketio = SocketIO(app)


@app.route('/' , methods=["PSOT" , "GET"] )
def home():
    return render_template("index.html")

if __name__ == "__main__":
    socketio.run(app , debug=True)