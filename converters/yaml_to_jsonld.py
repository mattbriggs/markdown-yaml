import os
import json
import yaml
import re
import sys
import jsonschema
from jsonschema import validate

def extract_schema_path(yaml_text):
    match = re.search(r'\$schema\s*=\s*(.+)', yaml_text)
    if match:
        return match.group(1).strip()
    else:
        raise ValueError("No $schema directive found at the top of the YAML.")

def load_yaml_with_schema(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        raw_text = f.read()
    schema_path = extract_schema_path(raw_text)
    yaml_data = yaml.safe_load(raw_text)
    return schema_path, yaml_data

def load_json_schema(schema_path, base_dir):
    full_path = os.path.normpath(os.path.join(base_dir, schema_path))
    with open(full_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def validate_against_schema(instance, schema):
    try:
        validate(instance=instance, schema=schema)
        print("✅ JSON-LD is valid against the schema.")
    except jsonschema.exceptions.ValidationError as e:
        print("❌ Validation Error:")
        print(e.message)

def transform_yaml_data(yaml_data):
    # Rename 'introduction' to 'abstract' if present
    if 'introduction' in yaml_data:
        yaml_data['abstract'] = yaml_data.pop('introduction')

    # Ensure 'articleBody' exists
    if 'articleBody' not in yaml_data:
        raise ValueError("Required property 'articleBody' is missing from YAML data.")

    return yaml_data

def convert_yaml_to_jsonld(input_path):
    base_dir = os.path.dirname(input_path)
    schema_path, yaml_data = load_yaml_with_schema(input_path)
    yaml_data = transform_yaml_data(yaml_data)

    schema = load_json_schema(schema_path, base_dir)
    validate_against_schema(yaml_data, schema)

    output_path = os.path.splitext(input_path)[0] + '.jsonld'
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(yaml_data, f, indent=2, ensure_ascii=False)

    print(f"✅ JSON-LD saved to: {output_path}")
    return output_path

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python script.py <path/to/input.yaml>")
        sys.exit(1)

    input_yaml_path = sys.argv[1]
    convert_yaml_to_jsonld(input_yaml_path)
