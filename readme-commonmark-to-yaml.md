# Markdown to YAML Conversion Script

## Description
This Python script converts Markdown files (CommonMark/DocFX flavored) into structured YAML. It supports recursive resolution of Markdown includes and maintains structured, semantic clarity.

## Usage
```bash
python script.py <filename>.md
```


## Features
- Handles `!INCLUDE` directives recursively.
- Parses Markdown headings (`H1`, `H2`) into structured YAML sections.
- Converts Markdown components (alerts, tables, lists, code blocks) into semantic YAML blocks.
- Includes logging for error handling and debugging.

## Requirements
Install dependencies:
```bash
pip install -r requirements.txt
```

## Output
The script generates `<filename>.yml` containing structured YAML data conforming to the specified schema.

## Files
- `script.py`: Main conversion script.
- `requirements.txt`: Dependency list.

## Logging
Logging outputs key steps and errors, providing insights into execution flow and facilitating troubleshooting.

## License
MIT License
`