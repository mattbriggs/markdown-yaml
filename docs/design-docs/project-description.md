# **Markdown-to-YAML Structured Converter**

You can find the current coversion CLI at:
[Markdown-to-YAML CLI Converter](md-to-yaml-cli/README.md)

## **Updated Project Overview**

This project converts Markdown documents into structured YAML files that model content as semantically meaningful components and units. The core design decomposes Markdown into **subcomponents**, assembles those into **units**, and aggregates units into an **article** structure suitable for downstream rendering, indexing, and validation (e.g., HTML, JSON-LD, or AI-ready semantic chunks).

The final output supports use cases such as documentation systems, static site generators, and AI retrieval systems.



## **Processing Pipeline (Updated Logic)**

```
Markdown → Subcomponents → Components → Units → Article (YAML)
```

### 1. **Markdown Input**
- May include front matter (`YAML` metadata block).
- May reference external content via `[!INCLUDE](...)`.

### 2. **Subcomponent Extraction**
- The Markdown is parsed line by line into **subcomponents** using regex patterns.
  - Examples: list items, table rows, paragraph lines.
- Subcomponents are raw, minimally interpreted chunks.

### 3. **Component Assembly**
- Subcomponents are grouped into logical **components**.
  - E.g., a set of list items → a `compListUnordered`.
  - A table’s rows → a `compTable`.
- Each component includes:
  - Type (e.g., `compParagraph`, `compTable`, `compListOrdered`)
  - Content (nested structure, such as children in a list)

### 4. **Unit Segmentation**
- Components are grouped into **units**, often corresponding to document **sections**.
- Units are delineated by heading levels (e.g., `#`, `##`, `###`).
- Each unit includes:
  - Title (from heading)
  - Summary (first line after heading)
  - Type (inferred from present components using a `unitMapping.json`)
  - Components (parsed and structured)

### 5. **Article Composition**
- Units are wrapped into a complete **article** object.
- The article includes:
  - Metadata (from front matter or other heuristics)
  - Units (array of structured, typed content)
- Output can be rendered or exported as:
  - YAML (default)
  - JSON-LD (for semantic web)
  - HTML (for display)



## **Heading Structure and Section Nesting**

Your notes indicate a desire to eventually support hierarchical section nesting based on heading levels. For now, flat units are created by splitting on `#` and `##`, but future improvements may include:

```markdown
# H1 → top-level section
## H2 → subsection
### H3 → sub-subsection
```

For example:

```
H1        → Section
  H2      → Subsection
    H3    → Nested subsection
  H2      → Another Subsection
    H3    → Another nested subsection
```

This allows for more accurate content structuring and rendering fidelity.



## **Design Considerations**

### ✅ Current Strengths
- Clear and deterministic transformation pipeline.
- Human-readable YAML output with long text formatting.
- Modular component typing with external mappings.
- Recursive content inclusion via `[!INCLUDE]`.

### ⚠️ Known Limitations / Areas for Improvement
- Flat unit structure: nested sections are not yet modeled.
- Schema validation is not enforced (though schema headers are present).
- The `compMapping.json` file is unused (could support stricter validation).
- No robust error handling or CLI.
- Assumes YAML front matter is only at the top level (not nested).



## **Potential Improvements**
| Area | Suggested Enhancement |
|||
| **Validation** | Integrate JSON Schema checks on YAML output |
| **Nesting** | Support recursive H1–H3 nesting to match document hierarchy |
| **Parsing** | Switch from regex to Markdown AST (e.g., `markdown-it-py`) |
| **Schema Use** | Utilize `compMapping.json` to validate components and enrich types |
| **Modularity** | Break parser into testable modules |
| **CLI** | Use `argparse` to support input/output customization |
| **Output Formats** | Add `--jsonld`, `--html`, or `--chunks` options |



## **Visual Model Summary (from your diagram)**

```
[Markdown] 
   ↓
[Subcomponent extraction via regex] 
   ↓
[Component assembly from subcomponents] 
   ↓
[Units built from components, using H1/H2/H3 splits]
   ↓
[Article: includes metadata + units]
   ↓
[YAML → JSON-LD, HTML, AI chunks]
```
