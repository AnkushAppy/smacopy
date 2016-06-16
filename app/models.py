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