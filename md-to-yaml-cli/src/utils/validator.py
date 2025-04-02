import jsonschema
import json
import os
import logging

logging.basicConfig(level=logging.INFO)


class Validator:
    def __init__(self, schema_dir="schemas", config_dir="config"):
        self.schema_dir = schema_dir
        self.config_dir = config_dir

        # Load main schemas
        self.article_schema = self._load_schema("article.schema.json")
        self.metadata_schema = self._load_schema("metadata.schema.json")

        # Load mappings for components and units
        self.comp_mapping = self._load_config("compMapping.json")
        self.unit_mapping = self._load_config("unitMapping.json")

    def _load_schema(self, schema_filename):
        schema_path = os.path.join(self.schema_dir, schema_filename)
        with open(schema_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _load_config(self, config_filename):
        config_path = os.path.join(self.config_dir, config_filename)
        with open(config_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def validate_article(self, article):
        article_dict = article.to_dict()
        
        # Validate entire article structure
        jsonschema.validate(instance=article_dict, schema=self.article_schema)
        logging.info("✅ Article structure validated successfully.")

        # Validate metadata separately
        self.validate_metadata(article.metadata)

        # Validate units individually
        for unit in article.units:
            self.validate_unit(unit)

    def validate_metadata(self, metadata):
        jsonschema.validate(instance=metadata, schema=self.metadata_schema)
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
        jsonschema.validate(instance=comp_content, schema=comp_schema)

        logging.info(f"✅ Component '{comp_type}' validated successfully.")