#<%REGION File header%>
#=============================================================================
# File      : converter_data.py
# Author    : Gideon Kruseman <g.kruseman@cgiar.org>
# Version   : 1.0.0
# Date      : 12/10/2024 5:05:37 PM
# Changed   : 12/10/2024 5:05:39 PM
# Changed by: Gideon Kruseman <g.kruseman@cgiar.org>
# Internal remarks   :
"""
version 1.0.0  2024-12-10 start. This module will contain the known mapping classifications,
        mappings, and schemas as constants or dictionaries.  see also Kruseman, G. 2024.
        MS Excel to OIMS mapping schema GENNOVATE_001: Version 1.0.0.0. CGIAR Foresight Initiative
        report. Rome: Alliance Bioversity International and CIAT.

"""
# version history information   :
"""
- Version 1.0.0: Initial implementation of the metadata conversion tool.
"""

#=============================================================================
#<%/REGION File header%>

#! <%GTREE 1 identify what conversion is needed%>
#! <%GTREE 1.1 Known mapping classifications%>
# Known mapping classifications
KNOWN_MAPPING_CLASSIFICATIONS = {
    "EXCEL_TO_OIMS_MAPPING_001":"Excel2OimsMapper_001",
    "EXCEL_TO_OIMS_MAPPING_BASE":"GenericMapper",
    "EXCEL_TO_OIMS_MAPPING_BASE_Ext_001":"ExtendedGenericMapper"
}

#! <%GTREE 1.2 Known mappings%>
# Known mappings
KNOWN_MAPPINGS = {
    "GENNOVATE_001": "GennovateMapper"}
}



#! <%GTREE 1.3 Known primary metadata schemas%>
# Known schemas
KNOWN_SCHEMAS = {
    "Foresight data metametadata":"BaseForesightMapper"
}

#! <%GTREE 1.4 Known combinations of mapping classes and primary metadata schemas%>
# Known combinations
KNOWN_COMBINATIONS = {
            ("EXCEL_TO_OIMS_MAPPING_001", "Foresight data metametadata"): "StandardForesightMapper",
            ("EXCEL_TO_OIMS_MAPPING_BASE", "Foresight data metametadata"): "GenericMapper",
            ("EXCEL_TO_OIMS_MAPPING_BASE_Ext_001","Foresight data metametadata)":"ExtendedGenericMapper"
        }


#! <%GTREE 1.5 Fallback option for converters%>
FALLBACK_MAPPER =  "GenericMapper"

#============================   End Of File   ================================