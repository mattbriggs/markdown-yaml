import argparse
from src.parser.markdown_parser import MarkdownParser
from src.exporter.yaml_exporter import YAMLExporter
from src.utils.validator import Validator

def run_cli():
    parser = argparse.ArgumentParser(description='Markdown-to-YAML CLI')
    parser.add_argument('--input', required=True, help='Markdown file path')
    parser.add_argument('--format', choices=['yaml', 'jsonld', 'html'], default='yaml')
    args = parser.parse_args()

    md_parser = MarkdownParser(args.input)
    article = md_parser.parse()

    validator = Validator()
    validator.validate_article(article)

    exporter = YAMLExporter(article)
    exporter.export()