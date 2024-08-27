from abc import ABC, abstractmethod
from typing import Any, Dict, List

from packaging import version

from update_sensei.data_management.deprecation_data_loader import DeprecationDataLoader


class BaseAnalyzer(ABC):
    def __init__(self, library: str, from_version: str, to_version: str) -> None:
        self.library = library
        self.from_version = from_version
        self.to_version = to_version
        self.deprecations: List[Dict[str, Any]] = []
        self.data_loader = DeprecationDataLoader()
        self.deprecation_data = self._load_deprecation_data()

    def _load_deprecation_data(self) -> Dict[str, Any]:
        return self.data_loader.load_library_data(self.library)

    def analyze_imports(self, imports: List[Dict[str, str]]) -> None:
        for imp in imports:
            if imp["type"] == "import" and imp["name"] == self.library:
                self.add_deprecation(f"{self.library}.*", 0, 0)
            elif imp["type"] == "from" and imp["module"] == self.library:
                self.add_deprecation(f'{self.library}.{imp["name"]}', 0, 0)

    def analyze_function_calls(self, function_calls: List[Dict[str, Any]]) -> None:
        for call in function_calls:
            if call["name"].startswith(f"{self.library}.") or call["name"].startswith(f"{self.library_alias}."):
                self.add_deprecation(call["name"], call["line"], call["col"])

    def analyze_constants(self, constants: List[Dict[str, Any]]) -> None:
        for constant in constants:
            self.add_deprecation(constant["name"], constant["line"], constant["col"])

    def analyze_type_annotations(self, type_annotations: List[Dict[str, Any]]) -> None:
        for annotation in type_annotations:
            self.add_deprecation(f"{annotation['name']}:{annotation['type']}", annotation["line"], annotation["col"])

    def analyze_arguments(self, arguments: List[Dict[str, Any]]) -> None:
        for arg in arguments:
            self.add_deprecation(f"{arg['name']}={arg['value']}", arg["line"], arg["col"])

    @abstractmethod
    def get_deprecation_info(self, item: str) -> Dict[str, Any]:
        pass

    def _is_deprecated(self, info: Dict[str, str]) -> bool:
        if not info:
            return False
        deprecated_in = version.parse(info["deprecated_in"])
        removed_in = version.parse(info["removed_in"])
        from_v = version.parse(self.from_version)
        to_v = version.parse(self.to_version)

        return (
            (deprecated_in <= from_v < removed_in)
            or (from_v < removed_in <= to_v)
            or (from_v < deprecated_in <= to_v)
        )

    def analyze(self, parsed_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Perform full analysis on the parsed data.

        :param parsed_data: Dictionary containing parsed file information
        :return: List of deprecation findings
        """
        self.deprecations = []
        self.analyze_imports(parsed_data["imports"])
        self.analyze_function_calls(parsed_data["function_calls"])
        self.analyze_constants(parsed_data["constants"])
        self.analyze_type_annotations(parsed_data["type_annotations"])
        self.analyze_arguments(parsed_data["arguments"])
        return self.deprecations

    def add_deprecation(self, item: str, line: int, col: int) -> None:
        """
        Add a deprecation finding to the list.

        :param item: The name of the deprecated item
        :param line: Line number where the deprecation was found
        :param col: Column number where the deprecation was found
        """
        deprecation_info = self.get_deprecation_info(item)
        if deprecation_info and self._is_deprecated(deprecation_info):
            self.deprecations.append(
                {
                    "item": item,
                    "line": line,
                    "col": col,
                    "deprecation_info": deprecation_info,
                }
            )


class AnalyzerFactory:
    @staticmethod
    def get_analyzer(library: str, from_version: str, to_version: str) -> BaseAnalyzer:
        """
        Factory method to get the appropriate analyzer based on the library.

        :param library: Name of the library (e.g. 'numpy', 'pandas')
        :param from_version: Starting version of the library
        :param to_version: Target version of the library
        :return: An instance of the appropriate analyzer
        """
        if library.lower() == "numpy":
            from .numpy_analyzer import NumpyAnalyzer

            return NumpyAnalyzer(from_version, to_version)
        elif library.lower() == "pandas":
            from .pandas_analyzer import PandasAnalyzer

            return PandasAnalyzer(from_version, to_version)
        else:
            raise ValueError(f"Unsupported library: {library}")
