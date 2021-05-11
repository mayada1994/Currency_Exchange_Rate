from flask import Flask, render_template, request

from migration.db_utils import get_db

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    db = get_db()
    cur = db.execute('SELECT DISTINCT currency FROM currency_rates')
    currency = cur.fetchall()
    return render_template("index.html", currency=currency)


@app.route("/rate", methods=["POST"])
def get_currency_rate(currency, date):
    return request.query_string
