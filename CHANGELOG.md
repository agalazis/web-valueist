# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-03-20

### Added
- Initial release of the `web_valueist` CLI tool.
- Project URLs added to `pyproject.toml`.
- Added test cases for `ParserNotSupportedError` exception.
- Fetch values from URLs using CSS selectors and perform comparisons against reference values.
- Support for parsing fetched values as `int`, `str`, `float`, and `bool`.
- Support for multiple comparison operators (e.g., `>`, `<`, `=`, `!=`, `>=`, `<=`, `gt`, `lt`, `eq`, `ne`, `ge`, `le`).
- Quantifiers `ANY` and `EVERY` to control how multiple matching elements are evaluated (default is `ANY`).
- CLI options:
  - `--debug` flag to show debug logs including found values.
  - `--json` flag to output input arguments and results in structured JSON format.

### Changed
- Bumped minimum Python version to `>=3.12`.
- Optimized reference value parsing in evaluate loop to execute only once.

### Removed
- Removed `lxml` dependency to avoid build errors, using built-in `html.parser` instead.
