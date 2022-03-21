# HackOverflow - Pawsitivity
## Running the Code
1. Open up your terminal in VS Code (Terminal -> New Terminal)
- `python manage.py makemigrations`
- `python manage.py migrate`
    - If you're working on the front-end, these should likely not do anythin
- `python manage.py runserver`
2. Now you should be able to open a browser window and go to `localhost:8000`
3. As you update your code, the browser will automatically update (unless it has a major issue)
4. Make sure you stop the server when you're done! The easy way is going back to the terminal and pressing either CTRL-C or CMD-C

## Configuring Dev. Environment

Since the project uses postgreSQL, there is a bit more setup required on the dev side to properly configure the environment.

### postgreSQL Setup
1. Install postgreSQL (if not already installed): https://www.postgresql.org/download/
    - Default settings are ok (and preferred)
    - Password is up to you to create and remember
2. Open postgreSQL by going to your app launcher (Windows -> start menu, Mac -> search bar) and type in "sql". The app is called "SQL Shell (psql)"
    - When you open there will be a sequence of prompts. The items in square brackets will be what's used if you don't type anything and just hit ENTER, so do that for every option except password (which is what you configured in step 1)
    - Now run the following commands to setup the local database:
        - `CREATE DATABASE hoverflowdb;`
        - `CREATE USER admin WITH ENCRYPTED PASSWORD 'c2DsgVyP5q6Jjn';`
        - `ALTER ROLE admin SET client_encoding TO 'utf8';`
        - `ALTER ROLE admin SET default_transaction_isolation TO 'read committed';`
        - `ALTER ROLE admin SET timezone TO 'UTC';`
        - `GRANT ALL PRIVILEGES ON DATABASE hoverflowdb TO admin;`
        - Then you're done, so enter `\q` to exit the shell
### Python Package Setup
3. Install all the packages using:
    - `pip install -r requirements.txt` (Windows)
    - `pip3 install -r requirements.txt` (Mac)
4. Run `python manage.py migrate` from the shell and you should be good to go!
## Editing SQL Database to match new migrations

If you pull in main or switch to a new branch, chances are that there will be migrations to make that will conflict with your local database's structure. Here's how to fix that.
1. Log into shell
    - Look for app "sql" and choose "SQL Shell (psql)"
    - The square brackets are the defaults, so hit enter to apply the defaults where applicable. Then use username 'admin' and the password found in ![settings.py](./hackoverflow/settings.py) under `DATABASES['DEFAULT']`
2. Connect to our database by running `\c hoverflowdb`
3. Delete the migrations in the database for the app(s) conflicting
    - `DELETE from django_migrations WHERE app='<APPNAME>';`
        - Replace <APPNAME> with the culprit's name
        - Re-run command for every conflicting app
4. Back in Python, delete the migrations folder(s)
5. In the terminal, run:
    - `python manage.py migrate --run-syncdb`
    - `python manage.py makemigrations <APPNAME>`
        - Again, replace <APPNAME> with the culprit's name
        - Re-run for every conflicting app
    - `python manage.py migrate --fake`
6. You should be good to run the server and go!

**Note:** If there are still issues after trying this, do this instead:
1. Log into shell with your main account (postgres is the default name)
2. Delete our database
    - `DROP DATABASE hoverflowdb;`
3. Restart at part 2 of the Setup instructions

## Testing
### Writing Tests

Recommend following: https://docs.djangoproject.com/en/4.0/intro/tutorial05/

### Running Tests

`python manage.py test <APP_NAME>`

- Note: you might get this error: `Got an error creating the test database: permission denied to create database`
    - Log into sql shell under your root (main) account.
    - Add the createdb permission to our 'admin' user:
        - `ALTER USER admin CREATEDB;`
