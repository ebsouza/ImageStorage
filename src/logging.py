import logging.config

def get_logging(module_name: str):
    logger = logging.getLogger(module_name)
    logging.config.fileConfig('logging.ini', disable_existing_loggers=False)

    return logger