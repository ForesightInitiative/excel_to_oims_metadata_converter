#<%REGION File header%>
#=============================================================================
# File      : excel_reader.py
# Author    : Gideon Kruseman <g.kruseman@cgiar.org>
# Version   : 1.0.0
# Date      : 2024-12-06
# Changed   : <date of changes relative to last version>
# Changed by: <author of the changes>
# Remarks   :
"""
"""
# version history information   :
"""
- Version 1.0.0: Initial implementation of the Excel reading functionality.
"""
#=============================================================================
#<%/REGION File header%>

#! <%GTREE 1 Initialization%>
import pandas as pd

#! <%GTREE 2 ExcelReader Class%>
class ExcelReader:
    #! <%GTREE 2.1 Initialization%>
    def __init__(self, file_path):
        self.file_path = file_path

    #! <%GTREE 2.2 Read Excel File%>
    def read_excel(self):
        try:
            return pd.ExcelFile(self.file_path)
        except Exception as e:
            raise FileNotFoundError(f"Error loading Excel file: {e}")

#============================   End Of File   ================================