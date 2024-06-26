# practicity
A Django server to track your practice progress (made for musicians) using a sqlite3 database.

## Prerequisites
Install sqlite3 on your system
```
sudo apt install sqlite3
```
Or on Mac
```
brew install sqlite3
```

## Set up
Install the python3 virtual environment on your system
```
sudo apt install python3.10-venv
```

Set up the virtual environment for the django webserver
```
python3 -m venv .venv
source .venv/bin/activate
pip3 install -r requirements.txt
``` 

## Run the Webserver
```
python3 manage.py runserver
```

## Run the Tests
```
python3 manage.py test
```

## Additional tools
In VSCode one can load the plugin to investigate the database: https://github.com/cweijan/vscode-database-client 