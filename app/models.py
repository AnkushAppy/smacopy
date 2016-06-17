from app import db
import enum


# class FriendShipStatus(enum.Enum):
#     PENDING = 'Pending'
#     BLOCKED = 'Blocked'
#     ACCEPTED = 'Accepted'
#     REJECTED = 'Rejected'


class User(db.Model):
    username = db.Column(db.String(64), primary_key=True)
    email = db.Column(db.String(64), index=True, unique=True)
    password = db.Column(db.String(64))
    friends_f = db.relationship('Friend', backref='user_f', lazy='dynamic', foreign_keys='Friend.first_username')
    friends_s = db.relationship('Friend', backref='user_s', lazy='dynamic', foreign_keys='Friend.second_username')
    friends_a = db.relationship('Friend', backref='user_a', lazy='dynamic', foreign_keys='Friend.action_username')

    message_f = db.relationship('Message', backref='user_f', lazy='dynamic', foreign_keys='Message.first_username')
    message_s = db.relationship('Message', backref='user_s', lazy='dynamic', foreign_keys='Message.second_username')
    message_a = db.relationship('Message', backref='user_a', lazy='dynamic', foreign_keys='Message.chat_by')

    def __repr__(self):
        return '<User: %s Email: %s>' % (self.username,self.email)


class Friend(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_username = db.Column(db.String(64), db.ForeignKey(User.username))
    second_username = db.Column(db.String(64), db.ForeignKey(User.username))
    status = db.Column(db.String(64))
    timestamp = db.Column(db.DateTime)
    action_username = db.Column(db.String(64), db.ForeignKey(User.username))
    __table_args__ = (db.Index('myIndex','first_username', 'second_username',unique=True), {})

    def __repr__(self):
        return '<%s and %s have friendship status %s >'%(self.first_username,self.second_username,self.status)


#p = models.Friend(id=1,first_username='john',second_username='cat',status='pending',timestamp=datetime.datetime.utcnow(),action_user='john')

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_username = db.Column(db.String(64), db.ForeignKey(User.username))
    second_username = db.Column(db.String(64), db.ForeignKey(User.username))
    chat = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime)
    chat_by = db.Column(db.String(64), db.ForeignKey(User.username))
    read_permission_first_user = db.Column(db.Boolean, default=True)
    read_permission_second_user = db.Column(db.Boolean, default=True)

    def __repr__(self):
        if self.second_username == self.chat_by:
            return '<%s messaged %s : \" %s \">'%(self.chat_by, self.first_username, self.chat)
        return '<%s messaged %s : \" %s \">' % (self.chat_by, self.second_username, self.chat)


#msg = models.Message(first_username='ethan',second_username='john',chat='Hi john, how are you',timestamp=datetime.datetime.utcnow(),chat_by='ethan')
# asd

