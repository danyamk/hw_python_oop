import datetime as dt


class Calculator:
    def __init__(self, limit: float):
        self.limit = limit
        self.current_date = dt.date.today()
        self.records = []

    def add_record(self, Record):
        self.records.append(Record)

    def get_today_stats(self):
        today_status = 0
        for record in self.records:
            if record.date == self.current_date:
                today_status += record.amount
        return today_status

    def get_week_stats(self):
        sum: float = 0
        week_ago = self.current_date - dt.timedelta(days=7)
        for record in self.records:
            if self.current_date >= record.date >= week_ago:
                sum += record.amount
        return sum


class Record:
    def __init__(self, amount, comment, date: str = None):
        self.amount = amount
        self.comment = comment
        if date is None:
            self.date = dt.date.today()
        else:
            self.date = dt.datetime.strptime(date, "%d.%m.%Y").date()
    pass


class CashCalculator(Calculator):
    USD_RATE = 1 / 73.15
    EURO_RATE = 1 / 86.81

    def __init__(self, limit: float):
        super().__init__(limit)

    def get_today_cash_remained(self, currency):
        today_sum = self.get_today_stats()
        remains = self.limit - today_sum
        if remains == 0:
            return('Денег нет, держись')
        if currency == 'rub':
            currency = 'руб'
        elif currency == 'usd':
            currency = 'USD'
            remains *= self.USD_RATE
        elif currency == 'eur':
            currency = 'Euro'
            remains *= self.EURO_RATE
        print(remains)
        if remains > 0:
            return f'На сегодня осталось {round(remains, 2)} {currency}'
        else:
            return ('Денег нет, держись: твой долг -'
                    f'{abs(round(remains, 2))} {currency}')


class CaloriesCalculator(Calculator):
    def __init__(self, limit: float):
        super().__init__(limit)

    def get_calories_remained(self):
        if self.limit == -1 or self.limit == 0:
            pass
        total = 0
        for record in self.records:
            if record.date == self.current_date:
                total += record.amount
        if total < self.limit:
            remains = self.limit - total
            return ('Сегодня можно съесть что-нибудь ещё, '
                    f'но с общей калорийностью не более {remains} кКал')
        else:
            return ('Хватит есть!')


# создадим калькулятор денег с дневным лимитом 1000
cash_calculator = CashCalculator(-1)

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

print(cash_calculator.get_today_cash_remained('usd'))
# должно напечататься
# На сегодня осталось 555 руб
