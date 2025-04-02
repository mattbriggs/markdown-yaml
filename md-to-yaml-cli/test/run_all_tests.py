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