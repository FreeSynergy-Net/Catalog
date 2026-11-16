# Changelog

## Unreleased (unreviewed/catalog-zentinel)

- New entry `zentinel` (`kind = "server"`, upstream Zentinel `26.11_2`, tag `v26.11_2`): tar.gz and debs for amd64/arm64 with signature and SHA-256,
  `provides gateway.reverse-proxy`, `schema = 2` for this package only. The 7 existing programs are unchanged.
- Wrapper tags (variant B): `v<upstream version>` for the first build, `v<upstream version>-fs<N>` (N >= 2) for further builds of our packaging. A package
  with `upstream` takes only wrapper tags, one without only `vMAJOR.MINOR.PATCH`. `tag_key` orders like rpm/dpkg (`~` < word/pre-release < end < number,
  `+build` ignored); `bump_catalog.py` never goes back from a final version to a pre-release and never mixes the two families.
- Hardening of the tag pattern: ASCII digits only (`[0-9]`, not `\d`) and `\Z` instead of `$` (a trailing newline is refused); only lower-case `-fs` is a suffix.
- Rule for `server`: offered only when the release has a signed rpm or deb (ADR 0077 section 3); otherwise skipped.
- `schema = 2` can be set per package inside `[[package]]`; the file stays at `schema = 1` for the older entries.
- New neutral server icon `icons/server.png` (CC0, made by `icons/make_icons.py`); the icon address points to `main`, so the file exists only after the merge.
- Docs: `docs/format.md` and `docs/format.de.md` describe the wrapper rule, ordering, per-package schema and the server rule.
- Tests: tag table with pre-release ordering, bump test, hardening (ASCII digits, `\Z`, `v1.0-Fs2`), generator and validation tests for `zentinel`.

- `capabilities_ref` is `v0.0.21` (packages.toml, default in `scripts/catalog_check.py`, docs, example, test fixture). fs-interfaces v0.0.21 names
  `gateway.reverse-proxy`, `messages.matrix`, `messages.matrix.oidc-server` (all `planned`), so the `zentinel` entry now passes the real check.
- The test filter that hid the `gateway.reverse-proxy` error for `zentinel` is removed.
