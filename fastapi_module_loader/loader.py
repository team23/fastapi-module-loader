import importlib
from typing import Dict, List, Optional

from fastapi_module_loader.exceptions import ImproperlyConfiguredModules
from fastapi_module_loader.module import BaseModule


class ModuleLoader:
    """
    Loads `ModuleConfig` instances.
    """

    modules: Dict[str, Optional[BaseModule]]
    is_loaded: bool = False
    is_setup: bool = False

    def __init__(self, modules: List[str]) -> None:
        self.modules = {
            module: None
            for module
            in modules
        }

    @classmethod
    def _load_module(cls, module_import: str):  # noqa: ANN206
        package_import, module_name = module_import.rsplit('.', 1)
        try:
            package = importlib.import_module(package_import)
        except ImportError:
            raise ImproperlyConfiguredModules(
                f'Could not import "{package_import}"',
            )

        try:
            module_class = getattr(package, module_name)
        except AttributeError:
            raise ImproperlyConfiguredModules(
                f'Could not find "{module_name}" in "{package_import}"',
            )

        if (
            not isinstance(module_class, type)
            or not issubclass(module_class, BaseModule)
        ):
            raise ImproperlyConfiguredModules(
                f'"{module_import}" must be a subclass of "BaseModule"',
            )

        return module_class

    def load(self) -> None:
        for module_import, module in self.modules.items():
            if module is not None:
                continue

            module = self._load_module(module_import)(self)
            self.modules[module_import] = module

            try:
                # Call the load() hook
                module.load()
            except Exception as O_o:
                raise ImproperlyConfiguredModules(
                    f'Could not load "{module_import}", as the load() hook did raise '
                    f'an exception: {O_o}',
                ) from O_o

        self.is_loaded = True

    @property
    def loaded_modules(self) -> List[BaseModule]:
        return [
            module
            for module
            in self.modules.values()
            if module is not None
        ]

    def setup(self) -> None:
        if not self.is_loaded:
            raise ImproperlyConfiguredModules(
                'Modules must be loaded first',
            )

        if self.is_setup:
            return

        # Call the pre_setup() hook
        for module in self.loaded_modules:
            module.pre_setup()

        # Call the setup() hook
        for module in self.loaded_modules:
            module.setup()

        # Call the post_setup() hook
        for module in self.loaded_modules:
            module.post_setup()

        self.is_setup = True
