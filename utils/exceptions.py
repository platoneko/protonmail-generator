class EmailMethodForVerificationDisabled(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class NotAvailableDomainException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class GettingVerificationCodeException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class SkipAdvIncomplete(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class RecoveryEmailProblemException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class VerifyException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
