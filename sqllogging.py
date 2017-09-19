import logging
import os.path
from config import LOG_NAME, LOG_PATH, LOG_FORMAT


def initlog(name=LOG_NAME, path=LOG_PATH):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    fh = logging.FileHandler(path)
    fmt = logging.Formatter(LOG_FORMAT)
    fh.setFormatter(fmt)
    fh.setLevel(logging.DEBUG)

    logger.addHandler(fh)


if __name__ == "__main__":
    initlog()
    log = logging.getLogger(LOG_NAME)
    log.info("aaaa")
    log2 = logging.info("b")
    try:
        1 / 0
    except Exception as e:
        logging.exception(repr(e))
        log.exception('another:' + repr(e))
