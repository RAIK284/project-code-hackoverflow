# HackOverflow - Pawsitivity
## Configuring Dev. Environment

Since the project uses postgreSQL, there is a bit more setup required on the dev side to properly configure the environment.

### postgreSQL Setup
1. Install postgreSQL (if not already installed): https://www.postgresql.org/download/
    - Default settings are ok (and preferred).
    - Password is up to you to create and remember.
2. Open postgreSQL by going to your app launcher (Windows -> start menu, Mac -> search bar) and type in "sql". The app is called "SQL Shell (psql)"
    - When you open there will be a sequence of prompts. The items in square brackets will be what's used if you don't type anything and just hit ENTER, so do that for every option except password (which is what you configured in step 1).
    - Now run the following commands to setup the local database:
        - `CREATE DATABASE hoverflowdb;`
        - `CREATE USER admin WITH ENCRYPTED PASSWORD 'c2DsgVyP5q6Jjn';`
        -  `ALTER ROLE myuser SET client_encoding TO 'utf8';`
        - `ALTER ROLE myuser SET default_transaction_isolation TO 'read committed';`
        - `ALTER ROLE myuser SET timezone TO 'UTC';`
        - `GRANT ALL PRIVILEGES ON DATABASE mydb TO myuser;`
        - Then you're done, so enter `\q` to exit the shell.
### Python Package Setup
3. Install all the packages using:
    - `pip install -r requirements.txt` (Windows)
    - `pip3 install -r requirements.txt` (Mac)
4. Run `python manage.py migrate` from the shell and you should be good to go!
