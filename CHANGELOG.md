# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [3.0.0] - Nain Singh Rawat - 2026-03-21

## What's Changed
* ci: add prepare-release github action to automate version bumps by @agalazis in https://github.com/agalazis/web-valueist/pull/26
* Uniform API: return value as list and introduce typing by @agalazis in https://github.com/agalazis/web-valueist/pull/27
* feat: add strict_parsing mode and type hinted parsed returns by @agalazis in https://github.com/agalazis/web-valueist/pull/28
* ci: update release workflow to trigger downstream, generate notes, and include name in changelog by @agalazis in https://github.com/agalazis/web-valueist/pull/29


**Full Changelog**: https://github.com/agalazis/web-valueist/compare/v1.0.1...v3.0.0

## [2.0.0] - 2026-03-21

### Added
- 

## [1.0.0] - 2026-03-20

### Added
- Project URLs added to `pyproject.toml`.
- Added test cases for `ParserNotSupportedError` exception.

### Changed
- Bumped minimum Python version to `>=3.12`.
- Optimized reference value parsing in evaluate loop to execute only once.

### Removed
- Removed `lxml` dependency to avoid build errors, using built-in `html.parser` instead.

## [0.1.0] - 2026-03-18

### Added
- Initial release of the `web_valueist` CLI tool.
- Fetch values from URLs using CSS selectors and perform comparisons against reference values.
- Support for parsing fetched values as `int`, `str`, `float`, and `bool`.
- Support for multiple comparison operators (e.g., `>`, `<`, `=`, `!=`, `>=`, `<=`, `gt`, `lt`, `eq`, `ne`, `ge`, `le`).
- Quantifiers `ANY` and `EVERY` to control how multiple matching elements are evaluated (default is `ANY`).
- CLI options:
  - `--debug` flag to show debug logs including found values.
  - `--json` flag to output input arguments and results in structured JSON format.
