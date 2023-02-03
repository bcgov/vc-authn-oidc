import logging
import time


from typing import Callable, Any


def log_debug(func: Callable[..., Any]) -> Callable[..., Any]:
    def wrapper(*args, **kwargs):
        logger = logging.getLogger(func.__name__)
        logger.setLevel(logging.DEBUG)
        logger.info(f" >>>> {func.__name__}")
        logger.debug(f" ..with params={{{args}}}")
        start_time = time.time()
        ret_val = func(*args, **kwargs)
        end_time = time.time()
        logger.info(f" <<<< {func.__name__} and took {end_time-start_time:.3f} seconds")
        logger.debug(f" ..with ret_val={{{ret_val}}}")
        return ret_val

    return wrapper
