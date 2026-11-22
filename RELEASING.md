# Releasing

Do not edit the version in `setup.py` or `CHANGELOG.md` by hand. release-please
writes both from pull request titles.

1. Give each pull request a conventional commit title. Pull requests are
   squash-merged, so the title becomes the changelog line. `feat:` lands under
   Added, `fix:` under Fixed, and `perf:` under Changed. `ci`, `test`, `build`,
   `docs` and `chore` stay out of the changelog. The `pr-title` check rejects
   other formats.
2. After each merge to `main`, release-please updates one open release pull
   request, `chore(main): release X.Y.Z`, with the next version and changelog.
3. A member of the maintainers team approves and merges the release pull request. The
   `release.yml` run on that merge tags `X.Y.Z` (no `v`), builds and checks the
   distributions, publishes them to PyPI, and attaches them to the GitHub
   Release.

PyPI trusts `release.yml` in the `pypi` environment of `Omnidim/omnidim-python-sdk`,
so there is no PyPI token. The workflow skips a version that is already on PyPI.
To attach missing files to an existing release, use **Run workflow** with that tag.
