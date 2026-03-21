# Release Workflow

This project uses an automated GitHub Actions workflow to handle new releases. The **Prepare Release** workflow manages versioning, changelog updates, and the creation of GitHub releases.

## How to Trigger a Release

You can trigger a new release manually from the GitHub website by following these steps:

1. Go to the **Actions** tab in the repository.
2. In the left sidebar, click on **Prepare Release**.
3. On the right side, click the **Run workflow** dropdown button.
4. Select the branch you want to run the workflow on (usually `main`).
5. Choose the **Version bump type**:
   - `patch`: Use for backward-compatible bug fixes (e.g., `1.0.0` -> `1.0.1`).
   - `minor`: Use for new backward-compatible features (e.g., `1.0.0` -> `1.1.0`).
   - `major`: Use for incompatible API changes (e.g., `1.0.0` -> `2.0.0`).
6. Click the green **Run workflow** button.

## What the Workflow Does Behind the Scenes

Once triggered, the workflow automatically performs the following steps:

1. **Checks out the repository.**
2. **Sets up Python and installs Poetry.**
3. **Bumps the version** in `pyproject.toml` using `poetry version <bump_type>`.
4. **Generates Release Notes** by using the GitHub API to fetch auto-generated release notes since the previous tag.
5. **Updates `CHANGELOG.md`** by automatically adding a new release header (e.g., `## [1.0.1] - Columbus - 2026-03-21`) and injecting the generated release notes.
6. **Commits and pushes** the updated `pyproject.toml` and `CHANGELOG.md` to the branch.
7. **Creates a GitHub Release** using the GitHub CLI (`gh release create`), which automatically tags the new version in Git (e.g., `v1.0.1`).

By creating a GitHub Release, this workflow subsequently triggers the existing `Publish to PyPI` and `Deploy docs to GitHub Pages` workflows, completing the full release pipeline.

> **Note:** For the downstream workflows to be triggered successfully upon a GitHub Release, a repository secret named `PAT` (Personal Access Token) with the appropriate permissions must be provided. Actions performed with the default `GITHUB_TOKEN` intentionally prevent downstream workflow triggers to avoid infinite loops.
