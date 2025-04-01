
# YAML to JSON-LD Converter

This Python script converts a YAML file into JSON-LD format using a `$schema` directive found in a YAML comment.

## Features

- Extracts `$schema` from the YAML top comment
- Validates the converted JSON-LD against the specified schema
- Saves the result as a `.jsonld` file next to the input file

## Requirements

Install dependencies using:

```bash
pip install pyyaml jsonschema
```

## Usage

```bash
python yaml_to_jsonld.py /path/to/input.yaml
```

This will produce `/path/to/input.jsonld` and validate it using the schema specified like this in the YAML file:

```yaml
# yaml-language-server: $schema=../article.schema.v1v1.full.json
```
