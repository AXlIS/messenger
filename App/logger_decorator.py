import logging
import inspect
import loggers.function_log_config

logger = logging.getLogger('start.work')


def log_start(func):
    def decorator(*args, **kwargs):
        logger.info(f'Start working {func.__name__}')
        stack = inspect.stack()
        logger.info(f'Function {func.__name__} called from {stack[1].function}')
        return func(*args, **kwargs)

    return decorator
