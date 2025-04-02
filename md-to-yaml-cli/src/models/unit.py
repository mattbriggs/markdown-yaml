from typing import List, Dict, Any
from .component import Component


class Unit:
    """
    Represents a structured content unit derived from a Markdown section.
    """

    def __init__(self, title: str, summary: str, unit_type: str, components: List[Component]):
        """
        Initializes a Unit instance.

        Args:
            title (str): Title of the unit, typically from Markdown heading.
            summary (str): Brief summary or description of the unit content.
            unit_type (str): Semantic type inferred from component presence (from unitMapping.json).
            components (List[Component]): List of structured components.
        """
        self.title = title
        self.summary = summary
        self.unit_type = unit_type
        self.components = components

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the Unit object into a dictionary suitable for serialization.

        Returns:
            Dict[str, Any]: Dictionary representation of the unit.
        """
        return {
            "title": self.title,
            "summary": self.summary,
            "type": self.unit_type,
            "components": [component.to_dict() for component in self.components]
        }

    def add_component(self, component: Component) -> None:
        """
        Adds a component to the unit.

        Args:
            component (Component): A structured component instance.
        """
        self.components.append(component)

    def validate(self, validator) -> bool:
        """
        Validates the unit structure and components using a provided validator.

        Args:
            validator: An instance of a Validator class that checks conformity to schemas.

        Returns:
            bool: True if validation passes, raises an exception otherwise.
        """
        validator.validate_unit(self)
        for component in self.components:
            component.validate(validator)
        return True