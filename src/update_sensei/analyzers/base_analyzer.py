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

    @abstractmethod
    def analyze_imports(self, imports) -> None:
        """
        Analyze import statements for potential deprecations.

        :param imports: List of dictionaries containing import information
        """
        pass

    @abstractmethod
    def analyze_function_calls(self, function_calls) -> None:
        """
        Analyze function calls for potential deprecations.

        :param function_calls: List of dictionaries containing function call information
        """
        pass

    def get_deprecation_info(self, item: str):
        """
        Retrieve deprecation information for a specific item.

        :param item: The name of the deprecated item (function, class, etc.)
        :return: Dictionary containing deprecation details
        """
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
