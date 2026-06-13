# Releasing

AGMH uses Release Please for release PRs, version bumps, changelog generation,
Git tags, and GitHub Releases. PyPI publishing is handled by GitHub Actions
using PyPI Trusted Publishing.

## Release Flow

1. Merge ordinary work into `main` using Conventional Commit messages.
2. The `Release Please` workflow opens or updates a release PR.
3. Review the generated version bump and `CHANGELOG.md`.
4. Merge the release PR.
5. Release Please creates the Git tag and GitHub Release.
6. The same `Release Please` workflow builds the source distribution and wheel,
   checks them with Twine, and publishes them to PyPI.

Release Please updates:

- `CHANGELOG.md`
- `.release-please-manifest.json`
- `pyproject.toml`
- `src/anti_gh_ms_hysteria/__init__.py`

## Commit Messages

Release Please reads Conventional Commits:

```text
fix: correct token rotation after HTTP 401
feat: add a new destination provider
docs: clarify remote mirror setup
feat!: change configuration schema
```

Version impact:

- `fix:` creates a patch release.
- `feat:` creates a minor release.
- `feat!:` or `BREAKING CHANGE:` creates a major release.
- `docs:` is included in Python release notes by Release Please, but not every
  documentation-only commit needs a release.

To force a specific version, include a `Release-As` footer:

```text
chore: release 0.2.0

Release-As: 0.2.0
```

## PyPI Trusted Publishing

Configure a PyPI trusted publisher for the `agmh` project:

- Owner: `haltman-io`
- Repository: `agmh`
- Workflow filename: `release-please.yml`
- Environment name: `pypi`

No PyPI API token is required when Trusted Publishing is configured. The
workflow requests an OpenID Connect token through GitHub Actions and PyPI
validates the repository, workflow, and environment.

`publish-pypi.yml` exists as a manual fallback for maintainers. If you want to
use that fallback, register it as an additional trusted publisher with workflow
filename `publish-pypi.yml` and the same owner, repository, and `pypi`
environment.

## TestPyPI Trusted Publishing

Configure a TestPyPI trusted publisher for manual test releases:

- Owner: `haltman-io`
- Repository: `agmh`
- Workflow filename: `publish-testpypi.yml`
- Environment name: `testpypi`

Run it from GitHub Actions with `workflow_dispatch`.

## Local Package Checks

Before merging packaging changes:

```bash
python -m compileall -q src tests
PYTHONPATH=src python -m unittest discover -s tests -v
python -m build
python -m twine check --strict dist/*
python -m pip install -e . --dry-run --no-deps
```

Remove generated `build/`, `dist/`, and `*.egg-info/` directories before
committing if they appear locally.
