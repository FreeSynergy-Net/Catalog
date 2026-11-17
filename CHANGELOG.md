# Changelog

## Unreleased (unreviewed/catalog-packages-0020)

- `fs-packages` tag `v0.0.19` -> `v0.0.20` (asset `fs-packages-0.0.20-linux-x86_64.tar.gz`; other fields unchanged).

## Unreleased (unreviewed/catalog-forms-resources)

- New entry `fs-forms` (`FreeSynergy.Forms`, tag `v0.0.2`, asset `fs-forms-0.0.2-linux-x86_64.tar.gz`, schema 1, no icon and no `provides` yet, "Contract: draft"; the tarball holds `fs-forms` and `fs-forms-simple`).
- New entry `fs-resources` (`FreeSynergy.Resources`, tag `v0.0.2`, asset `fs-resources-0.0.2-linux-x86_64.tar.gz`, schema 1, no icon and no `provides` yet, "Contract: draft"; the tarball holds `fs-resources` and `fs-resources-simple`).

## Unreleased (unreviewed/catalog-draw-messages-packages)

- `fs-packages` tag `v0.0.18` -> `v0.0.19` (pre-release; asset `fs-packages-0.0.19-linux-x86_64.tar.gz`; other fields unchanged).
- New entry `fs-draw` (`FreeSynergy.Draw`, tag `v0.0.2`, asset `fs-draw-0.0.2-linux-x86_64.tar.gz`, schema 1, no icon and no `provides` yet, "Contract: draft").
- New entry `fs-messages` (`FreeSynergy.Messages`, tag `v0.0.3`, asset `fs-messages-0.0.3-linux-x86_64.tar.gz`, schema 1, no icon and no `provides` yet, "Contract: draft").

## Unreleased (unreviewed/catalog-make-icons-weg)

- Removed `icons/make_icons.py`; icons come from the fs-icons set (it would have overwritten `server.png` with the old CC0 drawing). `icons/README.md` shortened accordingly.

## Unreleased (unreviewed/catalog-groups-texts)

- New entry `fs-groups` (`FreeSynergy.Groups`, tag `v0.0.2`, asset `fs-groups-0.0.2-linux-x86_64.tar.gz`, schema 1, no icon yet).
- New entry `fs-texts` (`FreeSynergy.Texts`, tag `v0.0.13`, asset `fs-texts-0.0.13-linux-x86_64.tar.gz`, binary `fs-texts`, ADR 0087).
- Removed the `fs-wiki` entry (renamed fs-texts, ADR 0087); an installed fs-wiki stays installed and keeps its data folder `wiki`; the switch to fs-texts comes with `replaces` in fs-packages 0.0.19.

## Unreleased (unreviewed/catalog-zentinel)

- `fs-people` tag `v0.0.3` -> `v0.0.14` (pre-release; asset `fs-people-0.0.14-linux-x86_64.tar.gz`); description unchanged.
- New entry `zentinel` (`kind = "server"`, upstream Zentinel `26.11_2`, tag `v26.11_2`): tar.gz and debs for amd64/arm64 with signature and SHA-256,
  `provides gateway.reverse-proxy`, `schema = 2` for this package only. The 7 existing programs are unchanged.
- Wrapper tags (variant B): `v<upstream version>` for the first build, `v<upstream version>-fs<N>` (N >= 2) for further builds of our packaging. A package
  with `upstream` takes only wrapper tags, one without only `vMAJOR.MINOR.PATCH`. `tag_key` orders like rpm/dpkg (`~` < word/pre-release < end < number,
  `+build` ignored); `bump_catalog.py` never goes back from a final version to a pre-release and never mixes the two families.
- Hardening of the tag pattern: ASCII digits only (`[0-9]`, not `\d`) and `\Z` instead of `$` (a trailing newline is refused); only lower-case `-fs` is a suffix.
- Rule for `server`: offered only when the release has a signed rpm or deb (ADR 0077 section 3); otherwise skipped.
- `schema = 2` can be set per package inside `[[package]]`; the file stays at `schema = 1` for the older entries.
- Neutral server icon `icons/server.png` (MIT, own drawing of the FreeSynergy project from the fs-icons set, see `icons/README.md`; replaces the earlier CC0 icon); the icon address points to `main`, so the file exists only after the merge. 21 further programme and kind icons added to `icons/` (not referenced by an entry yet).
- Docs: `docs/format.md` and `docs/format.de.md` describe the wrapper rule, ordering, per-package schema and the server rule.
- Tests: tag table with pre-release ordering, bump test, hardening (ASCII digits, `\Z`, `v1.0-Fs2`), generator and validation tests for `zentinel`.

- `capabilities_ref` is `v0.0.21` (packages.toml, default in `scripts/catalog_check.py`, docs, example, test fixture). fs-interfaces v0.0.21 names
  `gateway.reverse-proxy`, `messages.matrix`, `messages.matrix.oidc-server` (all `planned`), so the `zentinel` entry now passes the real check.
- The test filter that hid the `gateway.reverse-proxy` error for `zentinel` is removed.
