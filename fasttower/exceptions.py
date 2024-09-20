from fastapi import HTTPException


class NotFoundException(HTTPException):
    def __init__(self, status_code=404, detail="Not Found"):
        super().__init__(status_code, detail)


class ImproperlyConfigured(Exception):
    """FastTower is somehow improperly configured"""

    pass
