from fastapi.responses import JSONResponse
import logging
import traceback

logger = logging.getLogger(__name__)


def create_error_response(
        status_code: int,
        message: str,
):
    """
    Create error response for the API.
    :param status_code:
    :param message:
    :return:
    """
    error_trace = traceback.format_exc()
    if error_trace:
        logger.error(f"Error: {message}\nTraceback: {error_trace}")
        return JSONResponse(
            status_code=status_code,
            content={
                "code": status_code,
                "message": message,
                "traceback": error_trace
            }
        )
    else:
        logger.error(f"Error: {message}")
        return JSONResponse(
            status_code=status_code,
            content={
                "code": status_code,
                "message": message
            }
        )
