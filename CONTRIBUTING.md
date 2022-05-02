# How to contribute

## Dependencies

We use `poetry` to manage the [dependencies](https://github.com/python-poetry/poetry).
If you don't have `poetry`, you should install it (`brew install poetry` on MacOS
with Homebrew).

In addition, we use `b5` to manage local tasks. See
[b5 project page](https://github.com/team23/b5) for more details.

To install dependencies and prepare [`pre-commit`](https://pre-commit.com/) hooks
you would need to run `install` command:

```bash
b5 install
```

To activate your `virtualenv` run `b5 poetry shell`.

## Linting

After installation you may execute code linting.

```bash
b5 lint
```

### Checks

Many checks are configured for this project. Command `b5 lint` will run flake8.
The `b5 safety` command will look at the security of your code.

Command `b5 check` applies all checks.

### Before submitting

Before submitting your code please do the following steps:

1. Add any changes you want
1. Add tests for the new changes
1. Edit documentation if you have changed something significant
1. Run `b5 lint` to ensure that types, security and docstrings are okay.

## Other help

You can contribute by spreading a word about this library.
It would also be a huge contribution to write
a short article on how you are using this project.
You can also share your best practices with us.
