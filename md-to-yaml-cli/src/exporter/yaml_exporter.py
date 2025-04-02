import yaml
import logging

logging.basicConfig(level=logging.INFO)


# Custom YAML presenter for better readability (multiline strings)
def str_presenter(dumper, data):
    if "\n" in data or len(data) > 80:
        return dumper.represent_scalar("tag:yaml.org,2002:str", data, style="|")
    return dumper.represent_scalar("tag:yaml.org,2002:str", data)


yaml.add_representer(str, str_presenter)


class YAMLExporter:
    def __init__(self, article, output="output.yml", schema_path="../schemas/article.schema.json"):
        self.article = article
        self.output = output
        self.schema_path = schema_path

    def export(self):
        yaml_content = yaml.dump(
            self.article.to_dict(),
            sort_keys=False,
            allow_unicode=True,
            default_flow_style=False,
            width=float("inf"),
        )

        with open(self.output, "w", encoding="utf-8") as file:
            file.write(f"# yaml-language-server: $schema={self.schema_path}\n")
            file.write(yaml_content)

        logging.info(f"YAML exported successfully to {self.output}")