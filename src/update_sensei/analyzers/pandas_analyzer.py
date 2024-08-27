import re
from typing import Any, Dict, List

from update_sensei.analyzers.base_analyzer import BaseAnalyzer


class PandasAnalyzer(BaseAnalyzer):
    def __init__(self, from_version: str, to_version: str) -> None:
        super().__init__("pandas", from_version, to_version)
        self.deprecation_data = self._load_deprecation_data()

    def analyze_imports(self, imports: List[Dict[str, str]]) -> None:
        for imp in imports:
            if imp["type"] == "import" and imp["name"] == "pandas":
                self.add_deprecation("pandas.*", 0, 0)
            elif imp["type"] == "from" and imp["module"] == "pandas":
                self.add_deprecation(f'pandas.{imp["name"]}', 0, 0)

    def analyze_function_calls(self, function_calls: List[Dict[str, Any]]) -> None:
        for call in function_calls:
            if call["name"].startswith("pd.") or call["name"].startswith("pandas."):
                self.add_deprecation(call["name"], call["line"], call["col"])
            elif "." in call["name"]:
                obj, method = call["name"].rsplit(".", 1)
                if method in ["append", "ix"]:
                    self.add_deprecation(
                        f"pandas.DataFrame.{method}", call["line"], call["col"]
                    )
                    self.add_deprecation(
                        f"pandas.Series.{method}", call["line"], call["col"]
                    )

    def get_deprecation_info(self, item: str) -> Dict[str, Any]:
        item = re.sub(r"^pd\.", "pandas.", item)
        return self.deprecation_data.get(item, {})
