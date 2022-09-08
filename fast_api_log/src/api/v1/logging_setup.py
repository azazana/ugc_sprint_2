"""Конфиг логгера."""
import logging

LOG_FORMAT = '{"log_api":"%(asctime)s - %(levelname)s - %(name)s - %(message)s"} {"request_id": "%(request_id)s"}'

old_factory = logging.getLogRecordFactory()


def record_factory(*args, request_id="", **kwargs):
    """Добавление в логгер requist_id."""
    record = old_factory(*args, **kwargs)
    record.request_id = request_id
    return record


def setup_root_logger(log_filename):
    """ Setup configuration of the root logger of the application."""

    # get instance of root logger
    logger = logging.getLogger("")

    # configure formatter for logger
    formatter = logging.Formatter(LOG_FORMAT)

    file = logging.handlers.RotatingFileHandler(filename=log_filename, mode='a',
                                                maxBytes=15000000, backupCount=5)
    file.setFormatter(formatter)
    # add handlers
    logger.addHandler(file)
    # configure logger level
    logging.setLogRecordFactory(record_factory)

    logger.setLevel(logging.INFO)
