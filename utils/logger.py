import logging
import os
import sys
from data.config import Config


def setup_logger():
    """Настраивает корневой logger приложения."""
    if Config.config is None:
        raise RuntimeError("Config must be initialized before setting up logger")
    
    log_level = getattr(logging, Config.config.log_level.upper(), logging.DEBUG)
    log_file = Config.config.log_file

    logger = logging.getLogger()
    logger.setLevel(log_level)

    # Форматтер для текстового вывода
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Console handler (stdout)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File handler (если указан LOG_FILE)
    if log_file:
        # Создать директорию если не существует
        log_dir = os.path.dirname(log_file)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir, exist_ok=True)

        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(log_level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger


def get_logger(name):
    """Возвращает logger с указанным именем."""
    return logging.getLogger(name)