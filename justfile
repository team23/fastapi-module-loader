install-pre-commit:
    #!/usr/bin/env bash
    if ( which pre-commit > /dev/null 2>&1 )
    then
        pre-commit install --install-hooks
    else
        echo "-----------------------------------------------------------------"
        echo "pre-commit is not installed - cannot enable pre-commit hooks!"
        echo "Recommendation: Install pre-commit ('brew install pre-commit')."
        echo "-----------------------------------------------------------------"
    fi

install: install-pre-commit (poetry "install")

update: (poetry "install")

poetry *args:
    poetry {{args}}

test *args: (poetry "run" "pytest" "--cov=fastapi_module_loader" "--cov-report" "term-missing:skip-covered" args)

test-all: (poetry "run" "tox")

ruff *args: (poetry "run" "ruff" "check" "fastapi_module_loader" "tests" args)

mypy *args:  (poetry "run" "mypy" "fastapi_module_loader" args)

lint: ruff mypy

publish: (poetry "publish" "--build")
