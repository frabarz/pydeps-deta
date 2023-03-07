import asyncio
import logging
from typing import List

import httpx
from cmp_version import VersionString as Version

from .__version__ import __version__
from .models import Package, Release

logger = logging.getLogger(__name__)

KNOWN_NO_DEPS = {
    "cython",
    "numpy",
    "pyparsing",
}


class Repository:
    def __init__(
        self,
        *,
        semaphore: int = 4,
        remote_base: str = "https://pypi.org/",
    ) -> None:
        self.client = httpx.AsyncClient(
            base_url=remote_base,
            http2=True,
            headers={
                "User-Agent": f"python-pydeps/{__version__} httpx/{httpx.__version__}",
            }
        )
        self.semaphore = asyncio.Semaphore(semaphore)

    async def __aenter__(self):
        await self.client.__aenter__()
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        await self.client.__aexit__(exc_type, exc_value, traceback)

    async def get_release(self, package: str, version: Version):
        """
        Get a Release from app cache, or from remote repository in case of exception.
        """
        try:
            release = Release.get(package, version)

        except KeyError:
            release = await self.fetch_package_release(package, version)
            if not release.requires_dist and release.name not in KNOWN_NO_DEPS:
                logger.debug("Package without dependencies: %r", release)
                # TODO implement wheel analysis
            Release.put(release)

        return release

    async def fetch_release_list(self, package: str) -> List[Version]:
        """
        Retrieves a list of published release versions for a specified package.
        """
        async with self.semaphore:
            res = await self.client.get(f"/simple/{package}/", headers={
                "Accept": "application/vnd.pypi.simple.v1+json",
            })
        res.raise_for_status()
        root = res.json()

        return sorted(Version(v) for v in root["versions"])

    async def fetch_package(self, package: str):
        """
        Retrieves information about the latest release of a specified package.
        """
        async with self.semaphore:
            res = await self.client.get(f"/pypi/{package}/json")
        res.raise_for_status()
        root = res.json()

        return Package.from_pypi(root)

    async def fetch_package_release(self, package: str, release: Version):
        """
        Retrieves information about a specified release of a package.
        """
        async with self.semaphore:
            res = await self.client.get(f"/pypi/{package}/{release}/json")
        res.raise_for_status()
        root = res.json()

        info = root["info"]
        return Release(
            name=info["name"],
            version=info["version"],
            requires_dist=(
                [] if info["requires_dist"] is None else info["requires_dist"]
            ),
            requires_python=info["requires_python"],
        )

