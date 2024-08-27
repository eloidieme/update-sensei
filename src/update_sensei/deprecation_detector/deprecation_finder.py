from typing import Any, Dict, List

from update_sensei.analyzers.base_analyzer import AnalyzerFactory
from update_sensei.deprecation_detector.changelog_parser import ChangelogParser


class DeprecationFinder:
    def __init__(self, from_versions: Dict[str, str], to_versions: Dict[str, str]):
        self.from_versions = from_versions
        self.to_versions = to_versions
        self.analyzers = self._initialize_analyzers()
        self.changelog_parser = ChangelogParser()

    def _initialize_analyzers(self):
        """Initialize analyzers for each library."""
        return {
            library: AnalyzerFactory.get_analyzer(
                library, self.from_versions[library], self.to_versions[library]
            )
            for library in self.from_versions.keys()
        }

    def find_deprecations(self, parsed_data):
        """
        Find deprecations in the parsed data.
        """
        all_deprecations = []

        for file_data in parsed_data:
            file_deprecations = self._analyze_file(file_data)
            all_deprecations.extend(file_deprecations)

        return all_deprecations

    def _analyze_file(self, file_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Analyze a single file for deprecations.
        """
        file_deprecations = []

        for library, analyzer in self.analyzers.items():
            deprecations = analyzer.analyze(file_data)
            for dep in deprecations:
                changelog_links = self._get_changelog_links(library, dep)
                dep["changelog_links"] = changelog_links
                dep["file_path"] = file_data["file_path"]
                file_deprecations.append(dep)

        return file_deprecations

    def _get_changelog_links(
        self, library: str, deprecation: Dict[str, Any]
    ) -> List[str]:
        """
        Get changelog links for a deprecated item.
        """
        from_version = self.from_versions[library]
        to_version = self.to_versions[library]
        deprecated_in = deprecation["deprecation_info"]["deprecated_in"]
        removed_in = deprecation["deprecation_info"].get("removed_in", to_version)

        return self.changelog_parser.get_changelog_links(
            library=library,
            from_version=from_version,
            to_version=to_version,
            deprecated_in=deprecated_in,
            removed_in=removed_in,
        )
