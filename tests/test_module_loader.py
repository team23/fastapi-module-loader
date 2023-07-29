from unittest import mock

import pytest

from fastapi_module_loader import BaseModule, ModuleLoader
from fastapi_module_loader.exceptions import ImproperlyConfiguredModules


class WorkingModule(BaseModule):
    pass


class ExceptionRaisingModule(BaseModule):
    def setup(self) -> None:
        raise ValueError


class SubmoduleLoadingModule(BaseModule):
    def setup(self) -> None:
        self.load_in_module("sadly_does_not_exist")


TEST_MODULES = [
    "tests.test_module_loader.WorkingModule",
]
TEST_RAISING_MODULES = [
    "tests.test_module_loader.ExceptionRaisingModule",
]
TEST_LOADING_MODULES = [
    "tests.test_module_loader.SubmoduleLoadingModule",
]


def test_module_loader_allows_multiple_calls_to_load() -> None:
    loader = ModuleLoader(TEST_MODULES)
    loader.load()
    loader.load()


def test_module_loader_needs_load_to_be_called_before_setup() -> None:
    loader = ModuleLoader(TEST_MODULES)
    with pytest.raises(ImproperlyConfiguredModules):
        loader.setup()

    # Should work after load
    loader.load()
    loader.setup()


def test_module_loader_will_fail_on_missing_module_paths() -> None:
    loader = ModuleLoader(["this.does.not.exist"])
    with pytest.raises(ImproperlyConfiguredModules):
        loader.load()


def test_module_loader_will_fail_on_missing_module_in_import() -> None:
    loader = ModuleLoader(["tests.test_module_loader.DoesNotExist"])
    with pytest.raises(ImproperlyConfiguredModules):
        loader.load()


def test_module_loader_will_ensure_module_type() -> None:
    loader = ModuleLoader(
        [
            # use this test function, which is not a BaseModules
            "tests.test_module_loader.test_module_loader_will_ensure_module_type",
        ],
    )
    with pytest.raises(ImproperlyConfiguredModules):
        loader.load()


def test_module_will_be_able_to_import_submodules() -> None:
    loader = ModuleLoader(TEST_LOADING_MODULES)
    loader.load()
    with mock.patch("importlib.import_module") as import_module_mock:
        loader.setup()
    import_module_mock.assert_called_once_with(
        "tests.test_module_loader.sadly_does_not_exist",
    )


def test_module_loader_allows_multiple_setup_calls() -> None:
    loader = ModuleLoader(TEST_MODULES)
    loader.load()
    loader.setup()
    loader.setup()


def test_module_loader_calls_module_config_setup() -> None:
    loader = ModuleLoader(TEST_RAISING_MODULES)
    loader.load()
    with pytest.raises(ValueError):
        loader.setup()
