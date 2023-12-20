# Spam API Project using Django REST Framework

## How to run it:

1. Install all project requirements by opening a terminal inside SpamAPI project folder and running the command:
        
        pip install -r requirements.txt
2. After the requirements are installed, run these commands:

        python manage.py makemigrations
        python manage.py migrate
3. If everything returns ok, then run this command to populate the data in the DB:

        python manage.py initdata
4. Create an admin user account by running the command:

        python manage.py createsuperuser
    Input a phone number and password as the credentials for when you need to access the django admin console.


5.  Run the server using cmd:

        python manage.py runserver
6. Access the admin panel by visiting the url: `{local ip:8000}/admin`


7. Access the api endpoints by typing `api/<function>`


8. When accessing other functions which require authentication, add authorization header inside the header of the request. (In postman, click on header section)

        Authorization :  Token <Token Value>

## API REQUEST FORMAT

### 1. To register

**POST** `api/register`

        {
            "phone": null,      //must not be null
            "username": "",
            "password": "",
            "email": ""         //optional
        }

### 2. Login

**POST** `api/login`

        {
            "phone":""
            "password":"'
        }

### 3. Submit number as Spam

**PUT** `api/submit-spam`      _Requires Authorization Token_

        {
            phone:""
        }

### 4. Search for contact via Name

**GET** `api/search-name`         _Requires Authorization Token_       

        {
            name:""
        }

### 5. Search for contact via phone number

**GET** `api/search-number`   _Requires Authorization Token_  

        {
            phone:""
        }