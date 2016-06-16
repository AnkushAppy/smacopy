from flask import render_template, flash, redirect, request, session, jsonify
from app import app, db
from .forms import LoginForm, RegistrationForm
import models
import datetime


# # def all():
#     return jsonify({ 'Users' : models.User.query.all()})

@app.route('/')
@app.route('/login', methods=['GET','POST'])
def login():
    title = 'Login page'
    form = LoginForm()
    if form.validate_on_submit() and request.method == 'POST':
        #flash('Login requested for username = "%s", remember me="%s"')%(form.username.data,str(form.remember_me.data))
        username = form.username.data
        password = form.password.data
        username_obj = models.User.query.get(username)

        if not username_obj:
            return render_template('login.html', title=title, form=form)

        if username_obj.password != password:
            return render_template('login.html', title=title, form=form)

        if 'username' not in session:
            session['username'] = username
        return redirect('/user')
    return render_template('login.html', title=title, form=form)



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
    return render_template('register.html', title=title, form=form)


@app.route('/user', methods=['GET'])
def user():
    title = 'Welcome'
    username = session['username']
    username_obj = models.User.query.get(username)
    frndlist1 = username_obj.friends_f
    frndlist2 = username_obj.friends_s
    relation = None
    return render_template('user.html', title=title, username_obj = username_obj, frndlist1 = frndlist1, frndlist2 = frndlist2,relation=None)


@app.route('/user/<user_name>', methods=['GET','POST'])
def profile(user_name):
    title = 'Welcome'
    username = session['username']

    if username == user_name:
        return redirect('/user')
    else:
     
        relation = models.Friend.query.filter_by(first_username=username,second_username=user_name).first() or models.Friend.query.filter_by(first_username=user_name,second_username=username).first()
        if relation:
            username_obj = models.User.query.get(user_name)
            frndlist1 = username_obj.friends_f
            frndlist2 = username_obj.friends_s
            return render_template('user.html', title=title, username_obj = username_obj, frndlist1 = frndlist1, frndlist2 = frndlist2,relation=relation)
        else:
            new = 'New'
            username_obj = models.User.query.get(user_name)
            frndlist1 = username_obj.friends_f
            frndlist2 = username_obj.friends_s
            return render_template('user.html', title=title, username_obj = username_obj, frndlist1 = frndlist1, frndlist2 = frndlist2,relation=new)


@app.route('/user/add/<user_name>')
def requestFriendship(user_name):
    p = models.User.query.get(user_name)
    username = session['username']
    if p and session['username'] and (user_name != session['username']):
        relation = models.Friend.query.filter_by(first_username=username,second_username=user_name).first() or models.Friend.query.filter_by(first_username=user_name,second_username=username).first()
        if relation:
            if relation.status == 'pending':
                relation.status = 'Accepted'
                db.session.commit()

        else:
            frnd_obj = models.Friend(first_username=session['username'],second_username=user_name,status='pending',timestamp = datetime.datetime.utcnow(),action_username=session['username'])
            db.session.add(frnd_obj)
            db.session.commit()
    return redirect('/user/%s'%user_name)













