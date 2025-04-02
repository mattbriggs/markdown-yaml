from typing import List, Dict, Any


class Article:
    """
    Represents a structured article composed of metadata and content units.
    """

    def __init__(self, metadata: Dict[str, Any], units: List[Dict[str, Any]]):
        """
        Initializes an Article instance.

        Args:
            metadata (Dict[str, Any]): Metadata dictionary conforming to metadata schema.
            units (List[Dict[str, Any]]): List of structured content units.
        """
        self.metadata = metadata
        self.units = units

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the Article object into a dictionary suitable for serialization.

        Returns:
            Dict[str, Any]: A dictionary representing the entire article.
        """
        return {
            "metadata": self.metadata,
            "units": self.units
        }

    def add_unit(self, unit: Dict[str, Any]) -> None:
        """
        Adds a content unit to the article.

        Args:
            unit (Dict[str, Any]): A content unit dictionary.
        """
        self.units.append(unit)

    def validate(self, validator) -> bool:
        """
        Validates the article structure using a provided validator.

        Args:
            validator: An instance of a Validator class that checks conformity to a schema.

        Returns:
            bool: True if the article passes validation, raises exception otherwise.
        """
        validator.validate_article(self)
        return True