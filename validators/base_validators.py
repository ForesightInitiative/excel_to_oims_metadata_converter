#<%REGION File header%>
#=============================================================================
# File      : base_validators.py
# Author    : Gideon Kruseman <g.kruseman@cgiar.org>
# Version   : 1.0
# Date      : 12/12/2024 11:20:38 AM
# Changed   : 12/12/2024 11:20:41 AM
# Changed by: Gideon Kruseman <g.kruseman@cgiar.org>
# Remarks   :
"""

"""
# verrsion history
"""

"""
#=============================================================================
#<%/REGION File header%>
import pandas as pd  # Add this import at the top of the file

class BaseValidators:
    @staticmethod
    def validate_mandatory_fields(data, mandatory_fields, context=""):
        """
        Validate that all mandatory fields are present in the data.
        :param data: The data dictionary or list of dictionaries to validate.
        :param mandatory_fields: List of mandatory field names.
        :param context: Contextual information for error messaging (optional).
        :raises ValueError: If a mandatory field is missing.
        """
        missing_fields = [field for field in mandatory_fields if field not in data or pd.isna(data[field])]
        if missing_fields:
            raise ValueError(f"Missing mandatory fields in {context}: {missing_fields}")

#============================   End Of File   ================================