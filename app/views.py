from flask import render_template, flash, redirect, request, session
from app import app, db
from .forms import LoginForm, RegistrationForm
import models


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


@app.route('/user', methods=['GET'])
def user():
    title = 'Welcome'
    username = session['username']
    return render_template('user.html', username=username,  title=title)


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







