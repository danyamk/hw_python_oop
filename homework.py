import datetime as dt


class Record:
    def __init__(self, amount: float, comment: str, date=None):
        self.amount = amount
        self.comment = comment
        if date is None:
            self.date = dt.date.today()
        else:
            self.date = dt.datetime.strptime(date, "%d.%m.%Y").date()


class Calculator:
    def __init__(self, limit: float):
        self.limit = limit
        self.current_date = dt.date.today()
        self.records = []
        self.week_ago = self.current_date - dt.timedelta(days=7)

    def add_record(self, Record):
        self.records.append(Record)

    def get_today_stats(self):
        return sum(record.amount for record in self.records 
            if record.date == self.current_date)

    def get_week_stats(self):
        return sum(record.amount for record in self.records
            if self.current_date >= record.date >= self.week_ago)

    def get_remains(self):
        return self.limit - self.get_today_stats()


class CashCalculator(Calculator):
    USD_RATE = 73.15
    EURO_RATE = 86.81
    RUB_RATE = 1

    def __init__(self, limit: float):
        super().__init__(limit)

    def get_today_cash_remained(self, currency):
        remains = self.get_remains()
        if remains == 0:
            return('Денег нет, держись')
        db_currency = {
            "rub": ("руб", self.RUB_RATE),
            "usd": ("USD", self.USD_RATE),
            "eur": ("Euro", self.EURO_RATE),
        }
        if currency in db_currency:
            currency, rate = db_currency[currency]
            remains = round(remains / rate, 2)
            remains_abs = abs(remains)
            if remains > 0:
                return f'На сегодня осталось {round(remains, 2)} {currency}'
            else:
                return ('Денег нет, держись: твой долг - '
                        f'{remains_abs} {currency}')


class CaloriesCalculator(Calculator):
    def __init__(self, limit: float):
        super().__init__(limit)

    def get_calories_remained(self):
        remains = self.get_remains()
        if self.get_today_stats() < self.limit:
            return ('Сегодня можно съесть что-нибудь ещё, '
                    f'но с общей калорийностью не более {remains} кКал')
        else:
            return ('Хватит есть!')


if __name__ == "__main__":
    # создадим калькулятор денег с дневным лимитом 1000
    cash_calculator = CashCalculator(1)

    # дата в параметрах не указана,
    # так что по умолчанию к записи
    # должна автоматически добавиться сегодняшняя дата
    cash_calculator.add_record(Record(amount=145, comment='кофе'))
    # и к этой записи тоже дата должна добавиться автоматически
    cash_calculator.add_record(Record(amount=300, comment='Серёге за обед'))
    # а тут пользователь указал дату, сохраняем её
    cash_calculator.add_record(Record(amount=3000,
                                    comment='бар в Танин др',
                                    date='10.08.2021'))

    print(cash_calculator.get_today_cash_remained('eur'))
    # должно напечататься
    # На сегодня осталось 555 руб
