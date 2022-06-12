class EvaluatorException(Exception):
    """
    Base class for Evaluator Exceptions
    """
    def __init__(self, error_type: str, errors: str):
        self.errors = errors
        self.error_type = error_type
        super().__init__(error_type)

    def __str__(self):
        return f"{self.error_type}: {self.errors}"


class FailedEvaluation(EvaluatorException):
    def __init__(self, tried: str | list = None):

        super().__init__(type(self).__name__, f"Cannot evaluate {tried} into datetime")


class InvalidValue(EvaluatorException):
    def __init__(self, value: str):

        super().__init__(type(self).__name__, f"{value}")
