from fastapi.responses import JSONResponse


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
