from typing import Dict, Any


class Component:
    """
    Represents a single structured content component extracted from Markdown.
    """

    def __init__(self, component_type: str, content: Dict[str, Any]):
        """
        Initializes a Component instance.

        Args:
            component_type (str): Type identifier of the component (e.g., compParagraph, compTable).
            content (Dict[str, Any]): Structured content of the component adhering to compMapping schema.
        """
        self.component_type = component_type
        self.content = content

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the Component object into a dictionary suitable for serialization.

        Returns:
            Dict[str, Any]: Dictionary representation of the component.
        """
        return {self.component_type: self.content}

    def validate(self, validator) -> bool:
        """
        Validates the component using a provided validator instance.

        Args:
            validator: An instance of a Validator class that checks conformity to the component schema.

        Returns:
            bool: True if validation passes, raises an exception otherwise.
        """
        validator.validate_component(self)
        return True