from pathlib import Path
from typing import Any, Dict

import yaml


class DeprecationDataLoader:
    def __init__(self, data_directory: str = "data"):
        self.data_directory = Path(data_directory)

    def load_library_data(self, library: str) -> Dict[str, Any]:
        yaml_path = self.data_directory / f"{library.lower()}.yaml"

        if not yaml_path.exists():
            raise FileNotFoundError(f"No deprecation data found for {library}")

        with open(yaml_path, "r") as file:
            raw_data = yaml.safe_load(file)

        deprecation_data = {}
        for version, deprecations in raw_data.items():
            for dep in deprecations:
                full_name = f"{dep['item']}"
                deprecation_data[full_name] = {
                    "deprecated_in": dep["deprecated_in"],
                    "removed_in": dep["removed_in"],
                    "description": dep["description"],
                }

        return deprecation_data
