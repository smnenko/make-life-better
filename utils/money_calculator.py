from schemas.money import MoneyRetrieveAllSchema


def get_calculated_totals(monies: MoneyRetrieveAllSchema):
    result_dict = monies.dict()
    result_dict.update({
        'total_incomes': monies.get_total_incomes(),
        'total_outlays': monies.get_total_outlays()
    })
    return result_dict
