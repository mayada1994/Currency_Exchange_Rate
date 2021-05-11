import warnings

from pandas import read_csv

from application.controller.currency_rate_controller import app
from currency_rate import CurrencyRate
from rnn import *

TRAINING_PERCENTAGE = 0.7
TESTING_PERCENTAGE = 1 - TRAINING_PERCENTAGE
NUMBER_OF_PREVIOUS_DATA_POINTS = 3
LENGTH_DATA_SET = 0
TRAINING_SET_LENGTH = 0
TESTING_SET_LENGTH = 0
CURRENCY_RATE_ROW = 'Офіційний курс гривні, грн'
EXCHANGE_DATE_ROW = 'Дата'
CURRENCY_VALUE_ROW = 'Код літерний'
CURRENCY_UNIT_ROW = 'Кількість одиниць'


def get_raw_data(data_set_frame, currency):
    data_set_frame = data_set_frame[data_set_frame[CURRENCY_VALUE_ROW] == currency]
    data_set_frame = data_set_frame.drop(
        data_set_frame.columns.difference([EXCHANGE_DATE_ROW, CURRENCY_UNIT_ROW, CURRENCY_RATE_ROW]), 1)
    row_data = []
    for row in data_set_frame.to_records().tolist():
        row_data.append(CurrencyRate(date=row[0], currency=currency, rate=row[2] / row[1]))
    return row_data


def main():
    data_set_frame = read_csv('currency_rate_data_set.csv', header=0,
                              index_col=0, squeeze=True)
    currencies = list(dict.fromkeys(data_set_frame[CURRENCY_VALUE_ROW]))
    currency = input('Enter any one of [' + str(currencies)[1:-1] + '] currencies: \n').strip()

    raw_data = get_raw_data(data_set_frame, currency)
    rnn_model(raw_data, currency)


if __name__ == '__main__':
    warnings.filterwarnings("ignore")
    main()
    app.run(debug=True, port=8080)
