from flask import render_template, flash, redirect, request, session
from app import app, db
from .forms import LoginForm, RegistrationForm, MessageForm
import models
import datetime
from datetime import timedelta


@app.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=5)


@app.route('/')
@app.route('/login', methods=['GET','POST'])
def login():
    title = 'Login page'
    form = LoginForm()
    if form.validate_on_submit() and request.method == 'POST':
        error=None
        #flash('Login requested for username = "%s", remember me="%s"')%(form.username.data,str(form.remember_me.data))
        username = form.username.data
        username = username.strip()
        password = form.password.data
        username_obj = models.User.query.get(username)

        if not username_obj:
            error = "* Username or password are incorrect."
            return render_template('login.html',
                                   title=title,
                                   form=form, error=error)

        if username_obj.password != password:
            error = "Username or passsword are incorrect."
            return render_template('login.html',
                                   title=title,
                                   form=form, error=error)

        if 'username' not in session:
            session['username'] = username
        redirect_to_user = redirect('/user')
        response = app.make_response(redirect_to_user)
        response.set_cookie('username', value=username)
        return response
    return render_template('login.html',
                           title=title,
                           form=form)


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/login')


@app.route('/register', methods=['GET','POST'])
def register():
    title = 'Welcome'
    form = RegistrationForm()
    if form.validate_on_submit() and request.method == 'POST':
        new_user = models.User(username=form.username.data,
                               email = form.email.data,
                               password = form.password.data)
        models.db.session.add(new_user)
        models.db.session.commit()
        if 'username' not in session:
            session['username'] = form.username.data
        return redirect('/user')
    return render_template('register.html',
                           title=title,
                           form=form)


@app.route('/user', methods=['GET'])
def user():
    title = 'Welcome'
    username = session['username']
    username_obj = models.User.query.get(username)
    frndlist1 = username_obj.friends_f
    frndlist2 = username_obj.friends_s
    msg_obj1 = models.Message.query.filter_by(first_username=username)
    msg_obj2 = models.Message.query.filter_by(second_username=username)
    msg_all = msg_obj1.union(msg_obj2).order_by(models.Message.timestamp)
    relation = None
    return render_template('user.html',
                           title=title,
                           username_obj=username_obj,
                           frndlist1 = frndlist1,
                           frndlist2 = frndlist2,
                           relation=relation,
                           username=username,msg_all=msg_all)


@app.route('/user/<user_name>', methods=['GET','POST'])
def profile(user_name):
    title = 'Welcome'
    username = session['username']

    if username == user_name:
        return redirect('/user')
    else:
     
        relation = models.Friend.query.filter_by(first_username=username,
                                                 second_username=user_name).first() \
                   or models.Friend.query.filter_by(first_username=user_name,
                                                    second_username=username).first()
        if relation:
            username_obj = models.User.query.get(user_name)
            my_obj = models.User.query.get(username)
            frndlist1 = username_obj.friends_f
            frndlist2 = username_obj.friends_s
            msg_obj1 = models.Message.query.filter_by(first_username=username,second_username=user_name)
            msg_obj2 = models.Message.query.filter_by(first_username=user_name,second_username=username)
            msg_all = msg_obj1.union(msg_obj2).order_by(models.Message.timestamp).limit(10)
            return render_template('user.html',
                                   title=title,
                                   username_obj = username_obj,
                                   frndlist1 = frndlist1,
                                   frndlist2 = frndlist2,
                                   relation=relation,
                                   username=username,msg_obj2=msg_obj2,msg_obj1=msg_obj1,msg_all=msg_all)
        else:
            new = 'New'
            username_obj = models.User.query.get(user_name)
            if not username_obj:
                return redirect('/user')
            frndlist1 = username_obj.friends_f
            frndlist2 = username_obj.friends_s
            return render_template('user.html',
                                   title=title,
                                   username_obj = username_obj,
                                   frndlist1 = frndlist1,
                                   frndlist2=frndlist2,
                                   relation=new,
                                   username=username)


@app.route('/user/add/<user_name>')
def requestFriendship(user_name):
    p = models.User.query.get(user_name)
    username = session['username']
    if p and session['username'] and (user_name != session['username']):
        relation = models.Friend.query.filter_by(first_username=username,
                                                 second_username=user_name).first() \
                   or models.Friend.query.filter_by(first_username=user_name,
                                                    second_username=username).first()
        if relation:
            if relation.status == 'pending':
                relation.status = 'Accepted'
                db.session.commit()

        else:
            frnd_obj = models.Friend(first_username=session['username'],
                                     second_username=user_name,
                                     status='pending',
                                     timestamp = datetime.datetime.utcnow(),
                                     action_username=session['username'])
            db.session.add(frnd_obj)
            db.session.commit()
    if not p:
        return redirect('/user')
    return redirect('/user/%s'%user_name)


@app.route('/user/reject/<user_name>')
def reject(user_name):
    p = models.User.query.get(user_name)
    username = session['username']
    if p and session['username'] and (user_name != session['username']):
        relation = models.Friend.query.filter_by(first_username=username,
                                                 second_username=user_name).first() \
                   or models.Friend.query.filter_by(first_username=user_name,
                                                    second_username=username).first()
        relation.status = 'Rejected'
        db.session.commit()
    if not p:
        return redirect('/user')
    return redirect('/user/%s'%user_name)


@app.route('/user/unfriend/<user_name>')
def unfriend(user_name):
    relation = models.Friend.query.filter_by(first_username=user_name,second_username=session['username']).first() \
               or models.Friend.query.filter_by(first_username=session['username'],second_username=user_name).first()
    if not relation:
        user_obj = models.User.query.get(user_name)
        if not user_obj:
            return redirect('/user')
        return redirect('/user/%s' % user_name)
    db.session.delete(relation)
    db.session.commit()
    return redirect('/user/%s'%user_name)

@app.route('/user/<user_name>/message',methods=['GET','POST'])
def message(user_name):
    form = MessageForm()
    username = session['username']
    username_obj = models.User.query.get(user_name)
    user_obj = models.User.query.get(username)
    if not username_obj:
        redirect('/user')
    if not user_obj:
        redirect('/user')
    if user_name == username:
        redirect('/user')

    relation = models.Friend.query.filter_by(first_username=username,
                                             second_username=user_name).first() \
                   or models.Friend.query.filter_by(first_username=user_name,
                                            second_username=username).first()

    msg_obj1 = models.Message.query.filter_by(first_username=username, second_username=user_name)
    msg_obj2 = models.Message.query.filter_by(first_username=user_name, second_username=username)
    msg_all = msg_obj1.union(msg_obj2).order_by(models.Message.timestamp).limit(10)

    frndlist1 = user_obj.friends_f
    frndlist2 = user_obj.friends_s
    frnd_all = frndlist1.union(frndlist2).order_by(models.Friend.timestamp)
    if form.validate_on_submit() and request.method == 'POST':
        msg = models.Message(first_username=username, second_username=user_name, chat=form.message.data,
                             timestamp=datetime.datetime.utcnow(), chat_by=username)
        db.session.add(msg)
        db.session.commit()

        return render_template('message.html',
                               username_obj=username_obj,
                               username=username,
                               msg_all=msg_all,
                               relation=relation,
                               form=form,)

    return render_template('message.html',
                           username_obj=username_obj,
                           username=username,
                           msg_all=msg_all,
                           relation=relation,
                           form=form)



















