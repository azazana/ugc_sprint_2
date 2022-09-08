import logging

LOG_FORMAT = '{"log_api":"%(asctime)s - %(levelname)s - %(name)s - %(message)s"} {"request_id": "%(request_id)s"}'

# class RequestIdFilterInit(logging.Filter):
#
#     def filter(self, record):
#         record.request_id = 'my-attr'
#         # print(record.request_id)
#         return True

old_factory = logging.getLogRecordFactory()


def record_factory(*args, request_id="", **kwargs):
    record = old_factory(*args, **kwargs)
    record.request_id = request_id
    return record


def setup_root_logger(log_filename):
    """ Setup configuration of the root logger of the application """

    # get instance of root logger
    logger = logging.getLogger('')

    # configure formatter for logger
    formatter = logging.Formatter(LOG_FORMAT)

    file = logging.handlers.RotatingFileHandler(filename=log_filename, mode='a',
                                                maxBytes=15000000, backupCount=5)
    file.setFormatter(formatter)
    # logstash_handler = logstash.LogstashHandler('logstash', 5044, version=1)
    # add handlers
    logger.addHandler(file)
    # logger.addHandler(logstash_handler)
    # logger.addFilter(RequestIdFilterInit())
    # configure logger level
    logging.setLogRecordFactory(record_factory)

    logger.setLevel(logging.INFO)
    # logger.info('test')
#
# def setup_log_root():
#     logger = logging.getLogger('')
#
#     # configure formatter for logger
#     formatter = logging.Formatter(LOG_FORMAT)
#
#     # configure console handler
#     console = logging.StreamHandler()
#     console.setFormatter(formatter)
#
#     file = logging.handlers.RotatingFileHandler(filename="logs/fastapi-elk-stack.log", mode='a',
#                                                 maxBytes=15000000, backupCount=5)
#     file.setFormatter(formatter)
#
#     # add handlers
#     logger.setLevel(logging.INFO)
#
#     logstash_handler = logstash.LogstashHandler('logstash', 5044, version=1)
#
#     # class RequestIdFilter(logging.Filter):
#     #     def filter(self, record):
#     #         record.request_id = request.headers.get('X-Request-Id')
#     #         return True
#
#     # app.logger.addFilter(RequestIdFilter())
#     logger.addHandler(console)
#     logger.addHandler(file)
#     logger.addHandler(logstash_handler)
#
#     # Handler отвечают за вывод и отправку сообщений. В модуль logging доступно несколько классов-обработчиков
#     # Например, SteamHandler для записи в поток stdin/stdout, DatagramHandler для UDP, FileHandler для syslog
#     # LogstashHandler не только отправляет данные по TCP/UDP, но и форматирует логи в json-формат.
#     # return logger
#
