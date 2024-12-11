#<%REGION File header%>
#=============================================================================
# File      : metadata_converter.py
# Author    : Gideon Kruseman <g.kruseman@cgiar.org>
# Version   : 1.0.0
# Date      : 2024-12-06 to 2024-12-10
# Changed   :
# Changed by:
# Internal remarks   :
"""
version 1.0.0.1  2024-12-10 Updated to align with the new project structure and resolve identified issues.
"""
# version history information   :
"""
- Version 1.0.0: Initial implementation of the metadata conversion tool.
"""
#=============================================================================
#<%/REGION File header%>

#! <%GTREE 1 Initialization%>
#! <%GTREE 1.1 Load standard python Libraries%>
import os
import json
#! <%GTREE 1.2 Load OIMS converter tool libraries%>
#! <%GTREE 1.2.1 Load main modules%>
from modules.mapper import Mapper
from modules.convert_mapping_excel import ConvertMappingExcel

#! <%GTREE 1.2.2 Load utilities%>
from utils.settings_reader import SettingsReader
from utils.excel_reader import ExcelReader
from utils.json_reader import JsonReader
from utils.reporter import Reporter
from utils.logger import SetupLogger

#! <%GTREE 1.2.3 Load specific mappers%>
#specific mappers are loaded dynamically

#! <%GTREE 1.2.4 Load validators%>
from validators.input_validator import InputValidator
from validators.excel_to_oims_mapping_validator import ExcelToOimsMappingValidator
from validators.output_validator import OutputValidator


#! <%GTREE 1.2.5 Load data%>
from oims_structures.converter_data import (
    KNOWN_MAPPING_CLASSIFICATIONS,
    KNOWN_MAPPINGS,
    KNOWN_SCHEMAS,
)

#! <%GTREE 2 Main Converter Class%>
class MetadataConverter:
    #! <%GTREE 2.1 Initialization%>
    def __init__(self, settings_path=None, settings=None):
        if settings:
            self.settings = settings
        elif settings_path:
            self.settings = SettingsReader(settings_path).read_settings()
        self.logger = setup_logger()


    #! <%GTREE 2.2 Load Inputs%>
    #! <%GTREE 2.2 Load Inputs%>
    def load_inputs(self):
        self.logger.info("Loading input files...")
        self.excel_data = ExcelReader(self.settings["path_to_primary_metadata"]).read_excel()
        if self.settings["path_to_mapping_file"].endswith(".json"):
            self.mapping = JsonReader(self.settings["path_to_mapping_file"]).read_json()
            boolean_convert_excel_mapping = False
        else:
            self.mapping_excel = ExcelReader(self.settings["path_to_mapping_file"]).read_excel()
            boolean_convert_excel_mapping = True
        self.schema = JsonReader(self.settings["path_to_oims_metadata_schema_file"]).read_json()
        if boolean_convert_excel_mapping:
            self.mapping = convert_excel_mapping(self.mapping_excel)

    #! <%GTREE 2.3 Validate Inputs%>
    def validate_inputs(self):
        self.logger.info("Validating inputs...")
        InputValidator.validate_settings(self.settings)
        ExcelToOimsMappingValidator.validate_excel_against_mapping(self.excel_data, self.mapping)
        ExcelToOimsMappingValidator.validate_mapping_against_schema(self.mapping, self.schema)

    #! <%GTREE 2.4 Convert Data%>
    def convert_data(self):
        self.logger.info("Converting data...")
        return Mapper().map_to_json(
            self.excel_data,
            self.mapping,
            self.schema,
            self.mapping_classification_id,
            self.mapping_id,
            self.schema_id,
        )

    #! <%GTREE 2.5 Generate Outputs%>
    def generate_outputs(self, output_data):
        output_path = self.settings["output_json_path"]
        with open(output_path, "w") as json_file:
            json.dump(output_data, json_file, indent=4)
        self.logger.info(f"Output saved to {output_path}")

    #! <%GTREE 2.6 validate aettings%>
    def validate_settings(self):
        """
        Validate the settings file and the input/output paths.
        - Check file paths and folder existence.
        - Determine mapping file type (xlsx or json).
        - Validate IDs in settings.
        """
        try:
            # Load settings
            self.settings = SettingsReader(self.settings_file_path).read_settings()

            # Check file paths
            required_paths = [
                "path_to_primary_metadata",
                "path_to_oims_metadata_schema_file",
                "path_to_mapping_file"
            ]
            for path in required_paths:
                if not os.path.exists(self.settings[path]):
                    raise FileNotFoundError(f"Required file path '{path}' does not exist.")

            # Check output folder
            output_dir = os.path.dirname(self.settings["path_to_output_oims_metadata_file"])
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)

            # Determine mapping file type
            mapping_path = self.settings["path_to_mapping_file"]
            if mapping_path.endswith(".xlsx"):
                self.mapping_file_type = "xlsx"
            elif mapping_path.endswith(".json"):
                self.mapping_file_type = "json"
            else:
                raise ValueError(f"Unsupported mapping file type: {mapping_path}")


            self.mapping_classification_id = self.settings["mapping_classification_id"]
            self.mapping_id = self.settings["mapping_id"]
            self.schema_id = self.settings["oims_metadata_schema_id"]

            if mapping_classification_id not in KNOWN_MAPPING_CLASSIFICATIONS:
                print(f"Unknown mapping classification ID: {mapping_classification_id}. Using generic conversion.")
            if mapping_id not in KNOWN_MAPPINGS:
                print(f"Unknown mapping ID: {mapping_id}. Using generic conversion.")
            if schema_id not in KNOWN_SCHEMAS:
                print(f"Unknown OIMS metadata schema ID: {schema_id}. Validation will not be performed.")

            # Set internal flags for generic conversion or validation
            self.generic_conversion = (
                mapping_classification_id not in known_mapping_classifications
                or mapping_id not in known_mappings
                or schema_id not in known_schemas
            )
        except Exception as e:
            raise ValueError(f"Settings validation failed: {e}")

    #! <%GTREE 2.7 Run Conversion Process%>
    def run(self):
        self.validate_settings()
        self.load_inputs()
        self.validate_inputs()
        output_data = self.convert_data()
        self.generate_outputs(output_data)
        Reporter.generate_report(self.settings["report_path"])

#! <%GTREE 3 Main Function%>
if __name__ == "__main__":
    settings_file = "runcontrol/settings.json"
    converter = MetadataConverter(settings__path=settings_file)
    converter.run()

#============================   End Of File   ================================