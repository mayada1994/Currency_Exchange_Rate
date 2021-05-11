class CurrencyRate:

    def __init__(self, date, currency, rate):
        self.Date = date
        self.Currency = currency
        self.Rate = rate

    def __str__(self):
        return "CurrencyRate(date={date} , currency={currency} , rate={rate})".format(date=self.Date,
                                                                                      currency=self.Currency,
                                                                                      rate=self.Rate)
