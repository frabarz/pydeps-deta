from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from cmp_version import VersionString as Version
from deta import Deta


class FakeBase:
    def get(self, key: str):
        return None

    def put(self, item: Any, key: str):
        pass


try:
    deta = Deta()
    db = deta.Base("pydeps-repository")
except AssertionError:
    db = FakeBase()


@dataclass
class Package:
    author: str
    author_email: str
    bugtrack_url: Optional[str]
    classifiers: List[str]
    description: str
    description_content_type: str
    docs_url: Optional[str]
    download_url: str
    downloads: Dict[str, int]
    home_page: str
    keywords: str
    license: str
    maintainer: str
    maintainer_email: str
    name: str
    package_url: str
    platform: Optional[str]
    project_url: str
    project_urls: Dict[str, str]
    release_url: str
    requires_dist: List[str]
    requires_python: str
    summary: str
    version: str
    yanked: bool
    yanked_reason: Optional[str]

    @classmethod
    def from_pypi(cls, root: dict):
        return cls(**root["info"])


@dataclass(repr=False)
class Release:
    name: str
    version: str
    requires_dist: List[str] = field(default_factory=list)
    requires_python: Optional[str] = None

    @property
    def key(self):
        return f"{self.name}-{self.version}"

    def __repr__(self):
        return self.key

    def __str__(self):
        return f'{self.name}: "{self.version}"'

    @classmethod
    def get(cls, package: str, release: Version):
        data: Any = db.get(f"{package}-{release}")
        if data is None:
            raise KeyError("Combination of package and release not found in cache.")
        return cls(
            name=data["name"],
            version=data["version"],
            requires_python=data["requires_python"],
            requires_dist=data["requires_dist"],
        )

    @staticmethod
    def put(item: "Release"):
        db.put({
            "name": item.name,
            "version": item.version,
            "requires_python": item.requires_python,
            "requires_dist": item.requires_dist,
        }, item.key)
