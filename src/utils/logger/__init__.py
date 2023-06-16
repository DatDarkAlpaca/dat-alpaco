import logging
import logging.config

import coloredlogs
import yaml
import os


class Logger:
    initialized = False

    def __init__(self, logger_name: str, level: str = 'INFO'):
        self.logger = logging.getLogger(logger_name)

        if not Logger.initialized:
            Logger._initialize(os.getenv('LOGGER_CONFIG_FILEPATH'))

        coloredlogs.install(level=level, logger=self.logger)
        coloredlogs.install(level=None)

    @staticmethod
    def _initialize(config_path: str):
        with open(config_path, mode='r', encoding='utf-8') as file:
            config = yaml.safe_load(file.read())
            logging.config.dictConfig(config)

    def info(self, message: str):
        self.logger.info(message)

    def debug(self, message: str):
        self.logger.debug(message)

    def warning(self, message: str):
        self.logger.warning(message)

    def error(self, message: str):
        self.logger.error(message)

    def critical(self, message: str):
        self.logger.critical(message)


def create_default_logger_file():
    file_text = """version: 1
disable_existing_loggers: false

formatters:
    default:
    format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    datefmt: "[%Y-%m-%d %H:%M:%S]"

handlers:
  console:
    class: logging.StreamHandler
    level: DEBUG
    formatter: default
    stream: ext://sys.stdout

file:
  class: logging.handlers.TimedRotatingFileHandler
  level: DEBUG
  formatter: default
  when: D
  backupCount: 0
  filename: ./res/client.log

loggers:
  root:
    level: INFO
    handlers: [console, file]"""

    file = open('../res/config.yaml', 'w')
    file.write(file_text)
    file.close()
