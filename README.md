<p align="center" widht="100%">
<img src="./docu/practicity_logo.PNG" alt="logo image" style="width:30%;height:30%;">
</p>
<hr>

# Practicity
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

## Create the django database
First, check if changes have happened to the database. (if this is a fresh set up this should not be the case)
```
python3 manage.py makemigrations
``` 
And then update the databse / create it if it does not exist
```
python3 manage.py migrate
```

# Run the Webserver
```
python3 manage.py runserver
```

# Run the Tests
```
python3 manage.py test
```

## Additional tools
In VSCode one can load the plugin to investigate the database: https://github.com/cweijan/vscode-database-client 

# The directories
```
├── LICENSE
├── README.md
├── db_diagram.drawio
├── practicity
│   ├── db.sqlite3
│   ├── manage.py
│   ├── practicity
│   ├── progressTracker
│   └── templates
└── requirements.txt
```
* `manage.py` is the command-line utility for the Django server (one can start the server etc...)
* `practicity/settings.py` contains all configurations for the Django project
* `practicity/urls.py` contains all the urls that are set up by the Django server
* `practicity/progressTracker` contains the App for the websever in which musicians can track their practice progress. The heart of the functionality.

<hr>
<div style="text-align:center;">
<img src="./docu/practicity_logo.PNG" alt="logo image" style="width:30%;height:30%;">
</div>