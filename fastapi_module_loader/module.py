import importlib
from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
    from fastapi_module_loader.loader import ModuleLoader


class BaseModule:
    """
    Base class for modules auto loader configs.

    Usage
    ===

    In your modules `__init__.py` create a subclass of `ModuleConfig`,
    then put it into MODULES in config.py:
    ```python
    from fastapi_module_loader import BaseModule


    class SomethingModule(BaseModule):
        def setup(self):
            self.load_in_module("hooks")
    ```
    """

    loader: "ModuleLoader"

    def __init__(self, loader: "ModuleLoader") -> None:
        self.loader = loader

    def pre_setup(self) -> None:
        pass

    def setup(self) -> None:
        pass

    def post_setup(self) -> None:
        pass

    def load_in_module(self, file: str) -> None:
        importlib.import_module(f"{self.__class__.__module__}.{file}")
