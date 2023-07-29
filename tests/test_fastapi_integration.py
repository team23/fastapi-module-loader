from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.testclient import TestClient

from fastapi_module_loader import BaseModule, ModuleLoader


class TrackingModule(BaseModule):
    is_load: bool = False
    is_pre_setup: bool = False
    is_setup: bool = False
    is_post_setup: bool = False

    def load(self) -> None:
        self.is_load = True

    def pre_setup(self) -> None:
        self.is_pre_setup = True

    def setup(self) -> None:
        self.is_setup = True

    def post_setup(self) -> None:
        self.is_post_setup = True


loader = ModuleLoader(
    [
        "tests.test_fastapi_integration.TrackingModule",
    ],
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    loader.setup()  # Setup everything on FastAPI startup
    yield


loader.load()  # Ensure everything is loaded
app = FastAPI(lifespan=lifespan)  # Pass the lifespan context manager to FastAPI


@app.get("/")
async def root():
    assert loader.is_loaded is True
    assert loader.loaded_modules[0].is_load is True
    assert loader.is_setup is True
    assert loader.loaded_modules[0].is_pre_setup is True
    assert loader.loaded_modules[0].is_setup is True
    assert loader.loaded_modules[0].is_post_setup is True
    return {"message": "all ok"}


def test_fastapi_integration() -> None:
    with TestClient(app) as client:
        response = client.get("/")
        assert response.status_code == 200
