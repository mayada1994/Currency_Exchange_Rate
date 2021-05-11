class CurrencyRateDataBase:
    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()

    def get_exchange_rates_for_currency(self, selected_currency):
        sql = '''SELECT * FROM currency_rates WHERE currency = {selected_currency}'''
        try:
            self.__cur.execute(sql)
            res = self.__cur.fetchall()
            if res: return res
        except:
            print("db read error")
        return []
