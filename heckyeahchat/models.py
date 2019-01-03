from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    conversation_id = db.Column(db.String(200), db.ForeignKey(
        'conversation.id'), nullable=False)


class Conversation(db.Model):
    id = db.Column(db.String(200), primary_key=True)
    name = db.Column(db.String(100))
    messages = db.relationship('Message', backref='conversation', lazy=True)


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_time = db.Column(db.DateTime(), nullable=False)
    sender = db.Column(db.String(80), nullable=False)
    message = db.Column(db.Text, nullable=False)
    msg_type = db.Column(db.String(10), nullable=False)
    conversation_name = db.Column(db.String(50), nullable=False)
    conversation_id = db.Column(db.String(200), db.ForeignKey(
        'conversation.id'), nullable=False)

    def __repr__(self):
        return self.message
