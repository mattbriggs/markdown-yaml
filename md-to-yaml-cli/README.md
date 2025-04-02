# Markdown-to-YAML CLI Converter

A command-line tool built with Python that converts Markdown files into structured, schema-compliant YAML files, which are compatible with Schema.org's Article schema. This project supports structured documentation workflows, JSON-LD structured data generation, and HTML rendering.



## 🎯 Project Goals

- Convert Markdown documents into structured YAML format.
- Ensure schema compliance (JSON Schema, Schema.org).
- Support author-friendly YAML for documentation and structured data.
- Enable seamless JSON-LD and HTML output generation.
- Facilitate iterative, collaborative development.



## 📁 Project Structure

```
md-to-yaml-cli/
├── README.md
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
│   ├── main.py
│   ├── cli.py
│   ├── parser/
│   │   ├── markdown_parser.py
│   │   └── tests/
│   │       └── test_markdown_parser.py
│   ├── models/
│   │   ├── article.py
│   │   ├── unit.py
│   │   └── component.py
│   ├── exporter/
│   │   ├── yaml_exporter.py
│   │   └── tests/
│   │       └── test_yaml_exporter.py
│   └── utils/
│       ├── validator.py
│       └── tests/
│           └── test_validator.py
└── tests/
    └── run_all_tests.py
```



## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/md-to-yaml-cli.git
cd md-to-yaml-cli
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Usage

Convert Markdown to YAML:

```bash
python src/main.py --input path/to/markdown.md
```

Convert and validate:

```bash
python src/main.py --input path/to/markdown.md --validate
```

Specify an output file:

```bash
python src/main.py --input path/to/markdown.md --output output.yml
```



## 🛠 Iterative Development Workflow

Follow these steps for iterative, modular development:

1. Implement or refine module logic (e.g., parser, exporter).
2. Write or update corresponding tests in the `tests` directory.
3. Run unit tests for the module:

```bash
python src/parser/tests/test_markdown_parser.py
python src/utils/tests/test_validator.py
python src/exporter/tests/test_yaml_exporter.py
```

4. Run all tests:

```bash
python tests/run_all_tests.py
```

5. Verify CLI functionality and output correctness.



## 📚 Schemas and Configurations

- **Schemas (`schemas/`)**: JSON Schema files validate YAML structure.
- **Config (`config/`)**: JSON files (`compMapping.json`, `unitMapping.json`) define structured mappings and component schemas.

Update these files to reflect project changes or new content types.



## 📖 Templates

Templates (`templates/`) facilitate quick and consistent content creation:

- `article_template.yml` – YAML article structure.
- `jsonld_template.json` – JSON-LD representation of the article.



## 🧪 Testing

Run all tests:

```bash
python tests/run_all_tests.py
```

Ensure all modules and integrations function correctly through comprehensive testing.



## 🔄 Future Improvements

- Enhanced Markdown parsing using AST-based libraries (`markdown-it-py`).
- Additional exporters for JSON-LD and HTML.
- Improved error handling and CLI feedback.



## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the project.
2. Create your feature branch (`git checkout -b feature/new-feature`).
3. Commit changes (`git commit -m 'Add new feature'`).
4. Push to the branch (`git push origin feature/new-feature`).
5. Open a pull request.



## 📜 License

Distributed under the MIT License.



## 🧑‍💻 Author

[Matt Briggs](https://github.com/mattbriggs)