import importlib
from typing import Dict, List

from .base import BaseModule


class Loader:
    modules: Dict[str, BaseModule]
    is_loaded: bool = False
    is_setup: bool = False

    def __init__(self, modules: List[str]) -> None:
        self.modules = {}
        self._load(modules)

    @classmethod
    def _load_module(cls, module_import: str):  # noqa: ANN206
        package_import, module_name = module_import.rsplit('.', 1)
        package = importlib.import_module(package_import)
        return getattr(package, module_name)

    def _load(self, modules: List[str]) -> None:
        if self.is_loaded:
            return

        for module_import in modules:
            self.modules[module_import] = self._load_module(module_import)()

        self.is_loaded = True

    def setup(self) -> None:
        if not self.is_loaded:
            raise RuntimeError('Modules must be loaded first')

        if self.is_setup:
            return

        for module in self.modules.values():
            module.setup()

        self.is_setup = True
