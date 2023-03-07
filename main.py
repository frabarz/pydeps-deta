from typing import Dict, List, Optional, TypedDict

from fastapi import FastAPI

import pydeps
from pydeps import get_multiple, get_single


class QueryRequest(TypedDict):
    packages: Dict[str, List[str]]


class ReleaseWithoutName(TypedDict):
    version: str
    requires_dist: List[str]
    requires_python: Optional[str]


class ReleaseWithName(TypedDict):
    name: str
    version: str
    requires_dist: List[str]
    requires_python: Optional[str]


app = FastAPI(title=pydeps.__title__, version=pydeps.__version__)


@app.get("/")
def route_index():
    """
    Root endpoint for version discovery.
    """
    return {"title": pydeps.__title__, "version": pydeps.__version__}


@app.get("/{package}/",
         name="All versions of package",
         response_model=List[ReleaseWithoutName])
async def route_get_all(package: str):
    """
    Get dependency data for all versions of a package.
    """
    return await get_single(package)


@app.get("/{package}/{version}/",
         name="Single version of package",
         response_model=List[ReleaseWithoutName])
async def route_get_one(package: str, version: str):
    """
    Get dependency data for a specific version of a package.
    """
    return await get_single(package, min_version=version, max_version=version)


@app.get("/gte/{package}/{version}/",
         name="All versions of package greater than specified",
         response_model=List[ReleaseWithoutName])
async def route_get_gte(package: str, version: str):
    """
    Get dependency data for versions of a package greater than or equal to requested.
    """
    return await get_single(package, min_version=version)


@app.get("/lte/{package}/{version}/",
         name="All versions of package lower than specified",
         response_model=List[ReleaseWithoutName])
async def route_get_lte(package: str, version: str):
    """
    Get dependency data for versions of a package lower than or equal to requested.
    """
    return await get_single(package, max_version=version)


@app.get("/range/{package}/{min_version}/{max_version}/",
         name="All versions of package between range",
         response_model=List[ReleaseWithoutName])
async def route_get_range(package: str, min_version: str, max_version: str):
    """
    Get dependency data for versions of a package between a specified range.
    """
    return await get_single(package, min_version=min_version, max_version=max_version)


@app.post("/query/",
          name="Query many specific packages and versions",
          response_model=List[ReleaseWithName])
async def route_query(data: QueryRequest):
    """
    Get dependency data for multiple packages and versions.
    """
    return await get_multiple(data["packages"])
