import structlog
import time
from typing import Callable, Any

logger = structlog.getLogger(__name__)



def log_debug(func: Callable[..., Any]) -> Callable[..., Any]:
    def wrapper(*args, **kwargs):
        logger = structlog.getLogger(func.__name__)
        logger.debug(f" >>>> {func.__name__}")
        logger.debug(f" ..with params={{{args}}}")
        start_time = time.time()
        ret_val = func(*args, **kwargs)
        end_time = time.time()
        logger.debug(
            f" <<<< {func.__name__} and took {end_time-start_time:.3f} seconds"
        )
        logger.debug(f" ..with ret_val={{{ret_val}}}")
        return ret_val

    return wrapper


def extract_error_msg_from_traceback_exc(format_exc) -> str:
    try:
        return format_exc.splitlines()[-1].split(": ")[1:][0]
    except Exception:
        logger.error(f"Failed to extract error message from traceback: {format_exc}")
        return "Unknown error"