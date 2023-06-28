from starlette.responses import JSONResponse

from src.image.errors import ImageNotFound, ImageDecodeError


def setup_exception_handlers(app):

    @app.exception_handler(Exception)
    async def generic_error_handler(_, exc: Exception):
        return JSONResponse(**generate_error_response(50001, exc))

    @app.exception_handler(ImageNotFound)
    async def image_not_found_error_handler(_, exc: ImageNotFound):
        return JSONResponse(**generate_error_response(40401, exc))

    @app.exception_handler(ImageDecodeError)
    async def image_decode_error_handler(_, exc: ImageDecodeError):
        return JSONResponse(**generate_error_response(40001, exc))


def generate_error_response(code, exc):
    status_code = code // 100
    error_message = str(exc)

    return {
        'content': {
            'error': {
                'code': code,
                'message': error_message
            }
        },
        'status_code': status_code
    }
