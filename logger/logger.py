import logging
import os

class Log:
    """ Provides a logging interface for the automation """
    logger = None
    file = None

    @classmethod
    def initialize(cls):
        """ Initializes the logger with predefined configuration, reseting the log file """
        Log.file = 'output/transaction.log'
        if os.path.exists(Log.file):
            os.remove(Log.file)
        logging.basicConfig(
            filename = Log.file,
            encoding = "UTF-8",
            format   = "[{%(filename)s:%(lineno)d} %(levelname)s - %(message)s",
            level    = logging.INFO
        )
        Log.logger = logging.getLogger("fresh-news-RPA")

    @classmethod
    def critical(cls, s: str) -> None:
        print(s)
        Log.logger.critical(s)

    @classmethod
    def error(cls, s: str) -> None:
        print(s)
        Log.logger.error(s)

    @classmethod
    def warning(cls, s: str) -> None:
        print(s)
        Log.logger.warning(s)

    @classmethod
    def info(cls, s: str) -> None:
        print(s)
        Log.logger.info(s)

    @classmethod
    def debug(cls, s: str) -> None:
        print(s)
        Log.logger.debug(s)