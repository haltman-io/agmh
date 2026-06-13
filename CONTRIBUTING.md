# Contributing

AGMH accepts focused changes that keep the tool reliable, scriptable, and easy
to audit.

## Development Setup

```bash
python -m venv .venv
. .venv/bin/activate
python -m pip install -U pip
python -m pip install -e ".[tui,dev]"
```

On Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -U pip
python -m pip install -e ".[tui,dev]"
```

## Local Checks

Run these before sending changes:

```bash
python -m compileall -q src tests
PYTHONPATH=src python -m unittest discover -s tests -v
python -m build
python -m twine check --strict dist/*
python -m pip install -e . --dry-run --no-deps
```

## Change Guidelines

- Keep source/destination terminology precise.
- Do not reintroduce legacy `aghm` names.
- Do not log secrets, tokens, webhook URLs, or credentialized Git URLs.
- Prefer small, reviewable changes.
- Add focused tests for behavior changes.
- Update `README.md`, `config.example.toml`, and `CHANGELOG.md` when user-facing
  behavior changes.
- Use Conventional Commit messages so Release Please can generate releases and
  changelog entries.

## Security Issues

Do not report security issues through public issues or pull requests. Follow
`SECURITY.md`.

## Releases

See `RELEASING.md`.
