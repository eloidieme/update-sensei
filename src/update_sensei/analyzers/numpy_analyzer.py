import re
from typing import Any, Dict, List

from update_sensei.analyzers.base_analyzer import BaseAnalyzer


class NumpyAnalyzer(BaseAnalyzer):
    def __init__(self, from_version: str, to_version: str):
        super().__init__("numpy", from_version, to_version)
        self.deprecation_data = self._load_deprecation_data()

    def analyze_imports(self, imports: List[Dict[str, str]]) -> None:
        for imp in imports:
            if imp["type"] == "import" and imp["name"] == "numpy":
                self.add_deprecation("numpy.*", 0, 0)
            elif imp["type"] == "from" and imp["module"] == "numpy":
                self.add_deprecation(f"numpy.{imp['name']}", 0, 0)

    def analyze_function_calls(self, function_calls: List[Dict[str, Any]]) -> None:
        for call in function_calls:
            if call["name"].startswith("np.") or call["name"].startswith("numpy."):
                self.add_deprecation(call["name"], call["line"], call["col"])

    def get_deprecation_info(self, item: str) -> Dict[str, Any]:
        item = re.sub(r"^np\.", "numpy.", item)
        return self.deprecation_data.get(item, {})
