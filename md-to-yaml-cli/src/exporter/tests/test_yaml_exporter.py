import unittest
import os
import yaml
from src.models.article import Article
from src.exporter.yaml_exporter import YAMLExporter

class TestYAMLExporter(unittest.TestCase):
    def setUp(self):
        self.article = Article(
            metadata={
                "title": "Export Test",
                "author": {"name": "Author", "url": "https://example.com"},
                "datePublished": "2025-01-01T10:00:00Z",
                "description": "Testing export functionality."
            },
            units=[
                {
                    "title": "Test Unit",
                    "summary": "Testing summary.",
                    "type": "conceptUnit",
                    "components": [
                        {"compParagraph": {"content": "This is a paragraph."}}
                    ]
                }
            ]
        )
        self.output_file = "test_output.yml"

    def tearDown(self):
        if os.path.exists(self.output_file):
            os.remove(self.output_file)

    def test_yaml_export(self):
        exporter = YAMLExporter(self.article, output=self.output_file)
        exporter.export()

        self.assertTrue(os.path.exists(self.output_file))

        with open(self.output_file, 'r') as f:
            content = yaml.safe_load(f)

        self.assertEqual(content['metadata']['title'], "Export Test")
        self.assertEqual(content['units'][0]['title'], "Test Unit")

if __name__ == "__main__":
    unittest.main()