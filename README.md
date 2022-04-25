# fastapi-module-loader

Central module loading mechanism for the project. Each module may provide methods
to setup the module.

Example module usage:

```python
from fastapi_module_loader import BaseModule

class Module(BaseModule):
    def setup(self):
        from something.dto import SomethingInResponse

        # We have to correctly setup both, as InlineArticle is used internally
        # by the InlineRegistry and ArticleInResponse will be used in responses.
        SomethingInResponse.update_forward_refs()
```

The setup code will run after the basic FastAPI app loading is done and when all
models are basically defined. This means we can do things like calling `update_forward_refs()`
to resolve `ForwardRef` field types. Of course this can be used to any setup step.

## FastAPI integration notes

For the module loading mechanism to work you need to ensure to call `loader.setup()`
in your `main.py`.
