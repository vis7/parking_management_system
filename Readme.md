# Car Parking Management System

# Features (Backend)
Develop an API for showing booked parking spaces and also let user booking parking space on a particular date.

Constraints for booking parking space are as follows:-
- User can only book single parking space on any given date
- Booking should be made 24 hrs in advance
- The parking lot has 4 spaces and only 4 slots are available for any parking space
- Develop API for user login,  signup and logout

# Setup
Run below steps for setup
```
# To create and virtualenv and install all it's dependency
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt

# For migrations
python manage.py makemigrations
python manage.py migrate

# To load fixtures (in case you want)
python manage.py loaddata accounts/fixtures/users.json

# Create superuser
python manage.py createsuperuser
```

Import postman collection and environment from "postman" folder

# Run
To run project
```
python manage.py runserver
```

To run tests
```
python manage.py test
```

To reformat explictly code
```
```

# API Documentation
Run project and go to `http://127.0.0.1:8000/swagger/`


# Doc
# Assumption
- For the purpose of this project default user is sufficient but still we created our own User class by extending AbstractUser class of Django, Becase if we want to add diffrent types of users or modify funtionlity of user we can do it easily, without affecting existing database in production.
- User account is directly get activate without need to verify email
-
