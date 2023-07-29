# `fastapi-module-loader`

This library allows you to load modules in a structured and well defined way. The overall idea is explained pretty
quick, we have a list of modules and then ensure all those are basically imported. Also we allow the module classes to
execute additional code on loading. This is useful to for example resolve forward references with pydantic, to register
some hooks or just load all SQLAlchemy ORM models so relationships work.

The module loader idea is based on what Django does using `AppConfig`'s - so if you know those you might find this
pretty straight forward.

# Example FastAPI setup

Lets say we are using the following folder structure in your project, `modules` may contain a list of modules
used by your application:

```text
yourapp
|-- modules
|   `-- something
|       `-- __init__.py     <- SomethingModule is defined here, see technical details below
|-- config.py               <- Your config file
|-- loader.py               <- This is where you put the global loader instance
`-- main.py                 <- Your normal FastAPI application lives here
```

Now lets put the MODULES list into `config.py`:

```python
MODULES = [
    "yourapp.modules.something.SomethingModules",
]
```

Then add the loader to your `loader.py`:

```python
from fastapi_module_loader import ModuleLoader

from yourapp.config import MODULES


loader = ModuleLoader(MODULES)
```

**Note:** We are **NOT** calling `loader.load()` or `loader.setup()` here. This is because we want to do this in our
`main.py` file so we have control when this actually happens.

Then change your `main.py` to look like this:

```python
from fastapi import FastAPI

from yourapp.loader import loader


@asynccontextmanager
async def lifespan(app: FastAPI):
    loader.setup()  # Setup everything on FastAPI startup
    yield


loader.load()  # Ensure everything is loaded
app = FastAPI(lifespan=lifespan)

# ...put the actual FastAPI code here
```

# Use cases

Those are some use cases we encountered while working on projects. Those use cases led us to create this library:

* `main.py`: Load the modules to ensure everything is setup for the FastAPI app.
* In alembic migrations `env.py`: Ensure all `orm.py` are loaded and the alembic migrations can "see" all the ORM
  models. Otherwise, detecting any changes would not be possible at all.  
  (see https://alembic.sqlalchemy.org/en/latest/tutorial.html#the-migration-environment)
* To register any hooks bound to `async-signals` Signal instances.  
  (see https://github.com/team23/async-signals)
* There will be many additional use cases for using the module loader. If you have any interesting use case please
  open an issue and tell us about it. 😉

# Technical details

## Basic structure

The class `ModuleLoader` is the main entry point for the module loader system. It needs to be instantiated with a
list of modules as strings. You have to initialize the module loader in some global place for your application. This
can be done directly in `main.py`, although it is recommended to use a separate file for this like `loader.py`.

Getting you own loader instance can look like this:
```python
from fastapi_module_loader import ModuleLoader


# We recommend putting the module list into your normal config file - if you have one
MODULES = [
    "yourapp.modules.something.SomethingModules",
    "yourapp.modules.something_else.SomethingElseModules",
    "yourapp.modules.etc.EtcModules",
]


loader = ModuleLoader(MODULES)
```

The actual loading process then works like this:
1. Using `loader.load()` will import all the modules passed to the constructor. It will use `importlib` to load the
   module and then instantiate the module class. After this is done it will call the `load()` method on the modules -
   you can use this hook to load additional modules or similar.
2. The `loader.setup()` will execute the `setup()` method of all the modules. This is where the modules should do
   additional setup work like resolving `ForwardRef`'s or registering hooks.  
   Note that `loader.setup()` will actually call `pre_setup()`, then `setup()` and finally `post_setup()` on the 
   modules. This allows you to have different stages of your setup process.

## Module structure

A module is a class that inherits from `BaseModule`. It may implement the `setup()` and other methods as hooks. All
methods will be called on module loading/setup.

Example for a module:

```python
from fastapi_module_loader import BaseModule


class SomethingModule(BaseModule):
    def setup(self):  # providing a setup method is optional
        print("Hello world!")
```

## Loading process

`loader.load()` will import all the modules and then call the `load()` method on them. This is the place where you
should load further modules if you need to.

```python
from yourapp.loader import loader  # Import has to match your own setup


loader.load()  # will import all modules and call load() on each of them
```

When all modules are loaded you may use `loader.setup()` to execute the `setup()` method on all modules. This is the
place where you should do your actual setup work.

```python
from yourapp.loader import loader  # Import has to match your own setup


loader.setup()  # will call pre_setup(), setup() and then post_setup() on all modules
```

## Loading further modules in `load()`

It is a very common use case to load further modules in the `setup()` method. To support this use case the `BaseModule`
class provides a method `load_in_module()` then will load given module names inside the current module scope.

Example:

```python
from fastapi_module_loader import BaseModule


class SomethingModule(BaseModule):
    def setup(self):
        self.load_in_module("orm")
```

This will load `yourapp.modules.something.orm` if the module file itself is placed in
`yourapp/modules/something/__init__.py`.

See this example structure:

```text
yourapp
`-- modules
    `-- something
        |-- __init__.py     <- SomethingModule is defined here
        |-- etc...py
        |-- orm.py          <- This is loaded
        `-- etc...py
```

**Note:** For `load_in_module` to work you are required to put the modules class (`SomethingModule` in this example)
into the `__init__.py` file of the module. Otherwise the module loader will not be able to find the module you want
it to load.

## Integrating the module loader

To ensure everything is setup properly you should just call the methods mentioned above. This may for example look
like this:

```python
from fastapi_module_loader import loader


loader.load()
loader.setup()


# Put the actual code here
```

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
