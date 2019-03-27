import logging
import time
import re
from logging.handlers import TimedRotatingFileHandler
from logging.handlers import RotatingFileHandler

class Logger():
    def __init__(self,str):
        # 日志打印格式
        self.log_fmt = '%(asctime)s\tFile \"%(filename)s\",line %(lineno)s\t%(levelname)s: %(message)s'
        self.formatter = logging.Formatter(self.log_fmt)
        # 创建TimedRotatingFileHandler对象
        self.log_file_handler = TimedRotatingFileHandler(filename="./logs/log", when="M", interval=1, backupCount=2)
        self.log_file_handler.suffix = "%Y-%m-%d_%H-%M.log"
        # log_file_handler.extMatch = re.compile(r"^\d{4}-\d{2}-\d{2}_\d{2}-\d{2}.log$")
        self.log_file_handler.setFormatter(self.formatter)
        logging.basicConfig(level=logging.INFO)
        self.log = logging.getLogger()
        self.log.addHandler(self.log_file_handler)
        self.str=str
    def MyLogDebug(self):
        self.log.debug(self.str,exc_info=True)
        self.log.removeHandler(self.log_file_handler)

    def MyLogInfo(self):
        print("ok")
        self.log.info(self.str,exc_info=True)
        self.log.removeHandler(self.log_file_handler)

    def MyLogWarning(self):
        self.log.warning(self.str,exc_info=True)
        self.log.removeHandler(self.log_file_handler)

    def MyLogError(self):
        self.log.error(self.str, exc_info=True)
        self.log.removeHandler(self.log_file_handler)

    def MyLogCritical(self):
        self.log.critical(self.str, exc_info=True)
        self.log.removeHandler(self.log_file_handler)


if __name__ == "__main__":
    Logger("HELLO").MyLogInfo()