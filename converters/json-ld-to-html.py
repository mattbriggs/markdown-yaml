# jsonld_to_html.py
import json
from pathlib import Path
from jinja2 import Template

def load_jsonld(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def render_html(data, template_path):
    with open(template_path, 'r', encoding='utf-8') as f:
        template = Template(f.read())
    return template.render(data=data)

def save_html(html_content, output_path):
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)

def main():
    import argparse
    parser = argparse.ArgumentParser(description='Convert JSON-LD data to HTML.')
    parser.add_argument('jsonld', help='Path to the JSON-LD file')
    parser.add_argument('template', help='Path to the HTML Jinja2 template')
    parser.add_argument('output', help='Path to save the output HTML')
    args = parser.parse_args()

    data = load_jsonld(args.jsonld)
    html = render_html(data, args.template)
    save_html(html, args.output)

if __name__ == '__main__':
    main()
