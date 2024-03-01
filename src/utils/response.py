from fastapi.responses import JSONResponse
from ..exception import AuthError


class CustomResponse:
    def __init__(self, status_code, message, data=None, error=None):
        self.status_code = status_code
        self.message = message
        self.data = data or {}
        self.error = error or ""

    def to_dict(self):
        return JSONResponse(
            status_code=self.status_code,
            content={
                "message": self.message,
                "data": self.data,
                "errors": self.error,
            },
        )


class HandleException:
    def __init__(self, message: str, exception: Exception) -> None:
        self.status_code = 401 if isinstance(exception, AuthError) else 400
        self.message = message
        self.error = str(exception)

    def send_response(self):
        return CustomResponse(
            status_code=self.status_code, message=self.message, error=self.error
        ).to_dict()
