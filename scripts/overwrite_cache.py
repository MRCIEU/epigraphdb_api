"""Overwrite cache."""

from loguru import logger
from starlette.testclient import TestClient

from app.main import app


def main():
    client = TestClient(app)
    logger.info("Overwrite schema cache.")
    client.get(
        "/meta/schema",
        params={"graphviz": False, "plot": False, "overwrite": True},
    )

    logger.info("Done.")


if __name__ == "__main__":
    main()
