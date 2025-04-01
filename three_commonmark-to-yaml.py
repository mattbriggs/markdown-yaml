import sys
import re
import yaml
import logging
import os
import json

logging.basicConfig(level=logging.INFO)

# YAML multiline scalar representation for readability
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

            # Remove YAML metadata header from included file
            included_content = remove_metadata(included_content)

            return resolve_includes(included_content, os.path.dirname(include_path))
        except FileNotFoundError:
            logging.error(f"Include file not found: {include_path}")
            return ''

    return include_pattern.sub(replace_include, content)

def remove_metadata(content):
    """Extracts markdown content excluding YAML metadata header."""
    metadata_pattern = re.compile(r'^---\s*\n.*?\n---\s*\n', re.DOTALL)
    return metadata_pattern.sub('', content, count=1).strip()

# Parse nested lists explicitly into structured items with recursion
def parse_nested_list_items(list_content, ordered=False):
    lines = list_content.splitlines()
    items = []
    stack = []

    for line in lines:
        indent = len(line) - len(line.lstrip())
        item_text = re.sub(r'^[-*+]|\d+\.', '', line).strip()
        item = {'item': item_text}

        while stack and stack[-1][0] >= indent:
            stack.pop()

        if stack:
            parent_item = stack[-1][1]
            if 'children' not in parent_item:
                parent_item['children'] = []
            parent_item['children'].append(item)
        else:
            items.append(item)

        stack.append((indent, item))

    return items

# Recursively parse nested components such as lists and tables
def parse_nested_components(content):
    lines = content.splitlines()
    components = []
    buffer = []
    current_component_type = None

    # Helper functions
    def flush_buffer():
        nonlocal buffer, current_component_type
        if buffer:
            text = "\n".join(buffer).strip()
            if current_component_type == 'listOrdered':
                components.append({'compListOrdered': {'items': parse_nested_list_items(text, ordered=True)}})
            elif current_component_type == 'listUnordered':
                components.append({'compListUnordered': {'items': parse_nested_list_items(text, ordered=False)}})
            elif current_component_type == 'table':
                components.append({'compTable': parse_markdown_table(text)})
            else:
                components.append({'compParagraph': {'content': text}})
            buffer = []

    # Line-by-line processing
    for line in lines:
        stripped_line = line.strip()
        if re.match(r'^(\d+\.\s)', stripped_line):  # ordered list
            if current_component_type not in [None, 'listOrdered']:
                flush_buffer()
            current_component_type = 'listOrdered'
            buffer.append(line)
        elif re.match(r'^([-*+]\s)', stripped_line):  # unordered list
            if current_component_type not in [None, 'listUnordered']:
                flush_buffer()
            current_component_type = 'listUnordered'
            buffer.append(line)
        elif re.match(r'^\|.*\|$', stripped_line):  # tables
            if current_component_type not in [None, 'table']:
                flush_buffer()
            current_component_type = 'table'
            buffer.append(line)
        elif stripped_line == '':
            flush_buffer()
            current_component_type = None
        else:
            if current_component_type not in [None, 'paragraph']:
                flush_buffer()
            current_component_type = 'paragraph'
            buffer.append(line)

    flush_buffer()
    return components

def parse_markdown_table(table_markdown):
    lines = table_markdown.strip().split('\n')

    if len(lines) < 2:
        return {'headers': [], 'rows': []}

    headers = [cell.strip() for cell in lines[0].strip('|').split('|')]

    # Validate separator
    separator = lines[1]
    if not re.match(r'^\s*\|[-:\s|]+\|\s*$', separator):
        return {'headers': headers, 'rows': []}

    rows = []
    for line in lines[2:]:
        if line.strip().startswith('|'):
            cells = [cell.strip() for cell in line.strip('|').split('|')]
            if len(cells) == len(headers):
                rows.append({headers[i]: cells[i] for i in range(len(headers))})

    return {'headers': headers, 'rows': rows}

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

        components = parse_nested_components(remaining_content)
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
        f.write('# yaml-language-server: $schema=../article.schema.v1v1.full.json\n')
        f.write(yaml_content)

    logging.info(f"Converted Markdown to structured YAML: {yaml_filepath}")

if __name__ == '__main__':
    markdown_to_yaml(sys.argv[1])
