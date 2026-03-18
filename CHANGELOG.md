# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2024-05-24

### Added
- Initial release of the `web_valueist` CLI tool.
- Fetch values from URLs using CSS selectors and perform comparisons against reference values.
- Support for parsing fetched values as `int`, `str`, `float`, and `bool`.
- Support for multiple comparison operators (e.g., `>`, `<`, `=`, `!=`, `>=`, `<=`, `gt`, `lt`, `eq`, `ne`, `ge`, `le`).
- Quantifiers `ANY` and `EVERY` to control how multiple matching elements are evaluated (default is `ANY`).
- CLI options:
  - `--debug` flag to show debug logs including found values.
  - `--json` flag to output input arguments and results in structured JSON format.
