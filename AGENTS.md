# AI contribution instructions

These rules apply to any AI agent or coding assistant that modifies this repository.

## Versioning policy

- The project follows Semantic Versioning: `MAJOR.MINOR.PATCH`.
- **Every commit that changes repository content must increment the project version.**
- Use a PATCH increment by default.
- Use a MINOR increment for a backward-compatible feature or notable user-facing enhancement.
- Use a MAJOR increment only for a breaking change.
- One commit must correspond to one version number.
- Never create a content-changing commit without a version bump.

## Files that must stay in sync

Whenever the version changes, update all visible/version-bearing references:

1. `index.html`
   - `APP_VERSION`
   - the visible footer version
   - any other hard-coded version text
2. `README.md`
   - `Versione corrente`
3. Any future metadata file that contains the project version.

Before committing, search the repository for the previous version string and make sure no stale copy remains unless intentionally documenting history.

## Commit workflow

For every requested modification:

1. Read the current version from the repository.
2. Decide PATCH / MINOR / MAJOR according to the policy above.
3. Apply the requested changes.
4. Update every version reference in the same change set.
5. Verify the site still loads and that GitHub Pages deployment files remain valid.
6. Commit with a concise message that describes the change and, when useful, the new version.

## Safety rule

Do not silently alter the dashboard's financial thresholds, interpretation rules, data sources, or warning logic unless the user explicitly asks for that change.
