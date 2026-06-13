# Changelog

All notable project changes should be documented in this file.

This project uses human-readable release notes grouped by version. Dates use
`YYYY-MM-DD`.

## [0.3.0](https://github.com/haltman-io/agmh/compare/v0.2.0...v0.3.0) (2026-06-13)


### Features

* update documentation and templates for improved clarity and usability ([78320e7](https://github.com/haltman-io/agmh/commit/78320e73e93042ce1c7603d1d0ad2b4a6a4cad3c))

## [0.2.0](https://github.com/haltman-io/agmh/compare/v0.1.0...v0.2.0) (2026-06-13)


### Features

* add notification system with webhooks for events ([174db38](https://github.com/haltman-io/agmh/commit/174db38ae36085ec69bf55d5e6ddc59a7faa259c))
* enhance project structure with CI workflows, release automation, and packaging improvements ([dceb257](https://github.com/haltman-io/agmh/commit/dceb2573c32944a04ef2af54ee14cfeb772ceb34))
* enhance project structure with CI workflows, release automation… ([19e3806](https://github.com/haltman-io/agmh/commit/19e3806bb27dce7c99b8769ecb2c899c48bd9746))
* update project metadata, add templates, and enhance documentation ([5ecef83](https://github.com/haltman-io/agmh/commit/5ecef83d860032a08cf809337ae267b883e76b8b))

## [Unreleased]

### Added

- PyPI project links and installation guidance for published package users.
- Default GitHub review ownership through `.github/CODEOWNERS`.

### Changed

- README now treats `pip install agmh` as the primary installation path.
- Support, maintainer, and release documentation now reference the published
  PyPI project.

## [0.2.0](https://github.com/haltman-io/agmh/compare/v0.1.0...v0.2.0) (2026-06-13)

### Features

- Add notification system with webhooks for events
  ([174db38](https://github.com/haltman-io/agmh/commit/174db38ae36085ec69bf55d5e6ddc59a7faa259c)).
- Enhance project structure with CI workflows, release automation, and
  packaging improvements
  ([dceb257](https://github.com/haltman-io/agmh/commit/dceb2573c32944a04ef2af54ee14cfeb772ceb34)).
- Enhance project structure with CI workflows and release automation
  ([19e3806](https://github.com/haltman-io/agmh/commit/19e3806bb27dce7c99b8769ecb2c899c48bd9746)).
- Update project metadata, add templates, and enhance documentation
  ([5ecef83](https://github.com/haltman-io/agmh/commit/5ecef83d860032a08cf809337ae267b883e76b8b)).

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
