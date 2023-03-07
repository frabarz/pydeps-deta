---
title: "pydeps"
tagline: "An API server for pyflow, to provide pypi package dependencies."
theme_color: "#11a453"
git: "https://github.com/frabarz/pydeps"
homepage: "https://pydeps.frbrz.xyz"
---

This application provides endpoints for [pyflow](https://github.com/David-OConnor/pyflow) to get the info it needs to switfly calculate the right versions of the dependencies to install. pyflow is an excellent package manager for Python projects, written in Rust.

This is complete rewrite of the original [pydeps](https://github.com/David-OConnor/pydeps) project, made with Django and deployed on Heroku.
You can use the deployed server in pyflow to replace the original server, which has since died down.
