## How to add a new component

Adding new components to your system involves a clear, systematic process. Below is a detailed, step-by-step guide:

## 📌 Overview of Steps to Add New Components:

1. **Define the component schema** in your `compMapping.json` file.
2. **Update the parsing logic** in your `markdown_parser.py` to recognize and extract the new component.
3. **Add serialization logic** in your models (if needed, e.g., `component.py`).
4. **Add rendering support** in your exporters (YAML, JSON-LD, HTML).
5. **Update the validator** to recognize and validate the new component.
6. **Write tests** for your new component logic.

## ✅ Step-by-Step Guide:

### 🚧 **Step 1: Define Your Component Schema**

**File to update:**  
`config/compMapping.json`

### **Example:** Suppose you want to add a new component type called **`compCodeBlock`**.

Update your `compMapping.json` like so:

```json
{
  "compParagraph": {
    "schema": {
      "type": "object",
      "properties": {
        "content": { "type": "string" }
      },
      "required": ["content"]
    }
  },
  "compCodeBlock": {
    "schema": {
      "type": "object",
      "properties": {
        "language": { "type": "string" },
        "code": { "type": "string" }
      },
      "required": ["language", "code"]
    }
  }
}
```



### 🚧 **Step 2: Update Markdown Parser**

Update your component extraction logic in:  
`src/parser/markdown_parser.py`

For example, you might add a new regex pattern to detect code blocks:

```python
def extract_components(self, content: str) -> List[Component]:
    lines = content.split('\n')
    components = []
    buffer = []
    current_type = None

    for line in lines + ['']:
        if line.startswith('```'):
            if current_type != 'compCodeBlock':
                self.flush_buffer(buffer, current_type, components)
                buffer = [line]
                current_type = 'compCodeBlock'
            else:
                buffer.append(line)
                self.flush_buffer(buffer, current_type, components)
                buffer = []
                current_type = None
        # existing logic continues here...
        elif line.startswith('- ') or line.startswith('* '):
            # existing logic...
            pass
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
    if comp_type == 'compCodeBlock':
        lines = content_str.split('\n')
        language = lines[0].strip('`')
        code = '\n'.join(lines[1:-1])
        components.append(Component(comp_type, {"language": language, "code": code}))
    # existing flush logic continues...
```



### 🚧 **Step 3: Update the Component Model (If Needed)**

Check your model in:  
`src/models/component.py`

Typically, your existing model supports generic structures, but if special serialization is needed, extend here.

Example (optional customization):

```python
class Component:
    def __init__(self, component_type: str, content: dict):
        self.component_type = component_type
        self.content = content

    def to_dict(self):
        return {self.component_type: self.content}
```

Typically, this generic implementation suffices.



### 🚧 **Step 4: Update YAML Exporter**

Your YAML exporter (`src/exporter/yaml_exporter.py`) usually serializes the components generically:

```python
# Example; typically no special handling needed:
def export(self):
    yaml_content = yaml.dump(
        self.article.to_dict(),
        sort_keys=False,
        allow_unicode=True,
        default_flow_style=False,
        width=float("inf"),
    )
    with open(self.output, "w", encoding="utf-8") as file:
        file.write(f"# yaml-language-server: $schema={self.schema_path}\n")
        file.write(yaml_content)
```

Usually no changes required here.



### 🚧 **Step 5: Update the Validator**

The existing logic in your `validator.py` already supports dynamic validation from `compMapping.json`, ensuring your new component is validated automatically if added correctly in **Step 1**.

Existing logic example (already handles new components):

```python
def validate_component(self, component):
    comp_type, comp_content = next(iter(component.items()))

    if comp_type not in self.comp_mapping:
        raise jsonschema.ValidationError(f"❌ Unrecognized component type '{comp_type}'.")

    comp_schema = self.comp_mapping[comp_type]["schema"]
    validator = jsonschema.Draft7Validator(schema=comp_schema, registry=self.registry)
    validator.validate(comp_content)

    logging.info(f"✅ Component '{comp_type}' validated successfully.")
```

No additional code needed here if configured correctly in Step 1.



### 🚧 **Step 6: Write Tests**

Create new tests in your component tests (`test_markdown_parser.py`, `test_validator.py`) to ensure parsing, exporting, and validating work correctly:

Example in `test_validator.py`:

```python
def test_valid_code_block_component(self):
    valid_article = Article(
        metadata={
            "title": "Valid Article",
            "author": {"name": "Author", "url": "https://author.com"},
            "datePublished": "2025-01-01T10:00:00Z",
            "description": "Article with code block."
        },
        units=[
            {
                "title": "Unit with Code Block",
                "summary": "Summary here.",
                "type": "conceptUnit",
                "components": [
                    {"compCodeBlock": {
                        "language": "python",
                        "code": "print('Hello World!')"
                    }}
                ]
            }
        ]
    )

    try:
        self.validator.validate_article(valid_article)
    except Exception as e:
        self.fail(f"Validation raised an unexpected exception: {e}")
```



## ✅ **Summary of Changes:**

| Step | Task | File to Update |
|||-|
| 1 | Schema definition | `compMapping.json` |
| 2 | Markdown parsing | `markdown_parser.py` |
| 3 | Component model (if special) | `component.py` |
| 4 | YAML export (usually automatic) | `yaml_exporter.py` |
| 5 | Validation (usually automatic) | `validator.py` |
| 6 | Testing | test files |



## 🚩 **Final Recommendations:**

- **Test comprehensively** after each change.
- **Commit each step** separately to simplify debugging and reverting.
- Update the **templates** (`article_template.yml`) to reflect new components clearly for your authors.

Following this systematic and modular approach makes adding components predictable, straightforward, and error-resistant.