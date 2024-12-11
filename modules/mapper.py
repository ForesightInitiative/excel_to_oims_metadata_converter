#<%REGION File header%>
#=============================================================================
# File      : mapper.py
# Author    : Gideon Kruseman <g.kruseman@cgiar.org>
# Version   : 1.0
# Date      : 12/6/2024 3:53:59 PM
# Changed   : 12/6/2024 3:56:11 PM
# Changed by: Gideon Kruseman <g.kruseman@cgiar.org>
# Remarks   :
"""
"""
# version history information   :
"""
- Version 1.0.0: Initial implementation of the mapping utility.
"""
#=============================================================================
#<%/REGION File header%>

#! <%GTREE 1 Initialization%>
#! <%GTREE 1.1 Load standard python libraries%>
import json

#! <%GTREE 1.2 Load OIMS converter tool libraries%>
#! <%GTREE 1.2.1 Load data%>
from oims_structures.converter_data import (
    KNOWN_MAPPING_CLASSIFICATIONS,
    KNOWN_MAPPINGS,
    KNOWN_SCHEMAS,
    KNOWN_COMBINATIONS
    FALLBACK_MAPPER
)

#! <%GTREE 2 Mapper Class%>
class Mapper:
    #! <%GTREE 2.1 Class initialization%>
    def __init__(self):
        print("initializing mapper class")

    #! <%GTREE 2.2 main mapper code%>
    def map_to_json(self, excel_data, mapping, schema, mapping_classification_id, mapping_id, schema_id):
        """
        Main entry point for mapping data to JSON.
        Determines the appropriate conversion approach based on IDs.
        """
        print("Determining conversion approach...")

        # Identify the conversion approach
        mapper_class_name = None

        # Step 1: Check if a specific mapping ID is known
        if mapping_id in KNOWN_MAPPINGS:
            mapper_class_name = KNOWN_MAPPINGS[mapping_id]
        # Step 2: Check if the (mapping_classification_id, schema_id) pair is known
        elif mapping_classification_id in KNOWN_MAPPING_CLASSIFICATIONS and schema_id in self.known_schemas:
            mapper_class_name = KNOWN_COMBINATIONS.get(
                (mapping_classification_id, schema_id),
                FALLBACK_MAPPER  # Default to the standard fallback mappeer (e.g. GenericMapper) if no specific match
            )
        else:
            # Step 3: Fallback to generic mapper
            mapper_class_name = FALLBACK_MAPPER
            print(f"Unknown mapping combination for classification ID '{mapping_classification_id}' and schema ID '{schema_id}'. Using {mapper_class_name}.")

        # Dynamically import and use the selected mapper class
        try:
            module = __import__(f"mappers.{mapper_class_name.lower()}", fromlist=[mapper_class_name])
            mapper_class = getattr(module, mapper_class_name)
            return mapper_class.map_data(excel_data, mapping, schema)
        except ImportError:
            raise ImportError(f"Mapper class '{mapper_class_name}' not found. Ensure it is implemented and imported.")

#============================   End Of File   ================================