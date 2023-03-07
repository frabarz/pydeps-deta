# pydeps (alternative server)

A rewrite of the [pydeps](https://github.com/David-OConnor/pydeps) project, using [FastAPI](https://fastapi.tiangolo.com/), and intended for deployment on [Deta Space](https://deta.space).

This project enables a set of endpoints to get dependency information of python packages published on [pypi.org](https://pypi.org). Specifically, one of these endpoints is intended for use by the [pyflow](https://github.com/David-OConnor/pyflow) executable.

The deployed version of this repository is available at https://pydeps.frbrz.xyz/  
You can use its [OpenAPI documentation](https://pydeps.frbrz.xyz/openapi.json) to [explore the available endpoints](https://pydeps.frbrz.xyz/docs).

## Own instance on Deta

Although the app is available at Deta Discovery, it is not intended for the creation of multiple instances. The preferred way is using [the referenced live instance](https://pydeps.frbrz.xyz/query/) in pyflow, so more versions get cached and are readily available for other users.  
However dependencies are a delicate issue and you would do right in not trusting so easily third parties servers. You can still create your own instance, by [installing it on the Canvas](https://deta.space/discovery/r/rxyxftxvhwf4jhtk), or by cloning this repo and pushing a new private project. Or you could even just run it locally.

## Run locally

This project uses Deta Base to cache the results of each query for dependencies. To enable cache, you must provide the application with a Deta Project Key, and set it in the environment variable `DETA_PROJECT_KEY`.  
The app will still work without it, but your instance could be rate limited from the pypi API if there are too many requests in a short timespan. Note a request is made for each version, for each package.

You can run the application locally by executing inside the Python virtual environment:

```bash
(.venv) $ uvicorn main:app --port 8000
```

Then you can set the `http://localhost:8000/query/` URL on pyflow to use it instead of the official endpoint.
