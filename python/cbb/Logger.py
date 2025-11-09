import logging
from logging import Logger


def get_file_logger(file_name: str) -> Logger:
    # 新建一个logger对象
    logger: Logger = logging.getLogger(file_name)
    logger.setLevel(logging.INFO)

    # 新建一个文件处理器，并设置为追加写入模式
    file_handler = logging.FileHandler(f"logs/{file_name}.txt", mode="a", encoding="utf-8")
    file_handler.setLevel(logging.INFO)

    # 新建一个格式化输出器
    formatter = logging.Formatter("%(asctime)s [%(levelname)s] [%(filename)s:%(lineno)d] %(message)s")
    file_handler.setFormatter(formatter)

    # 将文件处理器添加到logger中
    logger.addHandler(file_handler)

    return logger
