class UserUniqueConstraintException(Exception):
    def __init__(self, field, message):
        self.field = field
        self.message = message
        super().__init__(self.message)


class UserDoesNotExists(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class InvalidTokenError(EOFError):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
