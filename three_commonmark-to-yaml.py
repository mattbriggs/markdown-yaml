import sys
import re
import yaml
import logging
import os
import json

logging.basicConfig(level=logging.INFO)

# YAML multiline scalar representation
def str_presenter(dumper, data):
    if '\n' in data or len(data) > 80:
        return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='|')
    return dumper.represent_scalar('tag:yaml.org,2002:str', data)

yaml.add_representer(str, str_presenter)

# Load component and unit mappings
with open('compMapping.json') as f:
    COMPONENT_MAP = json.load(f)

with open('unitMapping.json') as f:
    UNIT_MAP = json.load(f)

# Resolve recursive Markdown includes
def resolve_includes(content, base_path):
    include_pattern = re.compile(r'\[!INCLUDE \[.*?\]\((.*?)\)\]')

    def replace_include(match):
        include_path = os.path.join(base_path, match.group(1))
        try:
            with open(include_path, 'r') as file:
                included_content = file.read()
            return resolve_includes(included_content, os.path.dirname(include_path))
        except FileNotFoundError:
            logging.error(f"Include file not found: {include_path}")
            return ''

    return include_pattern.sub(replace_include, content)

# Identify components using schema-based mapping
def identify_components(section_content):
    components = []

    for comp_name, comp_pattern in COMPONENT_MAP.items():
        matches = re.findall(comp_pattern, section_content, re.MULTILINE | re.DOTALL)
        for match in matches:
            # Handle tuples returned by regex patterns with multiple groups
            if isinstance(match, tuple):
                match_content = ' '.join(m.strip() for m in match if m.strip())
            else:
                match_content = match.strip()

            components.append({comp_name: match_content})
            section_content = section_content.replace(match_content, '')

    # Remaining content as generic markdown
    if section_content.strip():
        components.append({'markdown': section_content.strip()})

    return components

# Modular unit identification using external mapping
def identify_unit_type(components):
    component_types = {list(c.keys())[0] for c in components}

    for unit_type, required_components in UNIT_MAP.items():
        if required_components and all(rc in component_types for rc in required_components):
            return unit_type

    return 'unknown'

# Extract metadata and split markdown into structured units
def split_markdown_units(content):
    sections = re.split(r'(?=^# )|(?=^## )', content, flags=re.MULTILINE)
    structured_units = []

    # Metadata extraction
    metadata_raw = sections.pop(0)
    metadata = {}
    metadata_match = re.search(r'^---\n(.*?)\n---\n', metadata_raw, re.DOTALL)
    if metadata_match:
        for line in metadata_match.group(1).split('\n'):
            if ':' in line:
                key, value = line.split(':', 1)
                metadata[key.strip()] = value.strip()

    for section in sections:
        lines = section.strip().split('\n')
        title = lines.pop(0).lstrip('#').strip()
        summary = lines.pop(0).strip() if lines else ''
        remaining_content = '\n'.join(lines).strip()

        components = identify_components(remaining_content)
        unit_type = identify_unit_type(components)

        unit = {
            'title': title,
            'summary': summary,
            'type': unit_type,
            'components': components
        }

        structured_units.append(unit)

    return metadata, structured_units

# Main conversion function
def markdown_to_yaml(md_filepath):
    base_path = os.path.dirname(md_filepath)

    with open(md_filepath, 'r') as f:
        content = f.read()

    content = resolve_includes(content, base_path)
    metadata, structured_units = split_markdown_units(content)

    yaml_output = {'metadata': metadata, 'units': structured_units}

    yaml_content = yaml.dump(yaml_output, sort_keys=False, allow_unicode=True, default_flow_style=False, width=float('inf'))

    yaml_filepath = os.path.splitext(md_filepath)[0] + '.yml'
    with open(yaml_filepath, 'w') as f:
        f.write(yaml_content)

    logging.info(f"Converted Markdown to structured YAML: {yaml_filepath}")

if __name__ == '__main__':
    markdown_to_yaml(sys.argv[1])
