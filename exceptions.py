from fastapi import HTTPException


class BaseHTTPExceptions(HTTPException):
    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class UrlDoesNotExist(BaseHTTPExceptions):
    detail = 'Url record does not exist in db'
    status_code = 404


class RequestDoesNotExist(BaseHTTPExceptions):
    detail = 'Request record does not exist in db'
    status_code = 404
