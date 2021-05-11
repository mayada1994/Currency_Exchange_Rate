import sqlite3
import os
from flask import Flask

# config
DATABASE = '/tmp/currency_exchange_rate.db'
DEBUG = True
SECRET_KEY = 'mdgfh78@#5?>ashf89hx,v06k'

app = Flask(__name__)
app.config.from_object(__name__)

app.config["APPLICATION_ROOT"] = "/migration"
app.config.update(dict(DATABASE=os.path.join(app.root_path, 'currency_exchange_rate.db')))


def connect_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn


def create_db():
    db = connect_db()
    with app.open_resource('currency_rate_data_set_csv.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()


# generates database from data in currency_rate_data_set_csv.sql
if __name__ == '__main__':
    create_db()
