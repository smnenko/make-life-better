from typing import List

from models.calorie import CalorieRecord


class CalorieCalculator:

    def __init__(self, calories: List[CalorieRecord]):
        self.calories = calories
        self.used_calories = None
        self.left_calories = None

    def get_used_calories(self):
        if self.calories:
            self.used_calories = sum([
                i.amount * i.dish.calorie / 100
                for i in self.calories
            ])
            return self.used_calories
        return None

    def get_left_calories(self):
        dates = [i.date for i in self.calories]
        if dates:
            start_date, end_date = min(dates), max(dates)
            self.left_calories = (
                (end_date - start_date).days * 2000 - self.used_calories
                if self.used_calories else None
            )
            return self.left_calories
        return None

    def get_statistics(self):
        return self.get_used_calories(), self.get_left_calories()
