from fastapi import Request

from permissions.user_permission import authenticated_permission


class MoneyView:

    @classmethod
    @authenticated_permission
    def get_all_for_user(cls, user_id: int, request: Request):
        pass
