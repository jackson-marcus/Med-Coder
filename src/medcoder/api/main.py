"""FastAPI application factory."""

from __future__ import annotations

import logging

from fastapi import FastAPI

from medcoder import __version__
from medcoder.api.routes import router

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")


def create_app() -> FastAPI:
    app = FastAPI(
        title="medcoder",
        description="Assistive ICD-10 coding: clinical note to ranked code suggestions via abbreviation expansion and hybrid retrieval, with a top-k accuracy eval harness. Human coder confirms every code.",
        version=__version__,
    )
    app.include_router(router)
    return app


app = create_app()
