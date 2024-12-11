#<%REGION File header%>
#=============================================================================
# File      : error_handler.py
# Author    : Gideon Kruseman <gkruseman@gmail.com>
# Version   : 1.0.0
# Date      : 2024-12-10
# Changed   : <date of changes relative to last version>
# Changed by: <author of the changes>
# Remarks   :
"""

"""
# version history information   :
"""
- Version 1.0.0: Initial implementation of the centralized error handling utility.
"""
#=============================================================================
#<%/REGION File header%>

#! <%GTREE 1 Initialization%>
from util.logger import setup_logger

logger = setup_logger("ErrorHandler")

class MetadataConversionException(Exception):
    """Base exception for metadata conversion errors."""
    pass

class InvalidMappingException(MetadataConversionException):
    """Raised when a mapping is invalid."""
    pass

class FileNotFoundException(MetadataConversionException):
    """Raised when a required file is not found."""
    pass

def handle_exception(exception):
    """
    Log and handle exceptions in a centralized way.

    :param exception: The exception to handle.
    """
    logger.error(f"An error occurred: {exception}", exc_info=True)
#============================   End Of File   ================================