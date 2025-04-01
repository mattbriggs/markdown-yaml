# JSONLD to HTML

This project provides a Python script that converts [JSON-LD](https://json-ld.org/) data into a simple, styled HTML page using the Jinja2 templating engine.

## Features
- Parses a JSON-LD file.
- Renders the content into a customizable HTML page.
- Uses Jinja2 templates for flexible formatting.

## Requirements

Install required packages using pip:

```bash
pip install -r requirements.txt
```

### `requirements.txt`
```
jinja2
```

## Usage

```bash
python jsonld_to_html.py path/to/data.json path/to/template.html path/to/output.html
```

## Example

### Command:
```bash
python jsonld_to_html.py data.json template.html output.html
```

### `data.json`
```json
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "The Future of AI in Everyday Life",
  "description": "A comprehensive look at how AI is shaping our world.",
  "author": {
    "@type": "Person",
    "name": "Dr. Alex Rivera"
  }
}
```

### `template.html`
```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{{ data.headline }}</title>
</head>
<body>
    <h1>{{ data.headline }}</h1>
    <p>{{ data.description }}</p>
    <p><strong>Author:</strong> {{ data.author.name }}</p>
</body>
</html>
```

### Output (`output.html`)
A fully rendered HTML page with values filled in from the JSON-LD data.

## License
MIT