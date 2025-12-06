import sys
import functools
import io
import logging


def logger(func=None, *, handle: io.TextIOWrapper | io.StringIO | logging.Logger = sys.stdout):
    if func is None:
        return lambda func: logger(func, handle=handle)

    @functools.wraps(func)
    def inner(*args, **kwargs):
        # Инициализация функций логирования
        if isinstance(handle, logging.Logger):
            # Логирование в логгер
            def info(to_log):
                handle.info(to_log)
            def warning(to_log):
                handle.warning(to_log)
            def error(to_log):
                handle.error(to_log)
            def critical(to_log):
                handle.critical(to_log)

        else:
            # Логирование в поток
            def info(to_log):
                handle.write(to_log)
                handle.flush()
            def warning(to_log):
                handle.write(to_log)
                handle.flush()
            def error(to_log):
                handle.write(to_log)
                handle.flush()
            def critical(to_log):
                handle.write(to_log)
                handle.flush()

        args_to_log = [param for param in args]
        kwargs_to_log = [(key, value) for key, value in kwargs.items()]
        all_params = (args_to_log, kwargs_to_log)
        info(f"INFO: function: {func.__name__}, params: {all_params}\n")

        try:
            # Лог выполненной функции
            output = func(*args, **kwargs)
            if output is not None:
                info(f"INFO: FINISHED {func.__name__}, RESULT: {output}\n")
            else:
                warning(f"WARNING: FINISHED {func.__name__}, RESULT IS NONE\n")

            return output

        except Exception as e:
            # Лог ошибки
            if isinstance(e, TypeError):
                critical(f"CRITICAL: UNFINISHED {func.__name__}, CRITICAL   : {type(e).__name__}: {e}\n")
            else:
                error(f"ERROR: UNFINISHED {func.__name__}, ERROR: {type(e).__name__}: {e}\n")

            raise e

    return inner
