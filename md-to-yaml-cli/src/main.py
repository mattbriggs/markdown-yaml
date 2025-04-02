import argparse
import logging
from parser.markdown_parser import MarkdownParser
from models.article import Article
from exporter.yaml_exporter import YAMLExporter
from utils.validator import Validator
import os

logging.basicConfig(level=logging.INFO)


def main():
    parser = argparse.ArgumentParser(description="Markdown-to-YAML structured converter CLI.")
    parser.add_argument("--input", required=True, help="Path to input Markdown file.")
    parser.add_argument("--output", help="Path to output YAML file.")
    parser.add_argument("--validate", action="store_true", help="Validate output against schema.")

    args = parser.parse_args()

    input_path = args.input
    output_path = args.output or os.path.splitext(input_path)[0] + ".yml"

    logging.info(f"Parsing Markdown file: {input_path}")

    md_parser = MarkdownParser(input_path)
    article_data = md_parser.parse()

    article = Article(metadata=article_data['metadata'], units=article_data['units'])

    if args.validate:
        logging.info("Validating article...")
        validator = Validator()
        article.validate(validator)
        logging.info("Validation successful.")

    logging.info(f"Exporting structured YAML to: {output_path}")

    exporter = YAMLExporter(article, output=output_path)
    exporter.export()

    logging.info("Markdown-to-YAML conversion complete.")


if __name__ == "__main__":
    main()
