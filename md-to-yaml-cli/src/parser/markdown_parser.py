import re
import yaml
import os
import logging
from typing import Dict, Any, List
from src.models.component import Component
from src.models.unit import Unit

logging.basicConfig(level=logging.INFO)


class MarkdownParser:
    def __init__(self, filepath: str):
        self.filepath = filepath
        self.base_path = os.path.dirname(filepath)

    def parse(self) -> Dict[str, Any]:
        with open(self.filepath, 'r') as file:
            content = file.read()

        content = self.resolve_includes(content)
        metadata, markdown_body = self.extract_metadata(content)
        units = self.split_into_units(markdown_body)

        structured_units = [unit.to_dict() for unit in units]

        return {"metadata": metadata, "units": structured_units}

    def resolve_includes(self, content: str) -> str:
        include_pattern = re.compile(r'\[!INCLUDE \[.*?\]\((.*?)\)\]')

        def replace_include(match):
            include_path = os.path.join(self.base_path, match.group(1))
            try:
                with open(include_path, 'r', encoding='utf-8') as file:
                    included_content = file.read()
                    
                # Remove YAML metadata from included content
                included_body = self.extract_markdown_body(included_content)

                # Recursively resolve nested includes
                return self.resolve_includes(included_body)
            except FileNotFoundError:
                logger.error(f"Include file not found: {include_path}")
                return ''

        return include_pattern.sub(replace_include, content)

    def extract_markdown_body(self, content: str) -> str:
        """
        Removes YAML front matter metadata and returns only the markdown body.
        """
        metadata_pattern = re.compile(r'^---\s*\n.*?\n---\s*\n', re.DOTALL)
        markdown_body = metadata_pattern.sub('', content).strip()
        return markdown_body

    def extract_metadata(self, content: str) -> (Dict[str, Any], str):
        metadata = {}
        metadata_match = re.match(r'^---\n(.*?)\n---\n', content, re.DOTALL)

        if metadata_match:
            metadata_str = metadata_match.group(1)
            metadata = yaml.safe_load(metadata_str)
            content = content[metadata_match.end():]

        return metadata, content

    def split_into_units(self, content: str) -> List[Unit]:
        unit_sections = re.split(r'(?=^# )|(?=^## )', content, flags=re.MULTILINE)
        units = []

        for section in unit_sections:
            section = section.strip()
            if not section:
                continue

            lines = section.splitlines()
            title = lines.pop(0).lstrip('#').strip()
            summary = lines.pop(0).strip() if lines else ''
            remaining_content = '\n'.join(lines).strip()

            components = self.extract_components(remaining_content)
            unit_type = self.identify_unit_type(components)

            unit = Unit(title=title, summary=summary, unit_type=unit_type, components=components)
            units.append(unit)

        return units

    def extract_components(self, content: str) -> List[Component]:
        lines = content.split('\n')
        components = []
        buffer = []
        current_type = None

        for line in lines + ['']:
            if line.startswith('- ') or line.startswith('* '):
                if current_type != 'compListUnordered':
                    self.flush_buffer(buffer, current_type, components)
                    buffer = []
                    current_type = 'compListUnordered'
                buffer.append(line)
            elif re.match(r'^\d+\. ', line):
                if current_type != 'compListOrdered':
                    self.flush_buffer(buffer, current_type, components)
                    buffer = []
                    current_type = 'compListOrdered'
                buffer.append(line)
            elif line.startswith('|'):
                if current_type != 'compTable':
                    self.flush_buffer(buffer, current_type, components)
                    buffer = []
                    current_type = 'compTable'
                buffer.append(line)
            elif line.strip() == '':
                self.flush_buffer(buffer, current_type, components)
                buffer = []
                current_type = None
            else:
                if current_type != 'compParagraph':
                    self.flush_buffer(buffer, current_type, components)
                    buffer = []
                    current_type = 'compParagraph'
                buffer.append(line)

        return components

    def flush_buffer(self, buffer, comp_type, components):
        if not buffer:
            return

        content_str = '\n'.join(buffer).strip()
        if comp_type == 'compParagraph':
            components.append(Component(comp_type, {"content": content_str}))
        elif comp_type in ['compListOrdered', 'compListUnordered']:
            items = [re.sub(r'^[-*\d+.]+\s+', '', item).strip() for item in buffer]
            components.append(Component(comp_type, {"items": [{"item": i} for i in items]}))
        elif comp_type == 'compTable':
            components.append(Component(comp_type, {"raw_table": content_str}))

    def identify_unit_type(self, components: List[Component]) -> str:
        component_types = {c.component_type for c in components}
        if 'compListOrdered' in component_types:
            return 'taskUnit'
        elif 'compTable' in component_types:
            return 'referenceUnit'
        elif 'compParagraph' in component_types:
            return 'conceptUnit'
        else:
            return 'unknown'