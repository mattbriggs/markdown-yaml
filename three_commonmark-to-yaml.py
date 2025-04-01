import sys
import re
import yaml
import logging
import os

logging.basicConfig(level=logging.INFO)

# YAML multiline scalar representation
def str_presenter(dumper, data):
    if len(data) > 80 or '\n' in data:
        return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='|')
    return dumper.represent_scalar('tag:yaml.org,2002:str', data)

yaml.add_representer(str, str_presenter)

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

# Identify components within a markdown section
def identify_components(section_content):
    components = []

    paragraphs = re.split(r'\n\n+', section_content.strip())

    for paragraph in paragraphs:
        if paragraph.startswith(':::'):
            component_name = paragraph.split()[0][3:].strip()
            component_content = '\n'.join(paragraph.split('\n')[1:-1]).strip()
        elif paragraph.startswith('```'):
            component_name = 'codeBlock'
            component_content = '\n'.join(paragraph.split('\n')[1:-1]).strip()
        elif paragraph.startswith('>'):
            component_name = 'quote'
            component_content = paragraph.lstrip('>').strip()
        else:
            component_name = 'markdown'
            component_content = paragraph.strip()

        components.append({component_name: component_content})

    return components

# Modular unit identification logic (extendable)
def identify_unit_type(title, components):
    # Example logic, extendable based on requirements
    if 'procedure' in title.lower():
        return 'procedure'
    elif 'concept' in title.lower():
        return 'concept'
    else:
        return 'general'

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

        unit = {
            'title': title,
            'summary': summary,
            'type': identify_unit_type(title, remaining_content),
            'components': identify_components(remaining_content)
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

    yaml_output = {'### YamlMime': 'article', 'metadata': metadata, 'units': structured_units}

    yaml_content = yaml.dump(yaml_output, sort_keys=False, allow_unicode=True, width=80)

    yaml_filepath = os.path.splitext(md_filepath)[0] + '.yml'
    with open(yaml_filepath, 'w') as f:
        f.write(yaml_content)

    logging.info(f"Converted Markdown to structured YAML: {yaml_filepath}")

if __name__ == '__main__':
    markdown_to_yaml(sys.argv[1])
