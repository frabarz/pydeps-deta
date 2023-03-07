# pydeps (alternative server)

A rewrite of the [pydeps](https://github.com/David-OConnor/pydeps) project, using [FastAPI](https://fastapi.tiangolo.com/), and intended for deployment on [Deta Space](https://deta.space).

This project enables a set of endpoints to get dependency information of python packages published on [pypi.org](https://pypi.org). Specifically, one of these endpoints is intended for use by the [pyflow](https://github.com/David-OConnor/pyflow) executable.

The deployed version of this repository is available at https://pydeps.frbrz.xyz/  
You can use its [OpenAPI documentation](https://pydeps.frbrz.xyz/openapi.json) to [explore the available endpoints](https://pydeps.frbrz.xyz/docs).

## Run locally

This project uses Deta Base to cache the results of each query for dependencies. To enable cache, you must provide the application with a Deta Project Key, and set it in the environment variable `DETA_PROJECT_KEY`.  
The app will still work without it, but your instance could be rate limited from the pypi API if there are too many requests in a short timespan. Note a request is made for each version, for each package.

You can run the application locally by executing inside the Python virtual environment:

```bash
(.venv) $ uvicorn main:app --port 8000
```

Then you can set the `http://localhost:8000/query/` URL on pyflow to use it instead of the official endpoint.
