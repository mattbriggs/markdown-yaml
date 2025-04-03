# How to add a new unit

Here's a clear, structured approach to adding a **new unit type** to your system, aligned with your current architecture:

## ✅ **Step-by-Step Guide to Adding New Units**

A "unit" in your system is a meaningful grouping of components (paragraphs, lists, tables, etc.). Each unit has a type (`conceptUnit`, `taskUnit`, etc.) defined by the components it must contain.

### 📌 **1. Update `unitMapping.json`**

**Location:**  
```
config/unitMapping.json
```

Add your new unit definition by specifying:

- **Unit Type**: A unique identifier.
- **Required Components**: Components that must be present to recognize the unit.

**Example:**

```json
{
  "myNewUnit": {
    "required_components": [
      "compNewType",
      "compParagraph"
    ]
  }
}
```

### 📌 **2. Update Article Schema (Optional but Recommended)**

Your main article schema (`article.schema.json`) might list permissible unit types explicitly. Ensure your new unit is recognized:

**Example update (`article.schema.json`):**

```json
"units": {
  "type": "array",
  "items": {
    "type": "object",
    "properties": {
      "title": { "type": "string" },
      "summary": { "type": "string" },
      "type": { 
        "type": "string",
        "enum": ["conceptUnit", "taskUnit", "myNewUnit"]  // add new unit here
      },
      "components": {
        "type": "array"
      }
    },
    "required": ["title", "type", "components"]
  }
}
```

### 📌 **3. Adjust Your Markdown Parser Logic**

**Location:**
```
src/parser/markdown_parser.py
```

Units are identified by detecting specific components. Update the `identify_unit_type` method to recognize your new unit:

**Example (`identify_unit_type` method):**

```python
def identify_unit_type(self, components: List[Component]) -> str:
    component_types = {c.component_type for c in components}
    for unit_type, definition in self.unit_mapping.items():
        required_comps = set(definition["required_components"])
        if required_comps.issubset(component_types):
            return unit_type
    return 'unknown'
```

No additional code needed if this generalized logic is already implemented.

### 📌 **4. Verify the Unit Model**

Your current unit model (`models/unit.py`) should already support new unit types as it’s generic:

```python
class Unit:
    def __init__(self, title: str, summary: str, unit_type: str, components: list):
        self.title = title
        self.summary = summary
        self.type = unit_type
        self.components = components

    def to_dict(self):
        return {
            "title": self.title,
            "summary": self.summary,
            "type": self.type,
            "components": [c.to_dict() for c in self.components]
        }
```

No additional changes needed.

### 📌 **5. Update Tests (Recommended)**

Explicitly test your new unit in your validator and parser tests.

**Example (`test_validator.py`):**

```python
def test_valid_article_with_new_unit(self):
    valid_article = Article(
        metadata={"title": "New Unit Example"},
        units=[
            {
                "title": "My New Unit",
                "summary": "Testing new unit type",
                "type": "myNewUnit",
                "components": [
                    {"compNewType": {"content": "Content"}},
                    {"compParagraph": {"content": "Paragraph content"}}
                ]
            }
        ]
    )
    self.validator.validate_article(valid_article)
```

**Example (`test_markdown_parser.py`):**

Create a Markdown file with the new unit pattern:

```markdown
# My New Unit
Summary text for new unit.

:::newtype
Content for the new type.

Paragraph content here.
```

Update your parser test accordingly to verify correct parsing.

### 📌 **6. Run Tests**

Verify correctness and integration by running your tests:

```bash
pytest
```

## 🚀 **Workflow Summary:**

- Define your new unit clearly in `unitMapping.json`.
- Adjust schemas and parser logic if needed.
- Explicitly add unit tests to ensure new unit works correctly.

## ✅ **Maintainability Recommendations:**

- Clearly document each new unit in your project docs.
- Consistently follow naming conventions for new units and components.

Following these steps ensures you can confidently and quickly add new units as your documentation evolves.