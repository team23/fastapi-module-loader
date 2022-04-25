# fastapi-module-loader

<div align="center">

[![Build status](https://github.com/team23/fastapi-module-loading/workflows/build/badge.svg?branch=master&event=push)](https://github.com/team23/fastapi-module-loading/actions?query=workflow%3Abuild)
[![Python Version](https://img.shields.io/pypi/pyversions/fastapi-module-loader.svg)](https://pypi.org/project/fastapi-module-loader/)
[![Dependencies Status](https://img.shields.io/badge/dependencies-up%20to%20date-brightgreen.svg)](https://github.com/team23/fastapi-module-loading/pulls?utf8=%E2%9C%93&q=is%3Apr%20author%3Aapp%2Fdependabot)

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Security: bandit](https://img.shields.io/badge/security-bandit-green.svg)](https://github.com/PyCQA/bandit)
[![Pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/team23/fastapi-module-loading/blob/master/.pre-commit-config.yaml)
[![Semantic Versions](https://img.shields.io/badge/%20%20%F0%9F%93%A6%F0%9F%9A%80-semantic--versions-e10079.svg)](https://github.com/team23/fastapi-module-loading/releases)
[![License](https://shields.io/badge/license-MIT-green)](https://github.com/team23/fastapi-module-loading/blob/master/LICENSE)
![Coverage Report](assets/images/coverage.svg)

FastAPI modules loading for better structure in your projects (like Django AppConfig)

</div>

## Example

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

## Installation

```bash
pip install -U fastapi-module-loader
```

or install with `Poetry`

```bash
poetry add fastapi-module-loader
```


### Makefile usage

[`Makefile`](https://github.com/team23/fastapi-module-loading/blob/master/Makefile) contains a lot of functions for faster development.

<details>
<summary>1. Download and remove Poetry</summary>
<p>

To download and install Poetry run:

```bash
make poetry-download
```

To uninstall

```bash
make poetry-remove
```

</p>
</details>

<details>
<summary>2. Install all dependencies and pre-commit hooks</summary>
<p>

Install requirements:

```bash
make install
```

Pre-commit hooks coulb be installed after `git init` via

```bash
make pre-commit-install
```

</p>
</details>

<details>
<summary>3. Codestyle</summary>
<p>

Automatic formatting uses `pyupgrade`, `isort` and `black`.

```bash
make codestyle

# or use synonym
make formatting
```

Codestyle checks only, without rewriting files:

```bash
make check-codestyle
```

> Note: `check-codestyle` uses `isort`, `black` and `darglint` library

Update all dev libraries to the latest version using one comand

```bash
make update-dev-deps
```

<details>
<summary>4. Code security</summary>
<p>

```bash
make check-safety
```

This command launches `Poetry` integrity checks as well as identifies security issues with `Safety` and `Bandit`.

```bash
make check-safety
```

</p>
</details>

</p>
</details>

<details>
<summary>5. Type checks</summary>
<p>

Run `mypy` static type checker

```bash
make mypy
```

</p>
</details>

<details>
<summary>6. Tests with coverage badges</summary>
<p>

Run `pytest`

```bash
make test
```

</p>
</details>

<details>
<summary>7. All linters</summary>
<p>

Of course there is a command to ~~rule~~ run all linters in one:

```bash
make lint
```

the same as:

```bash
make test && make check-codestyle && make mypy && make check-safety
```

</p>
</details>


<details>
<summary>8. Cleanup</summary>
<p>
Delete pycache files

```bash
make pycache-remove
```

Remove package build

```bash
make build-remove
```

Delete .DS_STORE files

```bash
make dsstore-remove
```

Remove .mypycache

```bash
make mypycache-remove
```

Or to remove all above run:

```bash
make cleanup
```

</p>
</details>

## 📈 Releases

You can see the list of available releases on the [GitHub Releases](https://github.com/team23/fastapi-module-loading/releases) page.

We follow [Semantic Versions](https://semver.org/) specification.

We use [`Release Drafter`](https://github.com/marketplace/actions/release-drafter). As pull requests are merged, a draft release is kept up-to-date listing the changes, ready to publish when you’re ready. With the categories option, you can categorize pull requests in release notes using labels.

### List of labels and corresponding titles

|               **Label**               |  **Title in Releases**  |
| :-----------------------------------: | :---------------------: |
|       `enhancement`, `feature`        |       🚀 Features       |
| `bug`, `refactoring`, `bugfix`, `fix` | 🔧 Fixes & Refactoring  |
|       `build`, `ci`, `testing`        | 📦 Build System & CI/CD |
|              `breaking`               |   💥 Breaking Changes   |
|            `documentation`            |    📝 Documentation     |
|            `dependencies`             | ⬆️ Dependencies updates |

You can update it in [`release-drafter.yml`](https://github.com/team23/fastapi-module-loading/blob/master/.github/release-drafter.yml).

GitHub creates the `bug`, `enhancement`, and `documentation` labels for you. Dependabot creates the `dependencies` label. Create the remaining labels on the Issues tab of your GitHub repository, when you need them.

## 🛡 License

[![License](https://img.shields.io/github/license/team23/fastapi-module-loader)](https://github.com/team23/fastapi-module-loading/blob/master/LICENSE)

This project is licensed under the terms of the `MIT` license. See [LICENSE](https://github.com/team23/fastapi-module-loading/blob/master/LICENSE) for more details.

## This project was generated with [![🚀 Your next Python package needs a bleeding-edge project structure.](https://img.shields.io/badge/python--package--template-%F0%9F%9A%80-brightgreen)](https://github.com/TezRomacH/python-package-template)
