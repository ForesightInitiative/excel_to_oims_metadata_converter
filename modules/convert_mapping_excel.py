#<%REGION File header%>
#=============================================================================
# File      : convert_mapping_excel.py
# Author    : Gideon Kruseman <g.kruseman@cgiar.org>
# Version   : 1.0.0
# Date      : 12/10/2024 3:53:59 PM
# Changed   :
# Changed by:
# documentation   :
"""
"""
# internal Remarks   :
"""
need to develop the code
"""
# version history information   :
"""
- Version 1.0.0: Initial implementation of the conversion utility to convert a
                 mapping file in excel format into an OIMS-compatioble JSON file.
"""
#=============================================================================
#<%/REGION File header%>

#! <%GTREE 1 Initialization%>
#! <%GTREE 1.1 Load standard python Libraries%>
import pandas as pd
import json
import os

from datetime import datetime

from validators.base_validators import BaseValidators
#! <%GTREE 2 Convert Excel mapping to OIMS class%>
class ConvertMappingExcel:
    #! <%GTREE 2.1 main method%>
    def convert_excel_mapping(self, mapping_excel_path, output_json_path=None):
        #! <%GTREE 2.1.1 tool version as a variable%>
        __tool_version__ = "1.0.0"
        """
        Convert an Excel mapping file into the OIMS standard JSON format.

        :param mapping_excel_path: Path to the Excel mapping file.
        :param output_json_path: Path to save the converted JSON file.
        :return: Dictionary representation of the OIMS mapping.
        """
        #! <%GTREE 2.1.2 load Excel sheets%>
        # Load Excel sheets
        excel_data = pd.ExcelFile(mapping_excel_path)
        mappings_df = excel_data.parse('mappings')
        mapping_metadata_df = excel_data.parse('mapping_metadata')

        #! <%GTREE 2.1.3 Determine output path and write to JSON%>
        #
        if not output_json_path:
            output_json_path = os.path.splitext(mapping_excel_path)[0] + ".json"

        #! <%GTREE 2.1.4 build header section%>
        # Build OIMS Header
        oims_header = {
            "mapping_info": {
                "mapper_tool_name": "ConvertMappingExcel",
                "version": __tool_version__,
                "input_parameters": [
                    {
                        "input_parameter_name": "mapping_excel_path",
                        "input_parameter_value": mapping_excel_path
                    },
                    {
                        "output_parameter_name": "output_json_path",
                        "output_parameter_value": output_json_path
                    }
                ]
            },
            "metadata_schema": self.build_metadata_schema(mapping_metadata_df),
            "file_descriptors": self.build_file_descriptors(mapping_metadata_df)
        }

        #! <%GTREE 2.1.5 build content section%>


        oims_content_object_metadata_blocks = []
        for index, row in mappings_df.iterrows():  # Use index to provide context
            mandatory_fields = ["sheetname", "oims_section", "table_orientation"]

            # Validate mandatory fields in the current row
            try:
                BaseValidators.validate_mandatory_fields(
                    row,
                    mandatory_fields,
                    context=f"row {index} in mappings sheet"
                )
            except ValueError as e:
                # Handle missing mandatory fields with a descriptive error
                print(f"Validation error: {e}")
                continue  # Skip the invalid row and proceed with the next


            # Determine subsection and entity_class
            if row["oims_section"] == "OIMS_header":
                subsection_contentobject = {"oims_subsection": row.get("oims_subsection", "default_header_subsection")}
                entity_class = None
            elif pd.notna(row.get("oims_content_object")):
                subsection_contentobject = {"oims_content_object": row["oims_content_object"]}
                entity_class = {"entity_class": row["entity_class"]}
            else:
                subsection_contentobject = {}
                entity_class = None


            oims_content_object_metadata = {
                "sheetname": row["sheetname"],
                "oims_section": row["oims_section"],
                **subsection_contentobject,
                **(entity_class if entity_class else {}),
                "table_orientation": row["table_orientation"],
                "attribute_pairs": self.parse_attribute_pairs(row["sheetname"], excel_data)
            }
            oims_content_object_metadata_blocks.append(oims_content_object_metadata)

        oims_content = {
            "OIMS_content": [
                {
                    "OIMS_content_object": "mapping",
                    "OIMS_content_object_properties": {
                        "validated_oims_metadata_schema":[
                            mapping_metadata_df.loc[
                                mapping_metadata_df["Property"] == "validated_oims_metadata_schema", "value"
                            ].values[0]
                        ],
                        "metadata_class":["mappings"],
                        "metadata":oims_content_object_metadata_blocks
                    }
                }
            ]
        }

        # Combine into final OIMS structure
        oims_data = {
            "OIMS": {
                "OIMS_header": oims_header,
                "OIMS_content": oims_content
            }
        }

        #! <%GTREE 2.1.6 save output to json and return the mapping in oims format%>
        with open(output_json_path, "w") as json_file:
            json.dump(oims_data, json_file, indent=4)
        print(f"Converted OIMS JSON saved to: {output_json_path}")

        return oims_data

    #! <%GTREE 2.2 build metadata schema sub section of the OIMS_header section method%>
    def build_metadata_schema(self, mapping_metadata_df):
        """
        Build the metadata schema section of the OIMS header.

        :param mapping_metadata_df: DataFrame containing metadata schema information.
        :return: Metadata schema structure.
        """
        schema_name = mapping_metadata_df.loc[
            mapping_metadata_df["Property"] == "schema_name", "value"
        ].values[0]
        schema_description = mapping_metadata_df.loc[
            mapping_metadata_df["Property"] == "schema_description", "value"
        ].values[0]
        schema_version = mapping_metadata_df.loc[
            mapping_metadata_df["Property"] == "schema_version", "value"
        ].values[0]
        schema_url = mapping_metadata_df.loc[
            mapping_metadata_df["Property"] == "schema_url", "value"
        ].values[0]
        pid_scheme = mapping_metadata_df.loc[
            mapping_metadata_df["Property"] == "pid_scheme", "value"
        ].values[0]
        pid = mapping_metadata_df.loc[
            mapping_metadata_df["Property"] == "pid", "value"
        ].values[0]

        return [
            {
                "OIMS_content_object": "mapping",
                "schema_properties": [
                    {
                        "schema_name": schema_name,
                        "schema_description": schema_description,
                        "schema_type": "primary metadata metadata",
                        "schema_version": schema_version,
                        "schema_url": schema_url,
                        "schema_pid": {
                            "pid_scheme": pid_scheme,
                            "pid": pid
                        },
                        "OIMS_content_object": "mapping"
                    }
                ]
            }
        ]

    #! <%GTREE 2.3 build file descriptors sub section of the OIMS_header section method%>
    def build_file_descriptors(self, mapping_metadata_df):
        """
        Build the file descriptors section of the OIMS header.

        :param mapping_metadata_df: DataFrame containing file descriptor information.
        :return: File descriptors structure.
        """
        metadata_name = mapping_metadata_df.loc[
            mapping_metadata_df["Property"] == "metadata_name", "value"
        ].values[0]
        metadata_description = mapping_metadata_df.loc[
            mapping_metadata_df["Property"] == "metadata_description", "value"
        ].values[0]
        current_version = mapping_metadata_df.loc[
            mapping_metadata_df["Property"] == "current_version", "value"
        ].values[0]
        metadata_version_status = mapping_metadata_df.loc[
            mapping_metadata_df["Property"] == "metadata_version_status", "value"
        ].values[0]
        contact_name = mapping_metadata_df.loc[
            mapping_metadata_df["Property"] == "contact_name", "value"
        ].values[0]
        contact_role = mapping_metadata_df.loc[
            mapping_metadata_df["Property"] == "contact_role", "value"
        ].values[0]
        contact_email = mapping_metadata_df.loc[
            mapping_metadata_df["Property"] == "contact_email", "value"
        ].values[0]

        return {
            "metadata_name": metadata_name,
            "metadata_description": metadata_description,
            "metadata_version": {
                "current_version": current_version,
                "metadata_version_status": metadata_version_status,
                "version_date": datetime.now().strftime("%Y-%m-%d")
            },
            "metadata_pid": {
                "pid_scheme": "TBD",
                "pid": "to be determined"
            },
            "contact": [
                {
                    "contact_name": contact_name,
                    "contact_role": contact_role,
                    "contact_email": [contact_email]
                }
            ]
        }

    #! <%GTREE 2.4 parse attribute pairs%>
    def parse_attribute_pairs(self, sheetname, excel_data):
        """
        Parse additional sheets for attribute pairs based on the sheet name.
        :param sheetname: Name of the sheet to parse for attribute pairs.
        :param excel_data: ExcelFile object containing all sheets.
        :return: List of attribute pairs.
        """
        try:
            sheet_data = excel_data.parse(sheetname)
            attribute_pairs = []
            for _, row in sheet_data.iterrows():
                cleaned_row = {key: value for key, value in row.items() if pd.notna(value)}
                attribute_pairs.append(cleaned_row)
            return attribute_pairs
        except Exception as e:
            print(f"Warning: Could not parse attribute pairs for sheet '{sheetname}'. Error: {e}")
            return []

#============================   End Of File   ================================