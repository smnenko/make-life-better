from typing import List

from models.money import Money, MoneyType


class MoneyTotalsCalculator:

    def __init__(self, monies: List[Money]):
        self.monies = monies

    def get_total_incomes(self):
        return sum([
            i.amount
            for i in self.monies
            if i.type == MoneyType.income
        ])

    def get_total_outlays(self):
        return sum([
            i.amount
            for i in self.monies
            if i.type == MoneyType.outlay
        ])

    def get_tuple_result(self):
        return self.get_total_incomes(), self.get_total_outlays()
