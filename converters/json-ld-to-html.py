# jsonld_to_html_refactored.py
import json
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, select_autoescape
import argparse


def load_jsonld(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def render_html(data, template_name):
    env = Environment(
        loader=FileSystemLoader(searchpath=Path(template_name).parent),
        autoescape=select_autoescape(["html", "xml"])
    )
    template = env.get_template(Path(template_name).name)
    return template.render(
        headline=data.get("headline"),
        author=data.get("author", {}).get("name"),
        datePublished=data.get("datePublished"),
        description=data.get("description"),
        article_parts=[part for part in data.get("hasPart", []) if part.get('text').strip()]
    )


def save_html(html_content, output_path):
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)


def main():
    parser = argparse.ArgumentParser(description='Convert JSON-LD to structured HTML.')
    parser.add_argument('jsonld_path', help='Path to the JSON-LD file')
    parser.add_argument('template_path', help='Path to the Jinja2 template file')
    parser.add_argument('output_path', help='Path to save the output HTML file')
    args = parser.parse_args()

    data = load_jsonld(args.jsonld_path)
    html = render_html(data, args.template_path)
    save_html(html, args.output_path)


if __name__ == '__main__':
    main()