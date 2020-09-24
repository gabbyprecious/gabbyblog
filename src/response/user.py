def success_response(data: list = [], code: int = 200, message: str = "Empty list returned") -> dict:
    return {
        "data": data,
        "code": code,
        "message": message
    }


def error_response(data: str = "An Error Occurred", code: int = 400, message: str = "An error occured.") -> dict:
    return {
        "error": data,
        "code": code,
        "message": message
    }

def token_response(token: str):
    return {
        "access_token": token
    }