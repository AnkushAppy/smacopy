#!flask/bin/python
import os
import unittest
import datetime

from config import basedir
from app import app, db
from app.models import User, Message, Friend

class TestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_unique_user(self):
        u1 = 'john'
        u2 = 'new_name'
        self.assertTrue(User.unique_user(u1))
        self.assertTrue(User.unique_user(u2))
        u3_name = 'another_user'
        u3_email = 'another_user@another_user.com'
        u3 = User(username=u3_name,email=u3_email,password='passw')
        self.assertTrue(User.unique_user(u3_name))
        db.session.add(u3)
        db.session.commit()
        self.assertFalse(User.unique_user(u3_name))

    def test_unique_email(self):
        u1 = 'john@john.com'
        u2 = 'new_name@new_name.com'
        self.assertTrue(User.unique_email(u1))
        self.assertTrue(User.unique_email(u2))
        u3_name = 'another_user'
        u3_email = 'another_user@another_user.com'
        u3 = User(username=u3_name,email=u3_email,password='hello')
        db.session.add(u3)
        db.session.commit()
        self.assertFalse(User.unique_email(u3_email))
        u_0 = User.query.filter_by(email=u3_email).first()
        print u_0.email

    def test_are_friends(self):
        u1_name = 'john'
        u1_email = 'john@john.com'
        u2_name = 'alex'
        u2_email = 'alex@alex.com'
        u1 = User(username=u1_name,email=u1_email,password='hello')
        u2 = User(username=u2_name, email=u2_email, password='hello')
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        f = Friend(first_username=u1_name,
                   second_username=u2_name,
                   status='Accepted',timestamp=datetime.datetime.utcnow(),action_username=u1_name)
        db.session.add(f)
        db.session.commit()
        self.assertTrue(Friend.are_friends(u1_name,u2_name))

    def test_count_friends(self):
        u1_name = 'john'
        u1_email = 'john@john.com'
        u2_name = 'alex'
        u2_email = 'alex@alex.com'
        u3_name = 'cat'
        u3_email = 'cat@cat.com'
        u1 = User(username=u1_name, email=u1_email, password='hello')
        u2 = User(username=u2_name, email=u2_email, password='hello')
        u3 = User(username=u3_name, email=u3_email, password='hello')
        db.session.add(u1)
        db.session.add(u2)
        db.session.add(u3)
        db.session.commit()
        status = 'Accepted'
        time = datetime.datetime.utcnow()
        f1 = Friend(first_username=u1_name,second_username=u2_name,status=status,timestamp=time,action_username=u1_name)
        f2 = Friend(first_username=u1_name, second_username=u3_name, status=status, timestamp=time,action_username=u3_name)
        db.session.add(f1)
        db.session.add(f2)
        db.session.commit()
        self.assertEqual(Friend.count_friends(u1_name),2)

    def test_count_messages(self):
        u1_name = 'john'
        u1_email = 'john@john.com'
        u2_name = 'alex'
        u2_email = 'alex@alex.com'
        u1 = User(username=u1_name, email=u1_email, password='hello')
        u2 = User(username=u2_name, email=u2_email, password='hello')
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        status = 'Accepted'
        time = datetime.datetime.utcnow()
        m1 = Message(first_username=u1_name,second_username=u2_name,chat='Hello',timestamp=time,chat_by=u1_name)
        m2 = Message(first_username=u1_name,second_username=u2_name,chat='Hello',timestamp=time,chat_by=u1_name)
        m3 = Message(first_username=u2_name,second_username=u1_name,chat='Hello',timestamp=time,chat_by=u2_name)
        db.session.add(m1)
        db.session.add(m2)
        db.session.add(m3)
        db.session.commit()
        self.assertEqual(Message.count_messages(u1_name,u2_name), 3)


if __name__=='__main__':
    unittest.main()
#
# @staticmethod
# def are_friends(self, user1, user2):
#     if Friend.query.filter_by(first_username=user1, second_username=user2, status='Accepted').first() \
#             or Friend.query.filter_by(first_username=user2, second_username=user1, status='Accepted').first():
#         return True
#     return False
#
#
# @staticmethod
# def count_friends(self, user1, user2):
#     frndlist1 = Friend.query.filter_by(first_username=user1, second_username=user2, status='Accepted')
#     frndlist2 = Friend.query.filter_by(first_username=user2, second_username=user1, status='Accepted')
#     frndlist = frndlist1.union(frndlist2)
#     count = 0
#     for f in frndlist:
#         count += 1
#
#     return count