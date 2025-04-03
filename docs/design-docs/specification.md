# **Markdown-to-YAML Structured Converter — Specification v2**

## **Project Summary**

This tool transforms a Markdown document into a structured, semantic YAML representation. It is designed to support content reuse, metadata extraction, validation, and machine-readability, enabling downstream applications such as:

- Static site generation
- AI knowledge ingestion
- JSON-LD for structured data
- HTML rendering
- Training and documentation systems

The tool supports recursive file inclusion, section detection via headings, component extraction (e.g., tables, lists, paragraphs), and type classification using configurable mappings.



## **Architecture Overview**

```text
Markdown File (.md)
     ↓
[Preprocessor]
     ↓
Includes Resolved + Metadata Extracted
     ↓
[Parser]
     ↓
Subcomponents → Components → Units (based on headings)
     ↓
[Composer]
     ↓
Article = { metadata + units }
     ↓
[Exporter]
     ↓
YAML, JSON-LD, HTML, AI-ready chunks
```



## **Feature Specification**

### 🧩 **1. Subcomponent Extraction**

- **Input**: Raw Markdown content
- **Output**: Stream of parsed subcomponents (individual lines classified by regex)
- **Details**:
  - Ordered/unordered list items
  - Table rows
  - Paragraph lines
  - Code blocks
  - Blockquotes (future)
- **Improvement**: Consider replacing regex-based extraction with an abstract syntax tree (AST) parser (e.g., `markdown-it-py` for Python or `mistune`).



### 🧱 **2. Component Assembly**

- **Purpose**: Groups subcomponents into semantic components:
  - `compListUnordered`
  - `compListOrdered`
  - `compTable`
  - `compParagraph`
  - (Planned: `compCodeBlock`, `compQuote`, `compImage`, etc.)
- **Structure**:
  ```yaml
  compListUnordered:
    items:
      - item: "First"
        children:
          - item: "Nested"
  ```
- **Improvement**:
  - Validate each component against `compMapping.json` to ensure well-formed structure
  - Fallback or log warning for unmapped component types



### 🧩 **3. Unit Formation**

- **Purpose**: Groups components into meaningful **units**, typically structured around headings (`#`, `##`, etc.)
- **Structure**:
  ```yaml
  title: "Section Title"
  summary: "First sentence"
  type: "conceptUnit"
  components: [...]
  ```
- **Improvements**:
  - Detect nesting hierarchy: convert heading levels into recursive unit nesting (e.g., `section → subsection → sub-subsection`)
  - Flatten option for consumers not supporting nesting
  - Refactor to allow configurable heading depth used for splitting



### 🧠 **4. Unit Typing**

- **Purpose**: Assigns a semantic `type` to each unit based on the components it contains
- **Logic**:
  - Uses `unitMapping.json` to determine which component combinations constitute known unit types
  - Fallbacks to `"unknown"` type if no match
- **Improvements**:
  - Add confidence scoring for heuristic matching
  - Log or output unresolved units for human review



### 📄 **5. Metadata Extraction**

- **Source**: Extracted from front matter block at the top of the Markdown file (`\nkey: value\n...`)
- **Improvement**:
  - Enforce front matter schema validation using `jsonschema`
  - Allow multiple metadata sources (file-level, section-level in future)
  - Merge metadata from included files optionally



### 🔁 **6. Include Resolution**

- **Syntax**: `[!INCLUDE](path.md)`
- **Behavior**:
  - Loads and flattens external Markdown content recursively
  - Removes their metadata blocks to avoid collisions
- **Improvement**:
  - Add max recursion depth and cycle detection
  - Support include context for relative metadata or unit inheritance



### 🧾 **7. Export Formats**

#### ✅ YAML (default)
- Semantic structure with nested objects
- Header includes `$schema` reference for tooling
- Multiline strings with pipe (`|`) formatting for readability

#### 🌐 JSON-LD
- Schema.org/Article or custom vocabularies
- Entity mapping: Article, Unit, Component → `@type`, `@id`, etc.
- Useful for SEO, knowledge graphs, and RAG indexing

#### 💡 HTML
- Render components into HTML for preview or publishing
- Style-friendly classes per component type
- Optionally embed schema metadata as JSON-LD

#### 🧠 AI-Ready Chunks
- Break YAML into retrieval-friendly segments:
  - Chunked by unit or subunit
  - Metadata on type, title, ID, component count
  - Exported as individual JSON files or streamed for ingestion



## **CLI & Configuration Enhancements**

### 📦 CLI Interface (planned)

Use `argparse` to support:

| Option | Description |
|--|-|
| `--input` | Path to the Markdown file |
| `--output` | Output file path or format base |
| `--format` | `yaml`, `jsonld`, `html`, `chunks` |
| `--schema` | Path to schema for validation |
| `--depth` | Heading depth for section splitting |
| `--include-root` | Whether to wrap with an article object |



### ⚙️ Configurable Mappings

- `compMapping.json`: Maps component types to their expected structures and validation rules
- `unitMapping.json`: Maps unit types to required component combinations

These mappings allow the logic to be updated without modifying code.



## **Validation Plan**

### ✅ YAML Schema Header
- Included in output for editor autocompletion and validation

### 🔍 JSON Schema
- Validate:
  - `metadata` block
  - Each unit and its `type`
  - Each component by type
- Fail-fast or warn-on-error depending on config



## **Testing Plan**

### 🧪 Fixtures
- Markdown files with expected YAML outputs
- Variants:
  - Lists (nested/flat)
  - Tables (simple/complex)
  - Sections (deeply nested)
  - Invalid structures

### 🧼 Lint & Style
- Enforce style with `black`, `ruff`, or `flake8`
- YAML formatting rules consistent with multiline style



## **Future Directions**

| Area | Direction |
||--|
| Markdown AST | Use a Markdown parser that emits a parse tree for high fidelity parsing |
| Language detection | Extract and classify language from metadata or headings |
| Web app | Upload Markdown and get structured previews instantly |
| Editor plugin | VSCode plugin to preview YAML structure live |
| CMS Integration | Connect with headless CMS (e.g., Sanity, Contentful) to roundtrip content |



## **Conclusion**

This enhanced specification defines a robust, extensible pipeline for converting Markdown into structured, typed, and machine-readable content. The tool supports multi-format output and can serve as a foundation for intelligent documentation, publishing workflows, and semantic content retrieval.