import re
from typing import Dict, List, Optional

from packaging import version

__all__ = [
    "RequirementsParser",
]


class RequirementsParser:
    def __init__(self, file_path):
        self.file_path = file_path
        self.requirements: List[Dict[str, str]] = []

    def parse_requirements(self) -> List[Dict[str, str]]:
        """Parse the requirements file and extract package information."""
        with open(self.file_path, "r") as file:
            for line in file:
                requirement = self._parse_line(line)
                if requirement:
                    self.requirements.append(requirement)

    def _parse_line(self, line: str) -> Optional[Dict[str, str]]:
        """Parse a single line from the requirements file."""
        line = line.strip()
        if not line or line.startswith("#"):
            return None

        # inline comments
        line = line.split("#")[0].strip()

        # package name and version
        match = re.match(r"^([^=<>]+)([=<>]+.+)?$", line)
        if match:
            package = match.group(1).strip()
            version_spec = match.group(2).strip() if match.group(2) else ""
            return {"package": package, "version_spec": version_spec}

        return None

    def get_package_version(self, package_name: str) -> Optional[str]:
        """Get the version of a specific package."""
        for req in self.requirements:
            if req["package"].lower() == package_name.lower():
                return self._extract_version(req["version_spec"])
        return None

    def _extract_version(self, version_spec: str) -> Optional[str]:
        """Extract the version from a version specifier."""
        if not version_spec:
            return None

        match = re.search(r"([\d.]+)", version_spec)
        if not match:
            return None

        return str(version.parse(match.group(1)))

    def compare_requirements(self, other_parser: "RequirementsParser"):
        """Compare requirements with another RequirementsParser instance."""
        comparison = {}
        all_packages = set(
            [req["package"] for req in self.requirements + other_parser.requirements]
        )

        for package in all_packages:
            this_version = self.get_package_version(package)
            other_version = other_parser.get_package_version(package)
            comparison[package] = {"from": this_version, "to": other_version}

        return comparison

    @staticmethod
    def parse_and_compare_requirements(*, from_file, to_file):
        """Parse and compare two requirements files."""
        from_parser = RequirementsParser(from_file)
        to_parser = RequirementsParser(to_file)

        from_parser.parse_requirements()
        to_parser.parse_requirements()

        return from_parser.compare_requirements(to_parser)
