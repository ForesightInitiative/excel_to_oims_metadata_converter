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

#! <%GTREE 2 Logger Setup%>
def setup_logger(name="MetadataConverter", log_file=None, level=logging.INFO):
    """
    Setup a logger with both console and optional file handlers.

    :param name: Name of the logger (default: "MetadataConverter").
    :param log_file: Path to a file where logs will be saved (default: None for no file logging).
    :param level: Logging level (default: logging.INFO).
    :return: Configured logger instance.
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Prevent duplicate handlers if logger is already configured
    if not logger.handlers:
        # Console handler
        console_handler = logging.StreamHandler()
        console_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)

        # File handler (optional)
        if log_file:
            os.makedirs(os.path.dirname(log_file), exist_ok=True)  # Ensure log directory exists
            file_handler = logging.FileHandler(log_file)
            file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            file_handler.setFormatter(file_formatter)
            logger.addHandler(file_handler)

    return logger
#============================   End Of File   ================================