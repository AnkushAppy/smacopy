#!flask/bin/python
import os
import unittest
import datetime, random

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

    def test_empty_db(self):
        rv = self.app.get('/')
        assert b' Hi !! Welcome to social messaging platform' in rv.data

    def login(self,username, password):
        return self.app.post('/login', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

    def logout(self):
        return self.app.get('/logout', follow_redirects=True)

    def register(self,username,email,password,confirm):
        return self.app.post('/register', data=dict(
            username=username,
            email=email,
            password=password,
            confirm=confirm
        ), follow_redirects=True)

    def profile(self,path):
        return self.app.get(path, follow_redirects=True)

    def test_login_logout(self):
        u = User(username='john',email='john@john.com',password='hello')
        db.session.add(u)
        db.session.commit()
        rv = self.login('john', 'hello')
        assert 'Hello john!! Your email: john@john.com' in rv.data
        rv = self.logout()
        assert 'Please Enter Login Credentials' in rv.data
        rv = self.login('invalid_user', 'hello')
        assert 'Username or password are incorrect.' in rv.data
        rv = self.login('john', 'invalid password')
        assert 'Please Enter Login Credentials' in rv.data
        rv = self.login('john','')
        assert 'This field is required.' in rv.data
        rv = self.login('','hello')
        assert 'This field is required.' in rv.data

    def test_register(self):
        rv = self.register('john','john@john.com','hello','hello')
        assert 'Hello john!! Your email: john@john.com' in rv.data
        rv = self.logout()
        assert 'Please Enter Login Credentials' in rv.data
        rv = self.register('', 'johnjohn.com', 'hell', 'helloX')
        assert 'This field is required.' in rv.data
        assert 'Invalid email address.' in rv.data
        assert 'Password must match' in rv.data
        assert 'Field must be between 5 and 64 characters long.' in rv.data

    def test_user_friend(self):
        u = User(username='john', email='john@john.com', password='hello')
        v = User(username='kim', email='kim@kim.com', password='hello')
        f = Friend(first_username='john',second_username='kim',status='pending',timestamp=datetime.datetime.utcnow(),action_username='john')
        #john have send friend request to kim, kim should confirm now
        db.session.add(u)
        db.session.add(v)
        db.session.add(f)
        db.session.commit()
        rv = self.login('john', 'hello')
        assert 'Hello john!! Your email: john@john.com' in rv.data
        rv = self.logout()
        assert 'Please Enter Login Credentials' in rv.data
        rv = self.login('kim', 'hello')
        assert 'Hello kim!! Your email: kim@kim.com' in rv.data
        assert 'Reject' in rv.data
        assert '/user/add/john' in rv.data
        #friendship got accepted by kim. now both should have name in their friend list
        # f = Friend.query.filter_by(first_username='john',second_username='kim').first()
        # f.status = 'Accepted'
        # db.session.commit()
        path = '/user/add/john'
        rv = self.profile(path)
        assert '/user/john' in rv.data
        rv = self.logout()
        rv = self.login('john', 'hello')
        assert 'Hello john!! Your email: john@john.com' in rv.data
        assert '/user/kim' in rv.data
        path = '/user/kim'
        rv = self.profile(path)
        assert '/user/john' in rv.data







    #model testcases
    # def test_unique_user(self):
    #     u1 = 'john'
    #     u2 = 'new_name'
    #     self.assertTrue(User.unique_user(u1))
    #     self.assertTrue(User.unique_user(u2))
    #     u3_name = 'another_user'
    #     u3_email = 'another_user@another_user.com'
    #     u3 = User(username=u3_name,email=u3_email,password='passw')
    #     self.assertTrue(User.unique_user(u3_name))
    #     db.session.add(u3)
    #     db.session.commit()
    #     self.assertFalse(User.unique_user(u3_name))
    #
    # def test_unique_email(self):
    #     u1 = 'john@john.com'
    #     u2 = 'new_name@new_name.com'
    #     self.assertTrue(User.unique_email(u1))
    #     self.assertTrue(User.unique_email(u2))
    #     u3_name = 'another_user'
    #     u3_email = 'another_user@another_user.com'
    #     u3 = User(username=u3_name,email=u3_email,password='hello')
    #     db.session.add(u3)
    #     db.session.commit()
    #     self.assertFalse(User.unique_email(u3_email))
    #     u_0 = User.query.filter_by(email=u3_email).first()
    #     print u_0.email
    #
    # def test_are_friends(self):
    #     u1_name = 'john'
    #     u1_email = 'john@john.com'
    #     u2_name = 'alex'
    #     u2_email = 'alex@alex.com'
    #     u1 = User(username=u1_name,email=u1_email,password='hello')
    #     u2 = User(username=u2_name, email=u2_email, password='hello')
    #     db.session.add(u1)
    #     db.session.add(u2)
    #     db.session.commit()
    #     f = Friend(first_username=u1_name,
    #                second_username=u2_name,
    #                status='Accepted',timestamp=datetime.datetime.utcnow(),action_username=u1_name)
    #     db.session.add(f)
    #     db.session.commit()
    #     self.assertTrue(Friend.are_friends(u1_name,u2_name))
    #
    # def test_count_friends(self):
    #     u1_name = 'john'
    #     u1_email = 'john@john.com'
    #     u2_name = 'alex'
    #     u2_email = 'alex@alex.com'
    #     u3_name = 'cat'
    #     u3_email = 'cat@cat.com'
    #     u1 = User(username=u1_name, email=u1_email, password='hello')
    #     u2 = User(username=u2_name, email=u2_email, password='hello')
    #     u3 = User(username=u3_name, email=u3_email, password='hello')
    #     db.session.add(u1)
    #     db.session.add(u2)
    #     db.session.add(u3)
    #     db.session.commit()
    #     status = 'Accepted'
    #     time = datetime.datetime.utcnow()
    #     f1 = Friend(first_username=u1_name,second_username=u2_name,status=status,timestamp=time,action_username=u1_name)
    #     f2 = Friend(first_username=u1_name, second_username=u3_name, status=status, timestamp=time,action_username=u3_name)
    #     db.session.add(f1)
    #     db.session.add(f2)
    #     db.session.commit()
    #     self.assertEqual(Friend.count_friends(u1_name),2)
    #
    # def test_count_messages(self):
    #     u1_name = 'john'
    #     u1_email = 'john@john.com'
    #     u2_name = 'alex'
    #     u2_email = 'alex@alex.com'
    #     u1 = User(username=u1_name, email=u1_email, password='hello')
    #     u2 = User(username=u2_name, email=u2_email, password='hello')
    #     db.session.add(u1)
    #     db.session.add(u2)
    #     db.session.commit()
    #     status = 'Accepted'
    #     time = datetime.datetime.utcnow()
    #     message_id = random.randint(1000000, 9999999)
    #     m1 = Message(id=random.randint(1000000, 9999999),first_username=u1_name,second_username=u2_name,chat='Hello',timestamp=time,chat_by=u1_name)
    #     m2 = Message(id=random.randint(1000000, 9999999),first_username=u1_name,second_username=u2_name,chat='Hello',timestamp=time,chat_by=u1_name)
    #     m3 = Message(id=random.randint(1000000, 9999999),first_username=u2_name,second_username=u1_name,chat='Hello',timestamp=time,chat_by=u2_name)
    #     db.session.add(m1)
    #     db.session.add(m2)
    #     db.session.add(m3)
    #     db.session.commit()
    #     self.assertEqual(Message.count_messages(u1_name,u2_name), 3)
    #
    # def test_can_user_read_message(self):
    #     u1_name = 'john'
    #     u1_email = 'john@john.com'
    #     u2_name = 'alex'
    #     u2_email = 'alex@alex.com'
    #     u1 = User(username=u1_name, email=u1_email, password='hello')
    #     u2 = User(username=u2_name, email=u2_email, password='hello')
    #     db.session.add(u1)
    #     db.session.add(u2)
    #     db.session.commit()
    #     status = 'Accepted'
    #     time = datetime.datetime.utcnow()
    #     m1 = Message(id=random.randint(1000000, 9999999), first_username=u1_name, second_username=u2_name, chat='Hello',
    #                  timestamp=time, chat_by=u1_name)
    #     db.session.add(m1)
    #     db.session.commit()
    #     # john deletes a message with alex
    #     msg = Message.query.filter_by(first_username='john',second_username='alex').first()
    #     msg.read_permission_first_user = False
    #     db.session.commit()
    #     self.assertFalse(Message.can_user_read_message(u1_name,msg.id))


if __name__=='__main__':
    unittest.main()

#
# @staticmethod
# def can_user_read_message(user1, msg_id):
#     msg = Message.query.get(msg_id)
#     if user1 == msg.first_username:
#         return msg.read_permission_first_user
#     else:
#         return msg.read_permission_second_user