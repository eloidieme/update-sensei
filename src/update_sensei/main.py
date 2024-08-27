import argparse
import logging
import os
import textwrap
from collections import defaultdict
from datetime import datetime

from update_sensei.deprecation_detector.deprecation_finder import DeprecationFinder
from update_sensei.file_parser.python_file_parser import ProjectParser
from update_sensei.file_parser.requirements_parser import RequirementsParser
from update_sensei.utils.config import Config


def setup_logging():
    logging.basicConfig(
        level=getattr(logging, Config.LOG_LEVEL),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )


def parse_arguments():
    now = datetime.now()
    default_report_path = (
        f"reports/deprecation_report_{datetime.strftime(now, '%Y_%m_%d_%H_%M_%S')}.md"
    )
    parser = argparse.ArgumentParser(
        description="Deprecation Checker for Python projects"
    )
    parser.add_argument(
        "project_path", type=str, help="Path to the Python project to analyze"
    )
    parser.add_argument(
        "--from-requirements", type=str, help="Path to the 'from' requirements.txt file"
    )
    parser.add_argument(
        "--to-requirements", type=str, help="Path to the 'to' requirements.txt file"
    )
    parser.add_argument(
        "--from-python",
        type=str,
        default=Config.DEFAULT_FROM_PYTHON_VERSION,
        help="'From' Python version",
    )
    parser.add_argument(
        "--to-python",
        type=str,
        default=Config.DEFAULT_TO_PYTHON_VERSION,
        help="'To' Python version",
    )
    parser.add_argument(
        "--output",
        type=str,
        default=default_report_path,
        help="Output file for the deprecation report",
    )
    return parser.parse_args()


def get_library_versions(from_req: str, to_req: str):
    if from_req and to_req:
        comparison = RequirementsParser.parse_and_compare_requirements(
            from_file=from_req, to_file=to_req
        )
        return {
            lib: {"from": comp["from"], "to": comp["to"]}
            for lib, comp in comparison.items()
            if Config.is_library_supported(lib)
        }
    return {
        lib: {"from": ver, "to": ver}
        for lib, ver in Config.get_library_versions().items()
    }


def generate_report(
    *,
    all_deprecations,
    library_versions,
    from_python: str,
    to_python: str,
) -> str:
    """
    Generate a comprehensive deprecation report
    with changelog links for each deprecation.
    """
    # Mapping of common library abbreviations to full names
    library_mapping = {
        "np": "numpy",
        "pd": "pandas",
    }

    report = "# Deprecation Report\n\n"
    report += "## Version Information\n\n"
    report += f"Python version: {from_python} -> {to_python}\n\n"
    for lib, versions in library_versions.items():
        report += f"{lib} version: {versions['from']} -> {versions['to']}\n"
    report += "\n"

    total_deprecations = len(all_deprecations)
    files_affected = len(set(dep["file_path"] for dep in all_deprecations))
    report += "## Summary\n\n"
    report += f"Total deprecations found: {total_deprecations}\n"
    report += f"Files affected: {files_affected}\n\n"

    deprecations_by_file = defaultdict(list)
    for dep in all_deprecations:
        deprecations_by_file[dep["file_path"]].append(dep)

    report += "## Detailed Findings\n\n"
    for file_path, deprecations in deprecations_by_file.items():
        report += f"### {file_path}\n\n"
        for dep in deprecations:
            report += f"- **Line {dep['line']}**: `{dep['item']}` is deprecated\n"
            report += textwrap.indent(dep["deprecation_info"]["description"], "  ")
            report += "\n\n"

            library_abbr = dep["item"].split(".")[0]
            library = library_mapping.get(
                library_abbr, library_abbr
            )  # Map to full name if possible

            if library in library_versions:
                changelog_links = dep["changelog_links"]

                report += "  Relevant changelogs:\n"
                for link in changelog_links:
                    report += f"    - {link}\n"
            else:
                report += f"  No changelog information available for {library_abbr}\n"
            report += "\n"

    return report


def main():
    setup_logging()
    logger = logging.getLogger(__name__)

    args = parse_arguments()

    logger.info(f"Starting analysis of project: {args.project_path}")

    project_parser = ProjectParser(args.project_path)
    parsed_files = project_parser.parse_project()

    library_versions = get_library_versions(
        args.from_requirements, args.to_requirements
    )

    finder = DeprecationFinder(
        from_versions={
            lib: versions["from"] for lib, versions in library_versions.items()
        },
        to_versions={lib: versions["to"] for lib, versions in library_versions.items()},
    )

    all_deprecations = finder.find_deprecations(parsed_files)

    report = generate_report(
        all_deprecations=all_deprecations,
        library_versions=library_versions,
        from_python=args.from_python,
        to_python=args.to_python,
    )

    os.makedirs("reports", exist_ok=True)
    with open(args.output, "w") as f:
        f.write(report)

    logger.info(f"Deprecation report written to {args.output}")
    print(f"Deprecation analysis complete. Report written to {args.output}")


if __name__ == "__main__":
    main()
