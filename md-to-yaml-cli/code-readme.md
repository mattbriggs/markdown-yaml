# 📄 **`code-readme.md`**

Here's a detailed starter readme to guide your iterative development. Here's a detailed **project scaffold** for your Markdown-to-YAML structured converter, organized using an Object-Oriented, pattern-based CLI approach. The structure emphasizes iterative development, easy testability, and clear modularity, making it ideal for ongoing collaboration with ChatGPT.

### 🗂 **Project Folder Structure**

```
md-to-yaml-cli/
├── README.md
├── code-readme.md
├── requirements.txt
├── config/
│   ├── compMapping.json
│   └── unitMapping.json
├── schemas/
│   ├── article.schema.json
│   └── metadata.schema.json
├── templates/
│   ├── article_template.yml
│   └── jsonld_template.json
├── src/
│   ├── __init__.py
│   ├── main.py
│   ├── cli.py
│   ├── parser/
│   │   ├── __init__.py
│   │   ├── markdown_parser.py
│   │   └── tests/
│   │       └── test_markdown_parser.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── component.py
│   │   ├── unit.py
│   │   └── article.py
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── validator.py
│   │   └── tests/
│   │       └── test_validator.py
│   └── exporter/
│       ├── __init__.py
│       ├── yaml_exporter.py
│       └── tests/
│           └── test_yaml_exporter.py
└── tests/
    └── run_all_tests.py
```


# Markdown-to-YAML CLI Converter

## Project Overview

This project parses Markdown files into structured YAML following Schema.org's `Article` schema, producing YAML, JSON-LD, and HTML outputs suitable for authoring and publishing workflows.

## Setup

### Requirements

Install Python dependencies:

```bash
pip install -r requirements.txt
```

## Iterative Development Guide

### 1. Develop in Modules

Each module can be independently developed and tested. Modules are:

- **Parser Module** (`markdown_parser.py`)
- **Models** (`component.py`, `unit.py`, `article.py`)
- **Validator Utility** (`validator.py`)
- **Exporter Module** (`yaml_exporter.py`)

### 2. Module Development Workflow

- Write initial functionality.
- Create corresponding test cases (`test_*.py`).
- Run tests to validate behavior.

Example:

```bash
python src/parser/tests/test_markdown_parser.py
```

### 3. Running the Whole Project

Use the CLI entry point defined in `cli.py`:

```bash
python src/main.py --input example.md --format yaml
```



## Creating and Updating Collateral

### JSON Schemas

Stored in `schemas/`:

- `article.schema.json`
- `metadata.schema.json`

### Configuration Files

Stored in `config/`:

- `compMapping.json`
- `unitMapping.json`

**Updating Config Files**:  
Edit JSON directly or through VS Code JSON editor for schema validation support.

### Templates

Stored in `templates/`:

- `article_template.yml`
- `jsonld_template.json`



## VS Code Authoring Experience

- YAML files contain a `$schema` header pointing to your JSON schema for IntelliSense.
- Schema validations and completions enhance authoring clarity.



## Testing Strategy

Run all tests with:

```bash
python tests/run_all_tests.py
```

This aggregates individual module tests into a single execution.



## Software Design Patterns Used

- **Builder Pattern**: for assembling articles from units and components.
- **Strategy Pattern**: for flexible parsing and exporting formats.
- **Factory Method**: to instantiate different exporter types (YAML, JSON-LD, HTML).
- **Validator Utility**: uses JSON schema for data validation.



## Future Iterations

Possible extensions include:

- Hierarchical nesting of units based on Markdown headings.
- Integration with Markdown AST parsing libraries for improved fidelity.
- Advanced validation and error-reporting mechanisms.



```



### 📌 **`requirements.txt`**

```text
PyYAML
jsonschema
argparse
markdown-it-py
pytest
```



### 🔧 **Code Scaffold Samples**

#### ✅ **CLI Entry Point** (`src/main.py`)

```python
from cli import run_cli

if __name__ == "__main__":
    run_cli()
```

#### ✅ **CLI Implementation** (`src/cli.py`)

```python
import argparse
from parser.markdown_parser import MarkdownParser
from exporter.yaml_exporter import YAMLExporter
from utils.validator import Validator

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
```



#### ✅ **Markdown Parser Module** (`markdown_parser.py`)

```python
class MarkdownParser:
    def __init__(self, filepath):
        self.filepath = filepath

    def parse(self):
        with open(self.filepath, 'r') as file:
            content = file.read()
        # Parse logic here
        return Article(...)  # Return Article model instance
```

#### ✅ **Validator Utility** (`validator.py`)

```python
import jsonschema
import json
import os

class Validator:
    def __init__(self):
        schema_path = os.path.join("schemas", "article.schema.json")
        with open(schema_path) as f:
            self.schema = json.load(f)

    def validate_article(self, article):
        jsonschema.validate(instance=article.to_dict(), schema=self.schema)
```



#### ✅ **YAML Exporter Module** (`yaml_exporter.py`)

```python
import yaml

class YAMLExporter:
    def __init__(self, article, output='output.yml'):
        self.article = article
        self.output = output

    def export(self):
        with open(self.output, 'w') as file:
            yaml.dump(self.article.to_dict(), file, sort_keys=False)
```



### 📋 **JSON Schema Example** (`schemas/article.schema.json`)

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["metadata", "units"],
  "properties": {
    "metadata": { "$ref": "./metadata.schema.json" },
    "units": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["title", "summary", "type", "components"],
        "properties": {
          "title": { "type": "string" },
          "summary": { "type": "string" },
          "type": { "type": "string" },
          "components": { "type": "array" }
        }
      }
    }
  }
}
```



### 🧪 **Aggregated Test Runner** (`tests/run_all_tests.py`)

```python
import unittest
from src.parser.tests.test_markdown_parser import TestMarkdownParser
from src.utils.tests.test_validator import TestValidator
from src.exporter.tests.test_yaml_exporter import TestYAMLExporter

if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTests(unittest.makeSuite(TestMarkdownParser))
    suite.addTests(unittest.makeSuite(TestValidator))
    suite.addTests(unittest.makeSuite(TestYAMLExporter))
    runner = unittest.TextTestRunner()
    runner.run(suite)
```

## How to Update and Extend compMapping.json:
	1.	Adding a New Component:
	•	Define a unique component key (e.g., compVideo).
	•	Include a clear description, required fields, and JSON Schema validation.
	2.	Updating Existing Components:
	•	Adjust the schema properties or required fields as needed.
	•	Ensure consistency in the schema definition.
	3.	Validation Integration:
	•	Update the Python validator to use this schema for validating each component parsed from Markdown.

⚙️ VS Code Integration:
	•	For easy editing and validation in VS Code, add the following to your .vscode/settings.json:

"json.schemas": [
  {
    "fileMatch": ["/config/compMapping.json"],
    "url": "http://json-schema.org/draft-07/schema#"
  }
]

This setup will give you intelligent autocomplete and immediate feedback on the JSON structure.

## unitMapping.json

Here's your initial **`unitMapping.json`** file. This mapping file defines how different types of document units are recognized based on the presence of certain component types. It helps automate the assignment of semantic unit types within your structured YAML files.

### 📄 **`config/unitMapping.json`**

```json
{
  "conceptUnit": {
    "description": "An explanatory or conceptual unit primarily consisting of paragraphs and optionally images or quotes.",
    "required_components": ["compParagraph"],
    "optional_components": ["compImage", "compQuote"]
  },
  "taskUnit": {
    "description": "A step-by-step procedural unit consisting of ordered lists and optionally paragraphs or code blocks.",
    "required_components": ["compListOrdered"],
    "optional_components": ["compParagraph", "compCodeBlock"]
  },
  "referenceUnit": {
    "description": "A structured reference, typically represented by tables or code blocks.",
    "required_components": ["compTable"],
    "optional_components": ["compCodeBlock"]
  },
  "codeExampleUnit": {
    "description": "A unit primarily providing code examples, possibly accompanied by explanatory paragraphs.",
    "required_components": ["compCodeBlock"],
    "optional_components": ["compParagraph"]
  },
  "summaryUnit": {
    "description": "A brief summarizing unit that includes paragraphs or quotes without complex structures.",
    "required_components": ["compParagraph"],
    "optional_components": ["compQuote"]
  },
  "imageUnit": {
    "description": "A visual unit centered around images, potentially supported by brief captions or paragraphs.",
    "required_components": ["compImage"],
    "optional_components": ["compParagraph"]
  }
}
```



### 🛠 **Explanation of Structure**

Each entry in the mapping includes:

- `description`: Clarifies the semantic meaning and typical use of the unit.
- `required_components`: Components that **must be present** for a unit to match this type.
- `optional_components`: Components that **may be present**, enriching the unit, but aren't required.



### 🖥 **How to Use `unitMapping.json`:**

In your Python script, implement a logic like this:

1. Identify the components in a parsed Markdown unit.
2. Iterate over each `unitMapping` entry, checking if required components are present.
3. Assign the first matching unit type.
4. Default to `"unknown"` if none matches.

Example logic in Python:

```python
def identify_unit_type(components, unit_mapping):
    present_components = set(components)

    for unit_type, rules in unit_mapping.items():
        required = set(rules['required_components'])
        if required.issubset(present_components):
            return unit_type
    return "unknown"
```



### ⚙️ **Extending the Mapping**

When you need to add or modify unit types:

- **Add New Unit Type**:
  1. Define clearly `description`, `required_components`, and `optional_components`.
  2. Update and save the `unitMapping.json`.

- **Modify Existing Unit**:
  - Adjust components or description for clarity and usability.



### ✨ **VS Code Integration**

Add to `.vscode/settings.json` for easier editing and IntelliSense:

```json
"json.schemas": [
  {
    "fileMatch": ["/config/unitMapping.json"],
    "url": "http://json-schema.org/draft-07/schema#"
  }
]
```



You now have a clear, semantic basis for automated unit typing and can integrate this into your content parser and validator.

## metadata.schema.json

Here's your initial **`metadata.schema.json`** file. This schema describes and validates the metadata portion of your structured YAML files, specifically aligning with your project's intent to create content compliant with the Schema.org `Article` schema.

### 📄 **`schemas/metadata.schema.json`**

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Metadata Schema for Structured Articles",
  "description": "Defines the metadata structure compliant with Schema.org's Article schema.",
  "type": "object",
  "required": [
    "title",
    "author",
    "datePublished",
    "description"
  ],
  "properties": {
    "title": {
      "type": "string",
      "description": "The main title of the article."
    },
    "author": {
      "type": "object",
      "required": ["name"],
      "properties": {
        "name": {
          "type": "string",
          "description": "The author's full name."
        },
        "url": {
          "type": "string",
          "format": "uri",
          "description": "A URL to the author's profile or homepage."
        }
      }
    },
    "datePublished": {
      "type": "string",
      "format": "date-time",
      "description": "ISO 8601 date and time when the article was first published."
    },
    "dateModified": {
      "type": "string",
      "format": "date-time",
      "description": "ISO 8601 date and time when the article was last updated."
    },
    "description": {
      "type": "string",
      "description": "A brief summary describing the article content."
    },
    "keywords": {
      "type": "array",
      "items": {
        "type": "string"
      },
      "description": "Keywords relevant to the article, useful for SEO and indexing."
    },
    "image": {
      "type": "string",
      "format": "uri",
      "description": "URL to an image representing or associated with the article."
    },
    "publisher": {
      "type": "object",
      "required": ["name"],
      "properties": {
        "name": {
          "type": "string",
          "description": "Publisher's organization or brand name."
        },
        "logo": {
          "type": "object",
          "required": ["url"],
          "properties": {
            "url": {
              "type": "string",
              "format": "uri",
              "description": "URL to the publisher's logo image."
            }
          }
        }
      }
    }
  },
  "additionalProperties": false
}
```



### 🛠 **Explanation of Schema Structure**

- **Required fields** ensure essential metadata is always present:
  - `title`, `author`, `datePublished`, and `description`.

- **Optional fields** enrich metadata:
  - `keywords` improve indexing.
  - `dateModified` tracks article updates.
  - `image` enhances visual representation.
  - `publisher` includes branding information.

- **Nested objects** (`author`, `publisher`) clearly structure person or organization entities.

- The schema is structured explicitly for compatibility with Schema.org’s `Article` type, facilitating downstream generation of structured data formats (e.g., JSON-LD).



### ⚙️ **Integrating and Validating in Python**

You can validate your parsed YAML metadata using the following snippet:

```python
import jsonschema
import yaml
import json

def validate_metadata(metadata):
    with open("schemas/metadata.schema.json") as schema_file:
        schema = json.load(schema_file)
    jsonschema.validate(instance=metadata, schema=schema)
```



### 🖥 **VS Code Integration**

Add to `.vscode/settings.json` for instant schema validation and auto-completion:

```json
"yaml.schemas": {
  "./schemas/metadata.schema.json": "metadata.yml"
}
```

Now you have a well-defined and standards-aligned schema for metadata, enhancing clarity, validation, and compliance with best practices.


Here's the fully-structured, object-oriented **`article.py`** model file for your `src/models/` directory. This class represents the entire parsed article, composed of metadata and units, using a clean and robust design suitable for iterative enhancement.

### 🧠 **Explanation of `article.py`**

This class encapsulates the structure of an article in a clean OOP manner:

- **Attributes:**
  - `metadata`: Dictionary validated against `metadata.schema.json`.
  - `units`: List containing structured units (components, paragraphs, tables, etc.).

- **Methods:**
  - `to_dict()`: Converts the `Article` object into a dictionary for easy serialization (YAML, JSON).
  - `add_unit(unit)`: Allows incremental construction of an article by adding units iteratively.
  - `validate(validator)`: Integrates with a validator utility class to ensure schema compliance.

### ✅ **Next Steps**

- **Unit Tests**: Create a corresponding test file (`test_article.py`) to ensure reliability.
- **Integration**: Use this class with your parser and exporter modules to create a complete pipeline.

This design supports your iterative development style with clearly defined structure and straightforward extensibility.


## component.py

Here's your structured, object-oriented **`component.py`** model file designed for clarity, extensibility, and iterative development in the `src/models/` directory. This model class represents individual content components parsed from Markdown, ready for serialization and validation:

### 🧠 **Explanation of `component.py`**

- **Attributes:**
  - `component_type`: Clearly identifies the component's semantic role (e.g., `compParagraph`, `compTable`).
  - `content`: Stores structured content matching definitions from your `compMapping.json`.

- **Methods:**
  - `to_dict()`: Allows easy conversion for YAML/JSON serialization.
  - `validate(validator)`: Integrates seamlessly with validation utilities using schemas from `compMapping.json`.



### ✅ **Next Steps:**

- **Unit Testing**: Write unit tests (`test_component.py`) to ensure correctness and robustness.
- **Integration**: Use this class in the parser to assemble structured components from Markdown.

This component model sets a robust foundation for structured content validation and easy integration into your structured content pipeline.

## unit.py

Here's your structured, object-oriented **`unit.py`** model file for the `src/models/` directory. This class represents content units parsed from Markdown sections, encapsulating titles, summaries, component collections, and inferred semantic types.

### 🧠 **Explanation of `unit.py`**

- **Attributes:**
  - `title`: Derived from Markdown headings.
  - `summary`: Concise description or overview.
  - `unit_type`: Semantic category based on `unitMapping.json`.
  - `components`: List of structured `Component` objects.

- **Methods:**
  - `to_dict()`: Facilitates serialization to YAML or JSON formats.
  - `add_component(component)`: Enables incremental unit construction.
  - `validate(validator)`: Ensures unit and all contained components meet defined schema criteria.



### ✅ **Next Steps:**

- **Unit Testing**: Develop tests (`test_unit.py`) to verify model reliability and correctness.
- **Integration**: Use this model to construct structured units within your parsing pipeline.

This structured, extensible model provides clear boundaries and validation, ensuring robust management and serialization of content units.

## article_template.yml

Here's your clear and concise **`article_template.yml`** file for the `templates/` directory. This YAML template provides a structured starting point that aligns directly with your `article.py` model, schema definitions, and JSON-LD standards.  


### 🧠 **How to use this template:**

- **Starting an article**: Copy this template and replace placeholders with your article-specific data.
- **VS Code Integration**: This template includes a schema comment (`yaml-language-server`) for immediate YAML validation and intelligent completions.



### ✅ **Next Steps:**

- Populate with actual article data during parsing or manual authoring.
- Adjust and extend as new components or unit types are added.

This clean and fully aligned template supports author-friendly YAML generation, ensuring consistency with schemas and facilitating smooth content management.

## jsonld_template.json

Here's your structured and well-defined **`jsonld_template.json`** file, located appropriately in your project's `templates/` directory. This template enables easy conversion of your structured YAML articles into fully compliant Schema.org JSON-LD representations.  





### 🛠 **Explanation of JSON-LD Structure**

- Fully compatible with **Schema.org Article schema**.
- Metadata elements (`headline`, `author`, `datePublished`, etc.) are directly mapped from your YAML article metadata.
- `articleBody` provides the main content body in plain text or HTML format.
- `articleSection` array reflects individual units from YAML, allowing structured content indexing and improved SEO/rich snippets.



### 🖥 **How to Use this Template**

- Use your YAML structured content to populate the fields:
  - Replace placeholders (`headline`, `author`, `datePublished`, etc.) directly from YAML metadata.
  - Concatenate or render YAML units into HTML snippets for `articleSection`.
  - Populate `articleBody` if needed for search indexing or summary purposes.

Example Python conversion snippet:

```python
import json
from jinja2 import Template

def render_jsonld(article_data):
    with open('templates/jsonld_template.json') as f:
        jsonld_template = json.load(f)

    jsonld_template['headline'] = article_data['metadata']['title']
    jsonld_template['author']['name'] = article_data['metadata']['author']['name']
    # Populate remaining fields similarly...

    return json.dumps(jsonld_template, indent=2)
```



### ✅ **Next Steps:**

- Integrate template rendering into your YAML-to-JSON-LD conversion module.
- Create and run tests to ensure consistency between YAML and generated JSON-LD outputs.

This structured, schema-compliant template greatly simplifies the process of converting structured YAML content into semantic, SEO-friendly JSON-LD outputs.


## main.py

Here's your clear and modular **`main.py`** script serving as the primary CLI entry point for the Markdown-to-YAML structured converter. This script is designed for extensibility, ease of testing, and smooth integration with your structured modules and validation mechanisms.

### 🛠 **Explanation of `main.py`:**

- **CLI Arguments**:
  - `--input`: Markdown file path (required).
  - `--output`: YAML file path (optional; defaults to same name as input).
  - `--validate`: Optional validation against defined schemas.

- **Pipeline**:
  - Markdown file is parsed by `MarkdownParser`.
  - Parsed data is structured into an `Article` object.
  - Validation (optional) ensures schema adherence.
  - Structured YAML is exported via `YAMLExporter`.

- **Logging** provides clear feedback during CLI execution.

---

### ✅ **Next Steps:**

- Implement detailed parsing logic inside `MarkdownParser`.
- Integrate validation logic inside `Validator`.
- Test and iterate through modular development and continuous integration.

This structured, clean CLI provides a strong foundation for incremental feature development, ensuring maintainability and ease of testing.

##

🧪 How to Run Tests:

Run individual tests directly:

python src/parser/tests/test_markdown_parser.py
python src/utils/tests/test_validator.py
python src/exporter/tests/test_yaml_exporter.py

Or collectively, using your existing run_all_tests.py:

python tests/run_all_tests.py

Ensure that your run_all_tests.py correctly discovers and aggregates these test cases.

⸻

⚙️ Next Steps:
	•	Verify each test passes and handle any failing tests by debugging the related modules.
	•	Add additional test cases as your parsing and validation logic become more sophisticated.
	•	Integrate these tests into CI workflows for automated verification during development iterations.

These comprehensive test scripts ensure your project’s core functionalities are rigorously validated, supporting smooth and confident iterative development.