import ast
import os
from typing import Dict, List

__all__ = [
    "ProjectParser",
]


class PythonFileParser:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.tree = None
        self.imports = []
        self.function_calls = []

    def parse_file(self) -> None:
        """Parse the Python file and generate the AST."""
        with open(self.file_path, "r") as file:
            content = file.read()
        self.tree = ast.parse(content)

    def extract_imports(self) -> List[Dict[str, str]]:
        """Extract all import statements from the parsed file."""
        for node in ast.walk(self.tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    self.imports.append({"type": "import", "name": alias.name})
            elif isinstance(node, ast.ImportFrom):
                module = node.module
                for alias in node.names:
                    self.imports.append(
                        {"type": "from", "module": module, "name": alias.name}
                    )
        return self.imports

    def extract_function_calls(self):
        """Extract all function calls from the parsed file."""
        for node in ast.walk(self.tree):
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name):
                    self.function_calls.append(
                        {
                            "name": node.func.id,
                            "line": node.lineno,
                            "col": node.col_offset,
                        }
                    )
                elif isinstance(node.func, ast.Attribute):
                    self.function_calls.append(
                        {
                            "name": self._get_attribute_chain(node.func),
                            "line": node.lineno,
                            "col": node.col_offset,
                        }
                    )
        return self.function_calls

    def _get_attribute_chain(self, node: ast.Attribute) -> str:
        """Helper method to get the full attribute chain for a function call."""
        if isinstance(node.value, ast.Name):
            return f"{node.value.id}.{node.attr}"
        elif isinstance(node.value, ast.Attribute):
            return f"{self._get_attribute_chain(node.value)}.{node.attr}"
        return node.attr

    def analyze(self):
        """Perform full analysis of the file."""
        self.parse_file()
        return {
            "file_path": self.file_path,
            "imports": self.extract_imports(),
            "function_calls": self.extract_function_calls(),
        }


class ProjectParser:
    def __init__(self, project_path: str):
        self.project_path = project_path
        self.python_files = []

    def find_python_files(self) -> List[str]:
        """Find all Python files in the project directory."""
        for root, _, files in os.walk(self.project_path):
            for file in files:
                if file.endswith(".py"):
                    self.python_files.append(os.path.join(root, file))
        return self.python_files

    def parse_project(self):
        """Parse all Python files in the project."""
        self.find_python_files()
        parsed_files = []
        for file_path in self.python_files:
            parser = PythonFileParser(file_path)
            parsed_files.append(parser.analyze())
        return parsed_files
