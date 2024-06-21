from flask import Flask, render_template, session, redirect, request, url_for
from flask_socketio import join_room, leave_room, send, SocketIO
from flask_sqlalchemy import SQLAlchemy
import random
from string import ascii_uppercase

app = Flask(__name__)
app.config["SECRET_KEY"] = "your_secret_key"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///chat.db"
db = SQLAlchemy(app)
socketio = SocketIO(app)

# Database models
class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(4), unique=True, nullable=False)
    members = db.Column(db.Integer, default=0)
    messages = db.relationship('Message', backref='room', lazy=True)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    content = db.Column(db.String(500), nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'), nullable=False)

    def to_dict(self):
        return {
            "name": self.name,
            "content": self.content
        }


# Create the database
with app.app_context():
    db.create_all()

def generate_unique_code(length):
    while True:
        code = "".join(random.choices(ascii_uppercase, k=length))
        if not Room.query.filter_by(code=code).first():
            break
    return code

@app.route('/', methods=["POST", "GET"])
def home():
    session.clear()
    if request.method == "POST":
        name = request.form.get("name")
        code = request.form.get("code")
        join = request.form.get("join", False)
        create = request.form.get("create", False)

        if not name:
            return render_template("home.html", error="Please Enter a Name.", code=code, name=name)

        if join != False and not code:
            return render_template("home.html", error="Please enter a room code.", code=code, name=name)

        room = code
        if create != False:
            room = generate_unique_code(4)
            new_room = Room(code=room)
            db.session.add(new_room)
            db.session.commit()
        else:
            existing_room = Room.query.filter_by(code=code).first()
            if not existing_room:
                return render_template("home.html", error="Room Does not exist", code=code, name=name)

        session["room"] = room
        session["name"] = name

        return redirect(url_for("room"))

    return render_template("home.html")

@app.route("/room")
def room():
    room_code = session.get("room")
    if room_code is None or session.get("name") is None:
        return redirect(url_for("home"))

    room = Room.query.filter_by(code=room_code).first()
    if not room:
        return redirect(url_for("home"))

    messages = [msg.to_dict() for msg in Message.query.filter_by(room_id=room.id).all()]
    return render_template("room.html", code=room_code, messages=messages)


@socketio.on("message")
def message(data):
    room_code = session.get("room")
    room = Room.query.filter_by(code=room_code).first()
    if not room:
        return

    content = {
        "name": session.get("name"),
        "message": data["data"]
    }

    new_message = Message(name=content["name"], content=content["message"], room_id=room.id)
    db.session.add(new_message)
    db.session.commit()

    send(content, to=room_code)
    print(f"{session.get('name')} said: {data['data']}")

@socketio.on('connect')
def connect(auth):
    room_code = session.get("room")
    name = session.get("name")

    if not room_code or not name:
        return
    room = Room.query.filter_by(code=room_code).first()
    if not room:
        leave_room(room_code)
        return

    join_room(room_code)
    send({"name": name, "message": "has entered the room!!"}, to=room_code)
    room.members += 1
    db.session.commit()
    print(f"{name} joined room {room_code}")

@socketio.on("disconnect")
def disconnect():
    room_code = session.get("room")
    name = session.get("name")
    leave_room(room_code)

    room = Room.query.filter_by(code=room_code).first()
    if room:
        room.members -= 1
        if room.members <= 0:
            db.session.delete(room)
        db.session.commit()

    send({"name": name, "message": "has left the room"}, to=room_code)
    print(f"{name} has left the {room_code}")

if __name__ == "__main__":
    socketio.run(app, debug=True)
