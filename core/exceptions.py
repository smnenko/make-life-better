class ObjectAlreadyExistsError(Exception):
    def __init__(self, field, message):
        self.field = field
        self.message = message
        super().__init__(self.message)


class ObjectDoesNotExists(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class InvalidTokenError(EOFError):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
