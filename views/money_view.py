from fastapi import Request


class MoneyView:

    @classmethod
    def get_all_for_user(cls, user_id: int, request: Request):
        pass
