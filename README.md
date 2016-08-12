# Chefs Django REST

This project is REST service to manage a social network about the recipes created by JuanLSanchez.

The administration of the project is with git-flow and the branches _master_, _develop_, _feature/*_, _hotfix/*_ and _release_.

The enumeration of the version have three integers 1.2.3:

1. The compatibility version where the version 1 and version 2 aren't compatibility.
2. Great modifications.
3. Small modifications. 

## Requirements

* Virtualenv
* Python 3.4

## Installation in development environment

```bash
# Create the environment 
virtualenv -p python3.4 env
# Load the environment 
source env/bin/activate
# Load the dependencies 
pip install -r requirements.txt 
# Make the sqlite database 
python manage.py migrate
# Run the server 
python manage.py runserver
```

