# HackOverflow - Pawsitivity
## Deployment Steps
### Configuring Dev. Environment
#### postgreSQL Setup
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

#### Python Package Setup
1. While in the project directory, install all the packages using:
   - `pip install -r requirements.txt` (Windows)
   - `pip3 install -r requirements.txt` (Mac)

If running the code gives an error for lacking a package, simply run `pip install <PACKAGE_NAME>` (or `pip3` on Mac)

### Running the Code
1. Open up your terminal while in the project directory. We need to initialize the django models to our postgreSQL database:
- Note: replace `python` with `python3` if on Mac (on all relevant steps)
- `python manage.py makemigrations messaging`
- `python manage.py makemigrations store`
- `python manage.py migrate`
- `python manage.py runserver`
2. Now you should be able to open a browser window and go to `localhost:8000`
4. Make sure you stop the server when you're done! The easy way is going back to the terminal and pressing either CTRL-C or CMD-C

### Adding Content
Adding profiles:
1. Navigate the site as a normal user, and create an account.
2. Once your account is created, go to your profile page to edit your profile information.

Adding products:
1. In the python terminal, run: `python manage.py createsuperuser`. Enter the information you'd like for an 'admin' account.
2. Navigate to `localhost:8000/admin`, and login using your new admin credentials.
3. Find the Product model, and click "Add" - now you can add products to populate the store page!

## Editing SQL Database to match new migrations
If you pull in main or switch to a new branch, chances are that there will be migrations to make that will conflict with your local database's structure. The easiest way to fix that is just deleting your database and remaking it from scratch.

1. Log into shell with your main account (postgres is the default username)
2. Delete our database
   - `DROP DATABASE hoverflowdb;`
3. Recreate the database
   - `CREATE DATABASE hoverflowdb;`
   - `GRANT ALL PRIVILEGES ON DATABASE hoverflowdb TO admin;`
   - Then you're done, so enter `\q` to exit the shell
4. Delete the migrations folder in all of the apps.
5. Delete the media folder, if it exists.
6. Run `python manage.py makemigrations <APP_NAME>` for every app.
7. Run `python manage.py migrate`.
8. Run `python manage.py runserver` and you're good to go!

## Testing
### Writing Tests
Recommend following: https://docs.djangoproject.com/en/4.0/intro/tutorial05/
### Running Tests
`python manage.py test <APP_NAME>`
- Note: you might get this error: `Got an error creating the test database: permission denied to create database`
  - Log into sql shell under your root (main) account.
  - Add the createdb permission to our 'admin' user:
    - `ALTER USER admin CREATEDB;`

### Tokens

| Emoji | Name        | Unicode |
| ----- | ----------- | ------- |
| 🐶    | dog face    | U+1F436 |
| 🐱    | cat face    | U+1F431 |
| 🦋    | butterfly   | U+1F98B |
| 🐢    | turtle      | U+1F422 |
| 🦄    | unicorn     | U+1F984 |
| 🐰    | rabbit face | U+1F430 |
| 🐾    | paw prints  | U+1F43E |
| 🦩    | flamingo    | U+1F9A9 |
| 🦈    | shark       | U+1F988 |
| 🦖    | T-Rex       | U+1F996 |
