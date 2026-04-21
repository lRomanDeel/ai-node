# kernel/core/logger.py

import logging
import sys


def setup_logger():
    """
    Настройка глобального логгера системы
    """

    logger = logging.getLogger("kernel")

    # чтобы не дублировались логи
    if logger.hasHandlers():
        return logger

    logger.setLevel(logging.INFO)

    handler = logging.StreamHandler(sys.stdout)

    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    handler.setFormatter(formatter)

    logger.addHandler(handler)

    return logger


# создаем singleton логгер
logger = setup_logger()
