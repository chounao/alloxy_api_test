import logging
import os
import time
from pathlib import Path


BASE_PATH = Path(__file__).resolve().parents[1]
LOG_PATH = Path(os.getenv("ALLOXY_LOG_DIR", BASE_PATH / "Log"))


class Logger:
    """项目日志工具：统一控制台和文件日志，并避免重复添加 handler。"""

    def __init__(self) -> None:
        LOG_PATH.mkdir(parents=True, exist_ok=True)
        self.logname = LOG_PATH / f"{time.strftime('%Y_%m_%d')}.log"
        self.logger = logging.getLogger("log")
        self.logger.setLevel(logging.DEBUG)
        self.logger.propagate = False

        # 中文备注：pytest 多次导入模块时不能重复添加 handler，否则日志会重复打印。
        if self.logger.handlers:
            return

        formatter = logging.Formatter(
            "[%(asctime)s][%(filename)s %(lineno)d][%(levelname)s]: %(message)s"
        )

        file_handler = logging.FileHandler(self.logname, mode="a", encoding="utf-8")
        console_handler = logging.StreamHandler()
        file_handler.setLevel(logging.DEBUG)
        console_handler.setLevel(logging.INFO)
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)


logger = Logger().logger
