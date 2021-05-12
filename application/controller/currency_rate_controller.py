import datetime

from flask import Flask, render_template, request

from currency_rate import CurrencyRate
from migration.db_utils import get_db
from rnn import rnn_model

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0


@app.route("/", methods=["GET"])
def index():
    db = get_db()
    cur = db.execute('SELECT DISTINCT currency FROM currency_rates')
    currency = cur.fetchall()
    return render_template("index.html", currency_value=currency)


@app.route("/rate", methods=["POST"])
def get_currency_rate():
    currency = request.form.get('currency')
    date = request.form.get('date')

    new_date = datetime.datetime.strptime(date, '%Y-%m-%d').strftime('%d.%m.%Y')

    db = get_db()
    cur = db.execute('SELECT * FROM currency_rates')
    currency_rates = cur.fetchall()
    all_currency_rates = []
    for row in currency_rates:
        all_currency_rates.append(CurrencyRate(date=row[0], currency=row[1], rate=row[3] / row[2]))

    selected_rates = []
    for i, result in enumerate(all_currency_rates):
        if result.Date == new_date:
            selected_rates = (all_currency_rates[i - 50: i + 1])
            break

    result = rnn_model(selected_rates, currency, selected_rates[-1])

    return render_template("result.html",
                           date=result.date,
                           actualRate=result.actual_rate,
                           predictedRate=result.predicted_rate,
                           error=result.error,
                           currency=currency,
                           url="/static/testing_prediction_rnn.png",
                           currency_value=currency

    )

@app.after_request
def add_header(response):
    response.cache_control.max_age = 0
    return response
