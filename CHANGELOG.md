# Changelog

All notable project changes should be documented in this file.

This project uses human-readable release notes grouped by version. Dates use
`YYYY-MM-DD`.

## [Unreleased]

### Added

- Security reporting policy.
- Contribution and support guidelines.
- Project maintenance files and GitHub issue/PR templates.
- PyPI/TestPyPI publishing workflows using Trusted Publishing.
- Release Please configuration for automated version bumps, changelog updates,
  Git tags, and GitHub Releases.
- CI workflow for Python tests and distribution checks.

### Changed

- Package metadata now identifies `extencil <extencil@segfault.net>` as author
  and maintainer.

## [0.1.0] - 2026-06-13

### Added

- Initial AGMH CLI package.
- Repository discovery from GitHub, GitLab, Forgejo/Codeberg, Bitbucket, and
  SourceHut sources.
- Local mirror, remote mirror, full mirror, and watching workflows.
- Destination support for GitHub, GitLab, Forgejo/Codeberg, Bitbucket, and
  SourceHut.
- Optional marker commits before remote mirrors.
- Optional webhook notifications for generic endpoints, Discord, and Telegram.
