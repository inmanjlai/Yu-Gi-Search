## How to get this starter up and running:

### Dependencies needed:
- PostgreSQL for the database
- Python and Pip/Pipenv
- .env file to provide DATABASE_URL variable

1. Clone this repository.
2. ```cd``` into Yu-Gi-Search.
3. Run ```pipenv install flask flask-sqlalchemy psycopg2-binary python-dotenv requests flask-migrate``` to initialize your virtual environment and install all dependencies.
4. Run ```pipenv shell``` to activate virtual environment
5. Run ```flask db init```, ```flask db migrate``` and ```flask db upgrade``` to initialize a migration folder, migrate the database models and apply changes to your database.
6. Use ```flask run``` to start the application.
5. Enjoy!


##TODO:

-Make user login and signup

-Allow users to comment on cards

-Make a collection for users

-Make a deck builder

-Create a forum

