#<%REGION File header%>
#=============================================================================
# File      : logger.py
# Author    : Gideon Kruseman <gkruseman@gmail.com>
# Version   : 1.0.0
# Date      : 2024-12-06
# Changed   : <date of changes relative to last version>
# Changed by: <author of the changes>
# Remarks   :
"""
Enhanced logger utility with file logging, dynamic configuration, and multi-level support.
"""
# version history information   :
"""
- Version 1.0.0: Initial implementation of the logger utility.
- version 1.0.0.1  2024-12-10 Added file logging, configurable logger names, and enhanced format.

"""
#=============================================================================
#<%/REGION File header%>

#! <%GTREE 1 Initialization%>
import logging
import os

#! <%GTREE 2 Logger Setup%>
class SetupLogger:
    def __init__(self, name="MetadataConverter", log_file="convert_metadata_log.txt", level=logging.INFO):
        """
        Initialize a logger with both console and optional file handlers.

        :param name: Name of the logger (default: "MetadataConverter").
        :param log_file: Path to a file where logs will be saved (default: "convert_metadata_log.txt").
        :param level: Logging level (default: logging.INFO).
        """
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

        # Prevent duplicate handlers if logger is already configured
        if not self.logger.handlers:
            # Console handler
            console_handler = logging.StreamHandler()
            console_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            console_handler.setFormatter(console_formatter)
            self.logger.addHandler(console_handler)

            # File handler
            if log_file:
                log_dir = os.path.dirname(log_file)
                if log_dir:  # Ensure the directory part is not empty
                    os.makedirs(log_dir, exist_ok=True)
                file_handler = logging.FileHandler(log_file)
                file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
                file_handler.setFormatter(file_formatter)
                self.logger.addHandler(file_handler)

    def info(self, message):
        self.logger.info(message)

    def error(self, message):
        self.logger.error(message)

    def debug(self, message):
        self.logger.debug(message)

    def warning(self, message):
        self.logger.warning(message)

    def critical(self, message):
        self.logger.critical()



#============================   End Of File   ================================