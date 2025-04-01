import sys
import re
import yaml
import logging
import os
from datetime import datetime

logging.basicConfig(level=logging.INFO)

# YAML representer for multiline strings
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

# Extract metadata and content from markdown
def extract_metadata(content):
    metadata = {}
    metadata_match = re.search(r'^---\n(.*?)\n---\n', content, re.DOTALL)
    if metadata_match:
        metadata_raw = metadata_match.group(1)
        for line in metadata_raw.split('\n'):
            if ':' in line:
                key, value = line.split(':', 1)
                metadata[key.strip()] = value.strip()
        content = content[metadata_match.end():]
    return metadata, content

# Main conversion function
def markdown_to_yaml(md_filepath):
    base_path = os.path.dirname(md_filepath)

    with open(md_filepath, 'r') as f:
        content = f.read()

    content = resolve_includes(content, base_path)
    metadata, body_content = extract_metadata(content)

    headline_match = re.search(r'^#\s+(.*)', body_content, re.MULTILINE)
    headline = headline_match.group(1).strip() if headline_match else ""

    article_body = re.sub(r'^#\s+.*', '', body_content, count=1, flags=re.MULTILINE).strip()

    yaml_structure = {
        '@context': 'https://schema.org',
        '@type': 'Article',
        'headline': headline,
        'articleBody': article_body,
        'datePublished': metadata.get('datePublished', datetime.utcnow().isoformat()),
        'author': {'name': metadata.get('author', 'Unknown')},
        'keywords': metadata.get('keywords', '').split(',') if 'keywords' in metadata else [],
        'description': metadata.get('description', ''),
        'inLanguage': metadata.get('language', 'en'),
        'url': metadata.get('url', ''),
        'identifier': metadata.get('id', '')
    }

    yaml_content = '# yaml-language-server: $schema=../article.schema.v1v1.full.json\n'
    yaml_content += yaml.dump(yaml_structure, sort_keys=False, allow_unicode=True)

    yaml_filepath = os.path.splitext(md_filepath)[0] + '.yml'
    with open(yaml_filepath, 'w') as f:
        f.write(yaml_content)

    logging.info(f"Converted Markdown to YAML: {yaml_filepath}")

if __name__ == '__main__':
    markdown_to_yaml(sys.argv[1])
