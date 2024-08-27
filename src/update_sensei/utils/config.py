from typing import Dict


class Config:
    # Supported libraries and their default versions
    SUPPORTED_LIBRARIES: Dict[str, str] = {"numpy": "1.20.0", "pandas": "1.3.0"}

    # Default Python versions
    DEFAULT_FROM_PYTHON_VERSION: str = "3.10"
    DEFAULT_TO_PYTHON_VERSION: str = "3.11"

    # Logging settings
    LOG_LEVEL: str = "INFO"

    @classmethod
    def get_library_versions(cls) -> Dict[str, str]:
        return cls.SUPPORTED_LIBRARIES.copy()

    @classmethod
    def is_library_supported(cls, library: str) -> bool:
        return library.lower() in [lib.lower() for lib in cls.SUPPORTED_LIBRARIES]
