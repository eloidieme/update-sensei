from typing import Dict, List


class Config:
    # Supported libraries and their default versions
    SUPPORTED_LIBRARIES: Dict[str, str] = {"numpy": "1.20.0", "pandas": "1.3.0"}

    # Default Python versions
    DEFAULT_FROM_PYTHON_VERSION: str = "3.10"
    DEFAULT_TO_PYTHON_VERSION: str = "3.11"

    # File extensions to analyze
    PYTHON_FILE_EXTENSIONS: List[str] = [".py", ".pyw"]

    # Maximum number of files to analyze in a single run
    MAX_FILES_TO_ANALYZE: int = 1000

    # Changelog URLs for supported libraries
    CHANGELOG_URLS: Dict[str, str] = {
        "numpy": "https://github.com/numpy/numpy/blob/main/doc/release/",
        "pandas": "https://github.com/pandas-dev/pandas/blob/main/CHANGELOG.md",
    }

    # Logging settings
    LOG_LEVEL: str = "INFO"

    # Output settings
    DEFAULT_OUTPUT_FORMAT: str = "markdown"
    SUPPORTED_OUTPUT_FORMATS: List[str] = ["markdown", "json", "html"]

    # Performance settings
    USE_MULTIPROCESSING: bool = True
    MAX_WORKERS: int = 4

    # Deprecation severity levels
    SEVERITY_LEVELS: Dict[str, int] = {"LOW": 1, "MEDIUM": 2, "HIGH": 3, "CRITICAL": 4}

    # Minimum severity level to report
    MIN_SEVERITY_TO_REPORT: int = SEVERITY_LEVELS["MEDIUM"]

    @classmethod
    def get_library_versions(cls) -> Dict[str, str]:
        return cls.SUPPORTED_LIBRARIES.copy()

    @classmethod
    def is_library_supported(cls, library: str) -> bool:
        return library.lower() in [lib.lower() for lib in cls.SUPPORTED_LIBRARIES]

    @classmethod
    def get_changelog_url(cls, library: str) -> str:
        return cls.CHANGELOG_URLS.get(library.lower(), "")

    @classmethod
    def get_severity_level(cls, severity: str) -> int:
        return cls.SEVERITY_LEVELS.get(severity.upper(), 0)

    @classmethod
    def should_report_severity(cls, severity: int) -> bool:
        return severity >= cls.MIN_SEVERITY_TO_REPORT
