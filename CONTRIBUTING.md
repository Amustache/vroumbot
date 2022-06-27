# Contributing

- [Documentation](#documentation)
- [Development](#development)
  * [Commits](#commits)
  * [Pull requests](#pull-requests)
  * [Testing](#testing)

First of all, thank you for taking the time to help this project, it means a lot.

To sum-up:
* You know how to Python? You can help the project by [reviewing code](https://github.com/AMustache/vroumbot/pulls), [fixing bugs](https://github.com/AMustache/vroumbot/issues), and [adding features](https://github.com/AMustache/vroumbot/issues)!
* No matter what you know, you can always report a bug or [ask for a feature](https://github.com/AMustache/vroumbot/issues), [discuss about the project](https://github.com/AMustache/vroumbot/discussions), or [get in touch](https://t.me/Stache)!

## Documentation

Documentation is particularly important for us, and for this project in particular. Thus, any help is welcome, let alone fixing typos.

- In general, you should not hesitate to be clear about "how it works"!
- This means documenting when you add something, documenting when you change something, documenting when you test something, ...
- In short, documenting so that the next person has to look for it as little as possible!

## Development

Before anything, make sure you followed "Self hosting" in the [README](./README.md).

### Commits

We use pre-commits so that the code is pretty and quite standard. You can find what is happening in the [.pre-commit-config.yaml](./.pre-commit-config.yaml) and [pyproject.toml](./pyproject.toml) files, but basically, for each commit:

- [black](https://github.com/psf/black) formats the code correctly.
- [isort](https://pycqa.github.io/isort/) sorts the imports.

Regarding commit messages:
- [Don't do that](https://xkcd.com/1296/), and we're cool.
- When fixing an issue, please explicit it using the "Fix" keyword, and the exact title of the issue. (e.g., "Fix #42: Loader does not load").

Notes:

- You can run pre-commit independently using `pre-commit run --all-files`
- If, for some reason, you need to commit without a check, use `git commit --no-verify [...]`

### Pull requests

We follow the [GitHub Flow](https://docs.github.com/en/get-started/quickstart/github-flow): all code contributions are submitted via a pull request towards the main branch.

1. Fork the project or open a new branch.
3. Complete your modifications.
4. Merge the main branch.
5. Open a PR.

Moreover:
- When creating a new branch to fix an issue, please refer to the issue in the branch name, starting by its number (e.g., `42-loader-does-not-load`).
- The title of your PR must be explicit.
- When fixing an issue, please explicit it using the "Fix" keyword, and the exact title of the issue. (e.g., "Fix #42: Loader does not load").
- The description may contain any additional information (the more the merrier!), but do not forget to mirror it in the documentation when needed.
- Please take into account that your PR will result in one commit; you may want to squash/rebase yourself beforehand.
- Please link the issues and the PR when needed.

### Testing

Please, test your bot before opening a PR. For that, you can very easily create a bot with BotFather, and use the commands in it. Just use its token in `secret.py`, and go wild.

## Thank you in advance!
