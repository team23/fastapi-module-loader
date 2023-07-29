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

    def load_in_module(self, module_path: str) -> None:
        """Will import a module under the current module."""

        importlib.import_module(f"{self.__class__.__module__}.{module_path}")

    def load(self) -> None:
        """Hook is executed on ModuleLoader.load()."""

    def pre_setup(self) -> None:
        """Hook is executed on ModuleLoader.setup(). Runs before BaseModule.setup()."""

    def setup(self) -> None:
        """Hook is executed on ModuleLoader.setup()."""

    def post_setup(self) -> None:
        """Hook is executed on ModuleLoader.setup(). Runs after BaseModule.setup()."""
