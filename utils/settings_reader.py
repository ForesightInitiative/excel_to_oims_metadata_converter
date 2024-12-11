#<%REGION File header%>
#=============================================================================
# File      : settings_reader.py
# Author    : Your Name <your.email@example.com>
# Version   : 1.0.0
# Date      : 2024-12-06
# Changed   : <date of changes relative to last version>
# Changed by: <author of the changes>
# Remarks   :
"""
The standard settings file looks like this:

{
  "path_to_primary_metadata":"<path/to/primary/metadata.xlsx>",
  "mapping_classification_id":"<identifier for the structure of the mapping file>",
  "mapping_id":"<specific mapping identifier>",
  "oims_metadata_schema_id":"<identifier for the underlying oims_cmpatible prumary metadata schema>",
  "path_to_oims_metadata_schema_file":"<path/to/oims/metadata/schema.json>"
  "path_to_mapping_file":"<path/to/mapping/file.json> or <path/to/mapping/file.xlsx>",
  "path_to_output_oims_metadata_file":"<path/to/oims/compatible/primary/metadata/file.json>"
}

"""
# version history information   :
"""
- Version 1.0.0: Initial implementation of the settings reader.
"""
#=============================================================================
#<%/REGION File header%>

#! <%GTREE 1 Initialization%>
import json

#! <%GTREE 2 SettingsReader Class%>
class SettingsReader:
    #! <%GTREE 2.1 Initialization%>
    def __init__(self, settings_file_path):
        self.settings_file_path = settings_file_path

    #! <%GTREE 2.2 Read Settings File%>
    def read_settings(self):
        try:
            with open(self.settings_file_path, "r") as file:
                return json.load(file)
        except Exception as e:
            raise FileNotFoundError(f"Error reading settings file: {e}")

    #! <%GTREE 2.2 Read Settings File%>
    def validate_settings(self, settings):
        """
        Validate the settings dictionary.
        - Ensure all required keys are present.
        - Validate file paths and supported formats.
        """
        required_keys = [
            "path_to_primary_metadata",
            "mapping_classification_id",
            "mapping_id",
            "oims_metadata_schema_id",
            "path_to_oims_metadata_schema_file",
            "path_to_mapping_file",
            "path_to_output_oims_metadata_file"
        ]

        # Check for missing keys
        missing_keys = [key for key in required_keys if key not in settings]
        if missing_keys:
            raise KeyError(f"Missing required settings keys: {', '.join(missing_keys)}")

        # Validate file paths
        for key in ["path_to_primary_metadata", "path_to_oims_metadata_schema_file", "path_to_mapping_file"]:
            if not os.path.exists(settings[key]):
                raise FileNotFoundError(f"File does not exist: {settings[key]}")

        # Check mapping file format
        mapping_file = settings["path_to_mapping_file"]
        if not (mapping_file.endswith(".xlsx") or mapping_file.endswith(".json")):
            raise ValueError(f"Invalid mapping file format: {mapping_file}")

        # Check if output directory exists or create it
        output_dir = os.path.dirname(settings["path_to_output_oims_metadata_file"])
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

#============================   End Of File   ================================