import unittest
from src.utils.validator import Validator
from src.models.article import Article

class TestValidator(unittest.TestCase):
    def setUp(self):
        self.validator = Validator()

        self.valid_article = Article(
            metadata={
                "title": "Valid Article",
                "author": {"name": "Author", "url": "https://author.com"},
                "datePublished": "2025-01-01T10:00:00Z",
                "description": "Valid description."
            },
            units=[
                {
                    "title": "Valid Unit",
                    "summary": "A valid summary.",
                    "type": "conceptUnit",
                    "components": [
                        {"compParagraph": {"content": "A paragraph component."}}
                    ]
                }
            ]
        )

    def test_valid_article(self):
        try:
            self.validator.validate_article(self.valid_article)
        except Exception as e:
            self.fail(f"Validation raised an unexpected exception: {e}")

    def test_invalid_article_missing_metadata(self):
        invalid_article = Article(metadata={}, units=[])
        with self.assertRaises(Exception):
            self.validator.validate_article(invalid_article)

    def test_invalid_component(self):
        invalid_article = Article(
            metadata=self.valid_article.metadata,
            units=[
                {
                    "title": "Invalid Unit",
                    "summary": "",
                    "type": "conceptUnit",
                    "components": [
                        {"compUnknown": {"content": "Unknown component."}}
                    ]
                }
            ]
        )
        with self.assertRaises(Exception):
            self.validator.validate_article(invalid_article)

if __name__ == "__main__":
    unittest.main()