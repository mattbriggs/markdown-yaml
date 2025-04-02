import jsonschema
import json
import os
import logging
import referencing
from jsonschema.validators import validator_for
from referencing import Registry, Resource

logging.basicConfig(level=logging.INFO)

class Validator:
    def __init__(self, schema_dir="schemas", config_dir="config"):
        self.schema_dir = schema_dir
        self.config_dir = config_dir

        # Load schemas explicitly
        self.article_schema = self._load_schema("article.schema.json")
        self.metadata_schema = self._load_schema("metadata.schema.json")

        # Load mappings for components and units
        self.comp_mapping = self._load_config("compMapping.json")
        self.unit_mapping = self._load_config("unitMapping.json")

        # Set up referencing registry with local schemas
        self.registry = self._setup_registry()

    def _load_schema(self, schema_filename):
        schema_path = os.path.join(self.schema_dir, schema_filename)
        with open(schema_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _load_config(self, config_filename):
        config_path = os.path.join(self.config_dir, config_filename)
        with open(config_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _setup_registry(self):
        registry = Registry()

        schemas = ["article.schema.json", "metadata.schema.json"]
        for schema_file in schemas:
            schema_path = os.path.join(self.schema_dir, schema_file)
            # Use the EXACT URI as it appears in $ref (e.g., "./metadata.schema.json")
            uri = f"./{schema_file}"
            with open(schema_path, "r", encoding="utf-8") as f:
                schema_content = json.load(f)
                resource = Resource.from_contents(schema_content)
                registry = registry.with_resource(uri=uri, resource=resource)
        return registry

    def validate_article(self, article):
        article_dict = article.to_dict()

        # Get appropriate validator class with referencing registry
        ValidatorClass = validator_for(self.article_schema)
        ValidatorClass.check_schema(self.article_schema)

        validator = ValidatorClass(
            schema=self.article_schema,
            registry=self.registry
        )

        validator.validate(article_dict)
        logging.info("✅ Article structure validated successfully.")

        # Validate metadata separately
        self.validate_metadata(article.metadata)

        # Validate units individually
        for unit in article.units:
            self.validate_unit(unit)

    def validate_metadata(self, metadata):
        validator = jsonschema.Draft7Validator(
            schema=self.metadata_schema,
            registry=self.registry
        )
        validator.validate(metadata)
        logging.info("✅ Metadata validated successfully.")

    def validate_unit(self, unit):
        required_fields = ["title", "summary", "type", "components"]
        for field in required_fields:
            if field not in unit:
                raise jsonschema.ValidationError(f"❌ Unit missing required field: {field}")

        unit_type = unit["type"]
        if unit_type not in self.unit_mapping:
            raise jsonschema.ValidationError(f"❌ Unrecognized unit type '{unit_type}'.")

        unit_def = self.unit_mapping[unit_type]

        required_comps = set(unit_def["required_components"])
        present_comps = set([list(comp.keys())[0] for comp in unit["components"]])

        if not required_comps.issubset(present_comps):
            missing = required_comps - present_comps
            raise jsonschema.ValidationError(f"❌ Unit '{unit['title']}' missing required components: {missing}")

        for comp in unit["components"]:
            self.validate_component(comp)

        logging.info(f"✅ Unit '{unit['title']}' validated successfully.")

    def validate_component(self, component):
        comp_type, comp_content = next(iter(component.items()))

        if comp_type not in self.comp_mapping:
            raise jsonschema.ValidationError(f"❌ Unrecognized component type '{comp_type}'.")

        comp_schema = self.comp_mapping[comp_type]["schema"]
        validator = jsonschema.Draft7Validator(
            schema=comp_schema,
            registry=self.registry
        )
        validator.validate(comp_content)

        logging.info(f"✅ Component '{comp_type}' validated successfully.")
