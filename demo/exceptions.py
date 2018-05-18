class ValidationError(Exception):
    """
    Custom validation error exception
    """
    def __init__(self, errors, *args, **kwargs):
        self.errors = errors
