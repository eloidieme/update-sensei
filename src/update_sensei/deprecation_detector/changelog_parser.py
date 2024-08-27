from typing import List

from packaging import version


class ChangelogParser:
    def __init__(self):
        self.changelog_template_urls = {
            "numpy": (
                "https://github.com/numpy/numpy/"
                "blob/main/doc/changelog/{}-changelog.rst"
            ),
            "pandas": (
                "https://github.com/pandas-dev/pandas/"
                "blob/main/doc/source/whatsnew/v{}.rst"
            ),
        }

    def get_changelog_url(self, *, library: str, version: str) -> str:
        template = self.changelog_template_urls.get(library.lower())
        if not template:
            return f"https://github.com/search?q={library}+{version}+changelog"

        return template.format(version)

    def get_changelog_links(
        self,
        *,
        library: str,
        from_version: str,
        to_version: str,
        deprecated_in: str,
        removed_in: str,
    ) -> List[str]:
        versions = sorted(
            set([from_version, deprecated_in, removed_in, to_version]),
            key=lambda v: version.parse(v),
        )

        return [self.get_changelog_url(library=library, version=v) for v in versions]
