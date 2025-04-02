import unittest
import os
from src.parser.markdown_parser import MarkdownParser

class TestMarkdownParser(unittest.TestCase):
    def setUp(self):
        self.test_markdown = """
---
title: Test Article
author:
  name: Test Author
  url: https://example.com
datePublished: 2025-01-01T10:00:00Z
description: Test description.
---

# Unit Title
Unit summary.

Paragraph content here.

- Item 1
- Item 2

## Subunit Title
Subunit summary.

| Header 1 | Header 2 |
|----------|----------|
| Cell 1   | Cell 2   |
"""
        self.test_file = "test_markdown.md"
        with open(self.test_file, "w") as f:
            f.write(self.test_markdown.strip())

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_parser_output(self):
        parser = MarkdownParser(self.test_file)
        result = parser.parse()

        self.assertIn('metadata', result)
        self.assertEqual(result['metadata']['title'], "Test Article")

        self.assertIn('units', result)
        self.assertEqual(len(result['units']), 2)

        unit1 = result['units'][0]
        self.assertEqual(unit1['title'], "Unit Title")
        self.assertEqual(unit1['summary'], "Unit summary.")
        self.assertEqual(unit1['type'], "conceptUnit")

        unit2 = result['units'][1]
        self.assertEqual(unit2['title'], "Subunit Title")
        self.assertEqual(unit2['type'], "referenceUnit")

if __name__ == "__main__":
    unittest.main()