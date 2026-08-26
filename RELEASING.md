# Releasing

Releases are created from an immutable version tag. The tag must exactly match
the version in `setup.py`.

Before the first automated PyPI release, configure a trusted publisher for the
`omnidimension` project on PyPI:

- Owner: `Omnidim`
- Repository: `omnidim-python-sdk`
- Workflow: `.github/workflows/release.yml`
- Environment: `pypi`

To release a new version:

1. Update the version in `setup.py` and merge it to `main`.
2. Create and push the matching tag, for example `0.2.20`.
3. The release workflow builds and validates the distributions, publishes the
   version to PyPI, and creates the GitHub Release with the distributions
   attached.

The workflow does not republish a version that is already on PyPI. This lets a
missing GitHub Release be reconciled safely without replacing the PyPI files.
