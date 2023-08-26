# MixRec
## Installation
First, install all necessary dependencies. Note that the recommended versions are python 3.11
and postgres 14.
```shell
sudo apt install git python3 postgresql python3-virtualenv
```
### Python
While it is not necessary, it is recommended to work with a python virtual environment.
We create the environment using virtualenv but there exists other options such as conda.
In the root of the project, execute the following commands:
```shell
virtualenv -p python3 venv        # create a new virtual environment in the directory 'venv'
source venv/bin/activate          # temporarily set venv python as the default
pip3 install -r requirements.txt  # install python dependencies (found in requirements.txt file)
```

### Postgres
```shell
sudo su postgres
psql
```
Create the SQL objects:
```sql
CREATE USER mixrec WITH SUPERUSER PASSWORD 'pw_mixrec';
CREATE DATABASE mixrec_db OWNER mixrec;
```

Next, we have to trust the database. This can be done by editing the `pg_hba.conf` file, 
which can be found in `/etc/postgresql/14/main/pg_hba.conf`. Open it in a text editor or in terminal
using nano (or other options). __It needs to be the first rule (above local all all peer)__.
```shell
sudo nano /etc/postgresql/14/main/pg_hba.conf
```
Scroll all the way down and add the following lines.
```
# TYPE  DATABASE        USER            ADDRESS                 METHOD

# our database
local   mixrec_db       mixrec                                  trust
```

Lastly, restart the database service to accommodate the changes made in the `pg_hba.conf` file.
```shell
sudo systemctl restart postgresql
```
You can check if everything worked correctly by executing:
```shell
sudo systemctl status postgresql
```
There should be a (green) line displaying:  Active: active

# Running the backend
To run the backend, execute the following commands in the root of the project
```shell
source venv/bin/activate
python ./backend/manage.py runserver
```

# Running the frontend
To run the frontend, execute the following commands in the root of the project
```shell
cd mix_rec_client
npm install
npm start
```

