# social messaging application
####Purpose: 
A messaging app where users can interact with other user. Many functionalities should be provided like send friend request, confirm, reject, block etc. User should be able to chat. Many functionalities should be provided like delete chat, multiple user chat, sorted by time, user online status etc. 

####Tools: 
refer requirement.txt


####Instruction to run the application, we will start from clone repo
```sh
git clone https://github.com/AnkushAppy/smacopy.git
cd smacopy
virtualenv flask
flask/bin/pip install -r requirements.txt
./db_create.py    //ignore error
./db_migrate.py
./run.py
```

check browser for http://127.0.0.1:5000 or http://127.0.0.1:5000/login

some login details for example, (username,password)->(john,hello),(alex,hello),(kim,hello),(cat,hello),(ethan,hello)

####Models and Relations
We have 3 tables. First is User table:
```sh
User:
username = db.Column(db.String(64), primary_key=True)
email = db.Column(db.String(64), index=True, unique=True)
password = db.Column(db.String(64))
```
Friend table: [first_username, second_username] should be unique.
```sh
Friend:
id = db.Column(db.Integer, primary_key=True)
first_username = db.Column(db.String(64), db.ForeignKey(User.username))
second_username = db.Column(db.String(64), db.ForeignKey(User.username))
status = db.Column(db.String(64))
timestamp = db.Column(db.DateTime)
action_username = db.Column(db.String(64), db.ForeignKey(User.username))
__table_args__ = (db.Index('myIndex','first_username', 'second_username',unique=True), {})
```
Message table:
```sh
id = db.Column(db.Integer, primary_key=True)
first_username = db.Column(db.String(64), db.ForeignKey(User.username))
second_username = db.Column(db.String(64), db.ForeignKey(User.username))
chat = db.Column(db.String(140))
timestamp = db.Column(db.DateTime)
chat_by = db.Column(db.String(64), db.ForeignKey(User.username))
read_permission_first_user = db.Column(db.Boolean, default=True)
read_permission_second_user = db.Column(db.Boolean, default=True)
```
All foreign key in Friend and Message table refering to username of User table. Accordingly relations are created in User class in models. flask_sqlalchemy is used as ORM over sqlite3 as SQL database. Syntax above are sqlalchamey's.


####To run the testcases, we need to run test.py file which is in root dir. Test are made for APIs and models. More test are yet to be written.
```sh
chmod a+x test.py
./test.py
```

Note: Very minimal ui and simple functionalities are provided. In future websocketIO, javascript and css have to be added. For now CRUD are done through APIs.
