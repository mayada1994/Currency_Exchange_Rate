import os

import numpy
from keras.layers import Dense
from keras.models import Sequential
from matplotlib import pyplot
from tensorflow.python.keras.models import load_model

TRAINING_PERCENTAGE = 0.7
TESTING_PERCENTAGE = 1 - TRAINING_PERCENTAGE
NUMBER_OF_PREVIOUS_DATA_POINTS = 3
LENGTH_DATA_SET = 0
numpy.random.seed(7)
TRAINING_SET_LENGTH = 0
TESTING_SET_LENGTH = 0
RECURRENT_NEURAL_NETWORK_MODEL = 'rnn_model.h5'


def training_testing_buckets(raw_data, training_percentage):
    global TRAINING_SET_LENGTH, TESTING_SET_LENGTH
    TRAINING_SET_LENGTH = int(LENGTH_DATA_SET * training_percentage)
    TESTING_SET_LENGTH = LENGTH_DATA_SET - TRAINING_SET_LENGTH
    training_set, testing_set = raw_data[0:TRAINING_SET_LENGTH], raw_data[TRAINING_SET_LENGTH:LENGTH_DATA_SET]
    return training_set, testing_set


def modify_data_set_rnn(training_set, testing_set):
    train_actual = []
    train_predict = []
    for interval in range(len(training_set) - NUMBER_OF_PREVIOUS_DATA_POINTS - 1):
        train_actual.append(training_set[interval: interval + NUMBER_OF_PREVIOUS_DATA_POINTS])
        train_predict.append(training_set[interval + NUMBER_OF_PREVIOUS_DATA_POINTS])

    test_actual = []
    test_predict = []
    for interval in range(len(testing_set) - NUMBER_OF_PREVIOUS_DATA_POINTS - 1):
        test_actual.append(testing_set[interval: interval + NUMBER_OF_PREVIOUS_DATA_POINTS])
        test_predict.append(testing_set[interval + NUMBER_OF_PREVIOUS_DATA_POINTS])

    return train_actual, train_predict, test_actual, test_predict


def build_recurrent_neural_network(train_actual, train_predict):
    recurrent_neural_network = Sequential()

    recurrent_neural_network.add(Dense(12, input_dim=NUMBER_OF_PREVIOUS_DATA_POINTS, activation="relu"))
    recurrent_neural_network.add(Dense(8, activation="relu"))
    recurrent_neural_network.add(Dense(1))

    recurrent_neural_network.compile(loss='mean_squared_error', optimizer='adam')
    recurrent_neural_network.fit(numpy.array(train_actual), numpy.array(train_predict), epochs=50, batch_size=2,
                                 verbose=2)

    recurrent_neural_network.save(RECURRENT_NEURAL_NETWORK_MODEL)
    return recurrent_neural_network


def predict_rnn(recurrent_neural_network, train_actual, test_actual):
    training_predict, testing_predict = recurrent_neural_network.predict(numpy.array(train_actual)), \
                                        recurrent_neural_network.predict(numpy.array(test_actual))

    print(training_predict, testing_predict)
    print('\t The prediction for the next day:', testing_predict[-1])
    return training_predict, testing_predict


def evaluate_performance_rnn(recurrent_neural_network, test_actual, test_predict):
    mse_testing = recurrent_neural_network.evaluate(numpy.array(test_actual), numpy.array(test_predict), verbose=0)
    print('\t Testing Mean Square Error:', mse_testing)


def plot_rnn(currency, raw_data, training_predict, testing_predict, file_name):
    training_data_trend = [None] * LENGTH_DATA_SET
    testing_data_trend = [None] * LENGTH_DATA_SET

    training_data_trend[NUMBER_OF_PREVIOUS_DATA_POINTS:len(training_predict) + NUMBER_OF_PREVIOUS_DATA_POINTS] = \
        list(training_predict[:, 0])
    testing_data_trend[NUMBER_OF_PREVIOUS_DATA_POINTS - 1:len(training_predict) + NUMBER_OF_PREVIOUS_DATA_POINTS] = \
        list(testing_predict[:, 0])

    # actual
    pyplot.plot(raw_data[int(TRAINING_PERCENTAGE * LENGTH_DATA_SET):], label="Actual data points",
                color="blue")
    # training
    # pyplot.plot(training_data_trend, label="Training prediction", color="green")

    # testing
    pyplot.plot(testing_data_trend, label="Testing prediction", color="red")

    pyplot.ylabel('currency values for 1 UAH')
    pyplot.xlabel('number of days')
    pyplot.title('UAH/' + currency + ' : actual vs predicted using RNN')

    pyplot.legend()
    # pyplot.show()
    pyplot.savefig(file_name)
    pyplot.clf()


def rnn_model(raw_data, currency):
    print('\nNeural Network Model')

    print('Loading the data set...')
    raw_data = [currency_rate.Rate for currency_rate in raw_data]

    global LENGTH_DATA_SET
    LENGTH_DATA_SET = len(raw_data)

    global RECURRENT_NEURAL_NETWORK_MODEL
    RECURRENT_NEURAL_NETWORK_MODEL = 'rnn_model_{currency}.h5'.format(currency=currency.lower())

    print('Splitting training and testing set...')
    training_set, testing_set = training_testing_buckets(raw_data, TRAINING_PERCENTAGE)
    train_actual, train_predict, test_actual, test_predict = modify_data_set_rnn(training_set, testing_set)

    if os.path.isfile(RECURRENT_NEURAL_NETWORK_MODEL):
        print('Loading model...')
        rnn = load_model(RECURRENT_NEURAL_NETWORK_MODEL)
    else:
        print('Building and training model...')
        rnn = build_recurrent_neural_network(train_actual, train_predict)

    print('Predicting...')
    training_predict, testing_predict = predict_rnn(rnn, train_actual, test_actual)

    print('Evaluating performance...')
    evaluate_performance_rnn(rnn, test_actual, test_predict)

    print('Plotting the graph...')
    plot_rnn(currency, raw_data, training_predict, testing_predict, "testing_prediction_rnn.pdf")

    print('Done...')
    return training_predict, testing_predict
