#<%REGION File header%>
#=============================================================================
# File      : excel_to_oims_mapping_validator.py
# Author    : Gideon Kruseman <g.kruseman@cgiar.org>
# Version   : 1.0
# Date      : 12/12/2024 1:24:18 PM
# Changed   : 12/12/2024 1:24:23 PM
# Changed by: Gideon Kruseman <g.kruseman@cgiar.org>
# Remarks   :
"""
The oims-compatible mapping file has been loaded into the tool this validator has
a method to check if the mapping file corresponds to the primary metadata file in
MS Excel format.

It also has a method to check the ampping file against the udnerlying etadata schema
that will be used to generate the OIMS-compatoible primary metadata file

"""
# version history information   :
"""
- Version 1.0.0: Initial implementation of the validators to validate the
          MS Excel primary metadata against the mapping file and
          the mapping file against the underlying metadat schema.
"""
#=============================================================================
#<%/REGION File header%>

"""
The mapping file contains
{
    "OIMS":{
        "OIMS_header":{},
        "OIMS_content": {
            "OIMS_content": [
                {
                    "OIMS_content_object": "mapping",
                    "OIMS_content_object_properties": {
                        "validated_oims_metadata_schema": [
                            "<identifier of the underlying schema>"
                        ],
                        "metadata_class": [
                            "mappings"
                        ],
                        "metadata":[{}]
                    }
                }
            ]
        }
    }
}

The ("metadata": [{}]) section has the information on the sheets that
can be expected there are two main cases. the first is information for the header
section of the output file.

Example 1:
                            {
                                "sheetname": "MetadataFileDescriptors",
                                "oims_section": "OIMS_header",
                                "oims_subsection": "file_descriptors",
                                "table_orientation": "attributes_in_rows",
                                "attribute_pairs": [
                                    {
                                        "information_type": "metadata_field_value",
                                        "excel_field_name": "Metadata Name",
                                        "excel_field_name_loc": "A2",
                                        "excel_value_loc_range_start": "E2",
                                        "oims_attribute_id": "metadata_name",
                                        "user_comments": "D2"
                                    }


the second case is  for the OIUMS_content section

Example 2:
                            {
                                "sheetname": "DescriptiveMetadataDataset",
                                "oims_section": "OIMS_content",
                                "oims_content_object": "DescriptiveMetadataDataset",
                                "entity_class": "dataset",
                                "table_orientation": "attributes_in_rows",
                                "attribute_pairs": [
                                    {
                                        "information_type": "metadata_field_value",
                                        "excel_field_name": "Title",
                                        "excel_field_name_loc": "B2",
                                        "excel_value_loc_range_start": "J2",
                                        "oims_attribute_id": "dataset_title",
                                        "user_comments": "I2"
                                    },


"""

class ExcelToOimsMappingValidator:
    def validate_excel_against_mapping(self,excel_data, mapping, allowed_missing_sheets=none, sheets_to_skip=none):
        """
        The ("metadata": [{}]) section has the information on the sheets that
        can be expected.
        1. check if the sheetname attribute in the mapping file and the sheets
        in the primary metadata MS Excel template correspond. certain sheets may
        be allowed to be missing and certain sheets should be skipped if the exist
        2. in each sheet do some checks:
            a. check table orientation
            b. if exist property excel_field_name and excel_field_name_loc check in sheet if value of
               excel_field_name is present in the location indicated by the value of excel_field_name_loc
            c. if oims_section == "OIMS_header":
                i.   check if oims_subsection value is one of "file_descriptors" or "mapping_tools"
                ii.  check all oims_attribute_id values against a list of expected properties
            d. if oims_section == "OIMS_content":
                i.   check if oims_content_object exists and has a value
                ii.  check if entity class is element of set {collection, dataset, data file,
                     data_file, support documentation, support_documentation, data container, data_container,
                     container, variable, data variable }

        """
        """
        Validate the Excel primary metadata against the mapping file.
        """
        allowed_missing_sheets = allowed_missing_sheets or []
        sheets_to_skip = sheets_to_skip or []

        metadata = mapping["OIMS"]["OIMS_content"]["OIMS_content"][0]["OIMS_content_object_properties"]["metadata"]

        # Step 1: Check if sheets in the Excel file match the mapping
        excel_sheets = excel_data.sheet_names
        for metadata_item in metadata:
            sheetname = metadata_item["sheetname"]

            # Skip specified sheets
            if sheetname in sheets_to_skip:
                continue

            # Check for missing sheets
            if sheetname not in excel_sheets and sheetname not in allowed_missing_sheets:
                raise ValueError(f"Missing sheet '{sheetname}' in Excel file.")

            if sheetname in excel_sheets:
                # Step 2: Perform checks on each sheet
                sheet_data = excel_data.parse(sheetname)

                # a. Check table orientation
                table_orientation = metadata_item["table_orientation"]
                if table_orientation not in ["attributes_in_rows", "attributes_in_columns"]:
                    raise ValueError(f"Invalid table orientation '{table_orientation}' for sheet '{sheetname}'.")

                # b. Check field locations
                for attribute_pair in metadata_item["attribute_pairs"]:
                    if "excel_field_name" in attribute_pair and "excel_field_name_loc" in attribute_pair:
                        field_name = attribute_pair["excel_field_name"]
                        field_loc = attribute_pair["excel_field_name_loc"]

                        # Validate if the field name is in the indicated location
                        field_row, field_col = self.parse_excel_location(field_loc)
                        if sheet_data.iloc[field_row, field_col] != field_name:
                            raise ValueError(f"Field '{field_name}' not found at location '{field_loc}' in sheet '{sheetname}'.")

                # c. Checks for OIMS_header and OIMS_content sections
                if metadata_item["oims_section"] == "OIMS_header":
                    oims_subsection = metadata_item.get("oims_subsection", "")
                    if oims_subsection not in ["file_descriptors", "mapping_tools"]:
                        raise ValueError(f"Invalid oims_subsection '{oims_subsection}' in sheet '{sheetname}'.")

                if metadata_item["oims_section"] == "OIMS_content":
                    oims_content_object = metadata_item.get("oims_content_object", None)
                    if not oims_content_object:
                        raise ValueError(f"Missing oims_content_object in sheet '{sheetname}'.")

                    entity_class = metadata_item.get("entity_class", None)
                    valid_classes = {"collection", "dataset", "data_file", "support_documentation",
                                     "data_container", "container", "variable", "data_variable"}
                    if entity_class not in valid_classes:
                        raise ValueError(f"Invalid entity class '{entity_class}' in sheet '{sheetname}'.")

    @staticmethod
    def parse_excel_location(location):
        """
        Parse an Excel-style cell location (e.g., "A2") into a (row, col) tuple.
        """
        col = ord(location[0].upper()) - ord('A')
        row = int(location[1:]) - 1
        return row, col

    def validate_mapping_against_schema(self,mapping, schema)
        """
        1. In the header section of the underlyuing schema the metadata_name should be in the list of "validated_oims_metadata_schema"
        2. if attribute pairs property "information_type" exists and value is not "metadata_field_value" then skip this apir in the validation
        3. check if oims_attribute_id is one of the values in "attribute_name" in the list of compound objects in the "metadata":[{]} of the underlying schema
        """
        # Step 1: Check if metadata_name is in validated_oims_metadata_schema
        # Extract the validated schema name from the mapping
        validated_schema_name = mapping["OIMS"]["OIMS_content"]["OIMS_content"][0]["OIMS_content_object_properties"]["validated_oims_metadata_schema"][0]

        # Verify the schema name matches the header in the schema
        schema_metadata_name = schema["OIMS"]["OIMS_header"]["file_descriptors"]["metadata_name"]
        if validated_schema_name != schema_metadata_name:
            raise ValueError(f"Schema mismatch: Mapping references '{validated_schema_name}', but schema defines '{schema_metadata_name}'.")

        # Get the list of attribute names from the schema
        schema_attributes = {
            attribute["attribute_name"]
            for content in schema["OIMS"]["OIMS_content"]
            for attribute in content["OIMS_content_object_properties"]["metadata"]
        }

        # Step 2: Check attribute pairs
        # Validate each attribute pair in the mapping
        for metadata_item in mapping["OIMS"]["OIMS_content"]["OIMS_content"][0]["OIMS_content_object_properties"]["metadata"]:
            for attribute_pair in metadata_item["attribute_pairs"]:
                # Skip pairs where `information_type` is not "metadata_field_value"
                if attribute_pair.get("information_type", "metadata_field_value") != "metadata_field_value":
                    continue

                # Check if the `oims_attribute_id` exists in the schema attributes
                oims_attribute_id = attribute_pair.get("oims_attribute_id", None)
                if oims_attribute_id and oims_attribute_id not in schema_attributes:
                    raise ValueError(f"Invalid oims_attribute_id '{oims_attribute_id}' in sheet '{metadata_item['sheetname']}'. "
                                     f"Expected one of {sorted(schema_attributes)}.")



#============================   End Of File   ================================