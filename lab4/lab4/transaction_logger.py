import logging

def set_logger(name="Root"):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    console_handler = logging.StreamHandler()
    # console_handler.setFormatter(logging.Formatter('%(levelname)s:%(name)s:%(message)s'))
    console_handler.setFormatter(logging.Formatter('%(name)s:%(message)s'))
    if not logger.hasHandlers():
        logger.addHandler(console_handler)

    return logger
