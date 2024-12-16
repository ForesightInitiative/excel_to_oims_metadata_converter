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
- Version 1.0.0: Initial implementation of the json reading functionality.
"""
#=============================================================================
#<%/REGION File header%>
#! <%GTREE 1 Initialization%>
import json

class JsonReader:
    #! <%GTREE 2.1 Initialization%>
    def __init__(self, file_path):
        self.file_path = file_path

    #! <%GTREE 2.2 Read Excel File%>
    def read_json(self):
        try:
            with open(self.file_path, "r") as file:
                return json.load(file)
        except Exception as e:
            raise FileNotFoundError(f"Error loading json file: {e}")


#============================   End Of File   ================================