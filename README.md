# social messaging application

# Instruction to run the application, we will start from clone repo
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

### To run the testcases, we need to run test.py file which is in root dir
```sh
chmod a+x test.py
./test.py
```

Very minimal ui and simple functionalities are provided. In future websocketIO, javascript and css have to be added. For now CRUD are done through APIs.
