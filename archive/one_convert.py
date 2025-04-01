import markdown
import yaml
from bs4 import BeautifulSoup

# Sample Markdown
md_content = """
# Sample Page

## Main Heading

This is some content.

- Item 1
- Item 2
"""

# Convert Markdown to HTML
html = markdown.markdown(md_content)

# Parse HTML with BeautifulSoup
soup = BeautifulSoup(html, "html.parser")

# Extract elements
title = soup.find("h1").text if soup.find("h1") else None
headings = [h.text for h in soup.find_all("h2")]
paragraphs = [p.text for p in soup.find_all("p")]
items = [li.text for li in soup.find_all("li")]

# Convert to structured YAML
output = {
    "document": {
        "title": title,
        "sections": [
            {
                "heading": headings[0] if headings else None,
                "paragraphs": paragraphs,
                "items": items
            }
        ]
    }
}

# Print YAML output
yaml_output = yaml.dump(output, default_flow_style=False)
print(yaml_output)
