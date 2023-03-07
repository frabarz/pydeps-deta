import asyncio
from typing import Dict, List, Optional

from cmp_version import VersionString as Version

from .models import Release
from .remote import Repository


async def get_single(
  name: str,
  *,
  min_version: Optional[str] = None,
  max_version: Optional[str] = None,
):
    """Retrieves extended information about a range of releases of a package."""
    minv = None if min_version is None else Version(min_version)
    maxv = None if max_version is None else Version(max_version)

    def in_range(vers: Version):
        return (maxv is None or vers <= maxv) and (minv is None or vers >= minv)

    async with Repository() as remote:
        versions = await remote.fetch_release_list(name)
        releases: List[Release] = await asyncio.gather(*(
            remote.get_release(name, version)
            for version in versions
            if in_range(version)
        ))

    return releases


async def get_multiple(packages: Dict[str, List[str]]):
    async with Repository() as remote:
        releases: List[Release] = await asyncio.gather(*(
            remote.get_release(name, Version(version))
            for name, versions in packages.items()
            for version in versions
        ))

    return releases
