# `fastapi-module-loader`

This module allows us to load modules in a structured and well defined way. The basic idea is pretty simple, we
have a list of modules and then ensure all those are basically imported. Also we allow the module classes to execute
additional code on loading. This is useful to for example resolve forward references with pydantic, to register
some hooks or just load all SQLAlchemy ORM models so relationships work.

## Basic structure

The class `ModuleLoader` is the main entry point for the module loader system. It needs to be instantiated with a
list of modules as strings. A global (singleton-like) instance of the module loader is provided in
`fastapi_module_loader`, for production code you should always just use this instance.

The actual loading process then is pretty simple:
1. Using `loader.load()` will import all the modules passed to the constructor.
2. The `loader.setup()` will execute the `setup()` method of all the modules. This is where the modules can do
   additional setup work.

For `fastapi_module_loader` the modules that are loaded are configured using `fastapi_module_loader.MODULES`. This is a list of strings that
represent the modules to load. The module names are absolute.

## Module structure

A module is a class that inherits from `BaseModule`. It may implement the `setup()` method. This method will be
called after all modules have been imported.

Example for a module:

```python
from fastapi_module_loader import BaseModule


class SomethingModule(BaseModule):
    def setup(self):  # providing a setup method is optional
        print("Hello world!")
```

# Loading further modules in `setup()`

It is a very common use case to load further modules in the `setup()` method. To support this use case the `BaseModule`
class provides a method `load_in_module()` then will load given module names inside the current module scope.

Example:

```python
from fastapi_module_loader import BaseModule


class SomethingModule(BaseModule):
    def setup(self):
        self.load_in_module("orm")
```

This will load `yourapp.modules.something.orm` if the module file itself is placed in `yourapp/modules/something/__init__.py`.

```text
yourapp
`-- modules
    `-- something
        |-- __init__.py     <- SomethingModule is defined here
        |-- etc...py
        |-- orm.py          <- This is loaded
        `-- etc...py
```

## Integrating the module loader

To ensure everything is setup properly you should just call the methods mentioned above. This may for example look
like this:

```python
from fastapi_module_loader import loader


loader.load()
loader.setup()


# Put the actual code here
```

Cases we use this:
* `main.py`: Load the modules to ensure everything is setup for the FastAPI app.
* alembic migrations `env.py`: Ensure all `orm.py` are loaded and the alembic migrations can "see" all the ORM models.
  Otherwise, detecting any changes would not be possible at all.

## Exceptions

The module loader will raise `ImproperlyConfiguredModules` if anything went wrong during handling the modules and
loading those, this includes:
* A module could not be imported
* A module does not inherit from `BaseModule`
* You are calling `loader.setup()` when `loader.load()` has not been called before

Note however that all exceptions raised by the `setup()` method of the modules will just be passed through. The module
loader will not catch now handle them. This is also the case if a modules to be loaded by `Self.load_in_module()`
does not exist. Generally you have to handle those errors in `setup()` yourself.

# Contributing

If you want to contribute to this project, feel free to just fork the project,
create a dev branch in your fork and then create a pull request (PR). If you
are unsure about whether your changes really suit the project please create an
issue first, to talk about this.
