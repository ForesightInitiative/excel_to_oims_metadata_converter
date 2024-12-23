# Excel to OIMS Metadata Converter ![Python](img/pythonbadge3_9plus.svg)

## Overview

The **Excel to OIMS Metadata Converter** is a standalone tool designed to transform metadata stored in Excel files into OIMS-compatible JSON files. The tool ensures adherence to OIMS standards through robust validation mechanisms and modular design.

December 11, 2024: inital commit of the code under dec=velopemnt
December 16, 2024: up-date of the underlying code base (still under development)
December 16, 2024: The application is still under development. please contact g.kruseman@cgiar.org if you want to contribute to the development.

Future (2025 and beyomnd) extensions include:

- Integration into a graphical user interface (GUI) toolkit.
- Transformation into a web application for broader accessibility.

## Current Features (under development)

- **Modular Design**: Reusable components for validation, mapping, and file handling.
- **Dynamic Mappers**: Supports both specific and generic mapping logic.
- **Validation Framework**: Ensures metadata conformity with OIMS standards.
- **Extensibility**: Easily add new mappers, schemas, or validators.
- **Error and Process Logging**: Logs errors and process steps for reference.

## Installation

Clone the repository and install dependencies:

```bash
git clone https://github.com/ForesightInitiative/excel_to_oims_metadata_converter.git
cd excel_to_oims_metadata_converter
pip install -r requirements.txt
```

## Usage

Run the tool using the following command:

```markdown
python metadata_converter.py --settings config/settings.json
```

## Folder Structure

excel_to_oims_metadata_converter/


|-- metadata_converter.py # Entry point for the tool 


|-- modules/              # General-purpose modules


|-- utils/                # Utility modules (e.g., logging, validators)


|-- mappers/              # Specific mappers


|-- validators/           # Input/output validation modules



|-- oims_structures/      # OIMS-compatible schemas and related files


|-- json/                 # Default JSON files


|-- logs/                 # Process and error logs


|-- config/               # location of the user settings file 

 
|-- img/                  # image files


|-- documentation         # documentation files


|-- README.md             # Basic documentation


|-- requirements.txt      # Python dependencies


|-- LICENSE               # Open-source license: GPL 3.0



## Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature (`git checkout -b feature-name`).
3. Commit your changes (`git commit -m "Description of changes"`).
4. Push to your fork and submit a pull request.

## Contact

For questions or support, contact: - Gideon Kruseman ([gkruseman@gmail.com](mailto:gkruseman@gmail.com))
