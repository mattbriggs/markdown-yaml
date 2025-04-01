import sys
import re
import yaml
import logging
import os

logging.basicConfig(level=logging.INFO)

# Custom YAML representer for multiline strings
def str_presenter(dumper, data):
    if '\n' in data:
        return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='|')
    return dumper.represent_scalar('tag:yaml.org,2002:str', data)

yaml.add_representer(str, str_presenter)

# Handle recursive includes
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

# Parse Markdown into sections
def parse_markdown_sections(content):
    sections = []

    metadata_match = re.search(r'---\n(.*?)\n---', content, re.DOTALL)

    metadata = {}
    if metadata_match:
        metadata_raw = metadata_match.group(1)
        for line in metadata_raw.split('\n'):
            if line.strip().startswith('#customer intent:'):
                key, value = line.split(':', 1)
                metadata['customer-intent'] = value.strip()
            elif ':' in line:
                key, value = line.split(':', 1)
                metadata[key.strip()] = value.strip()

        content = content[metadata_match.end():]

    sections.append({'metadata': metadata})

    h1_split = re.split(r'\n#\s+', content, maxsplit=1)
    if len(h1_split) > 1:
        h1_title, rest = h1_split[1].split('\n', 1)
        h2_split = re.split(r'\n##\s+', rest)
        sections.append({'title': h1_title.strip(), 'type': 'introduction', 'content': h2_split[0].strip()})

        for h2_section in h2_split[1:]:
            h2_title, *h2_content = h2_section.split('\n', 1)
            sections.append({
                'title': h2_title.strip(),
                'type': 'unknown',
                'content': h2_content[0].strip() if h2_content else ''
            })

    return sections

# Convert Markdown components preserving their original order
def convert_components(title, type_, section_content):
    unit = {'title': title, 'type': type_}

    lines = section_content.split('\n')
    components = []

    alert_pattern = re.compile(r'> \[!(\w+)(?: [^\]]*)?\]\s*(.*)')
    codeblock_pattern = re.compile(r'```(\w+)?\n([\s\S]*?)```', re.MULTILINE)

    i = 0
    while i < len(lines):
        line = lines[i]

        if match := alert_pattern.match(line):
            alert_type = match.group(1).lower()
            alert_content = [match.group(2).strip()]
            i += 1
            while i < len(lines) and lines[i].startswith('>'):
                alert_content.append(lines[i].lstrip('> ').rstrip())
                i += 1
            components.append(('alert', {'type': alert_type, 'notice': '\n'.join(alert_content).strip()}))
        elif line.startswith('```'):
            code_match = codeblock_pattern.match('\n'.join(lines[i:]))
            if code_match:
                components.append(('codeBlock', {'type': code_match.group(1) or '', 'code': code_match.group(2).strip()}))
                i += code_match.group(0).count('\n') + 1
        elif line.startswith('|'):
            table_lines = []
            while i < len(lines) and lines[i].startswith('|'):
                table_lines.append(lines[i])
                i += 1
            components.append(('table', '\n'.join(table_lines).strip()))
        elif re.match(r'^\d+\.', line):
            items = []
            while i < len(lines) and re.match(r'^\d+\.', lines[i]):
                items.append({'item': lines[i].split('.', 1)[1].strip()})
                i += 1
            components.append(('listOrdered', items))
        elif line.startswith('- '):
            items = []
            while i < len(lines) and lines[i].startswith('- '):
                items.append({'item': lines[i][2:].strip()})
                i += 1
            components.append(('listUnordered', items))
        else:
            buffer = []
            while i < len(lines) and lines[i] and not re.match(r'^(>|```|\||\d+\.|- )', lines[i]):
                buffer.append(lines[i])
                i += 1
            if buffer:
                components.append(('summary', '\n'.join(buffer).strip()))
            else:
                i += 1

    for comp_type, comp_content in components:
        if comp_type in unit:
            if isinstance(unit[comp_type], list):
                unit[comp_type].append(comp_content)
            else:
                unit[comp_type] = [unit[comp_type], comp_content]
        else:
            unit[comp_type] = comp_content

    return unit

def markdown_to_yaml(md_filepath):
    base_path = os.path.dirname(md_filepath)

    with open(md_filepath, 'r') as f:
        content = f.read()

    content = resolve_includes(content, base_path)
    sections = parse_markdown_sections(content)

    yaml_structure = {'metadata': sections[0].get('metadata', {}), 'contents': []}

    for sec in sections[1:]:
        yaml_structure['contents'].append(convert_components(sec['title'], sec['type'], sec['content']))

    yaml_content = '# yaml-language-server: $schema=article.schema.v1v1.json\n' + yaml.dump(yaml_structure, sort_keys=False, allow_unicode=True)

    yaml_filepath = os.path.splitext(md_filepath)[0] + '.yml'
    with open(yaml_filepath, 'w') as f:
        f.write(yaml_content)

    logging.info(f"Converted Markdown to YAML: {yaml_filepath}")

if __name__ == '__main__':
    markdown_to_yaml(sys.argv[1])