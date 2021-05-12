class PredictionResult:

    def __init__(self, date, actual_rate, predicted_rate, error, currency, url_to_graph):
        self.date = date
        self.actual_rate = actual_rate
        self.predicted_rate = predicted_rate
        self.error = error
        self.currency = currency
        self.url_to_graph = url_to_graph

