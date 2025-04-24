class BadRequestsError(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message
class ResourceNotFound(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message

class InvalidTokenFormat(Exception):
    def __init__(self, message="The token format is invalid. Expected: Bearer <token>"):
        self.message = message
        super().__init__(self.message)

class TokenMissing(Exception):
    def __init__(self, message="Authorization token is missing"):
        self.message = message
        super().__init__(self.message)

class TokenExpired(Exception):
    def __init__(self, message="The token has expired"):
        self.message = message
        super().__init__(self.message)

class TokenInvalid(Exception):
    def __init__(self, message="The token is invalid"):
        self.message = message
        super().__init__(self.message)
