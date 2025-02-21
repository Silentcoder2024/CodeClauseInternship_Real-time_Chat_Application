from flask import Flask, render_template, request
from flask_socketio import SocketIO, send
from flask_sqlalchemy import SQLAlchemy
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chat.db'
db = SQLAlchemy(app)
socketio = SocketIO(app, cors_allowed_origins="*")
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    text = db.Column(db.String(500), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)
@app.route("/")
def index():
    messages = Message.query.all()
    return render_template("index.html", messages=messages)
@socketio.on("message")
def handle_message(data):
    print(f"Message: {data}")
    msg = Message(username=data["username"], text=data["text"])
    db.session.add(msg)
    db.session.commit()
    send(data, broadcast=True)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    socketio.run(app, host="127.0.0.1", port=5000, debug=True)

