# Catalog format 2: reference (EN) · [Deutsch](format.de.md)

`packages.toml` says what is offered; `python3 scripts/gen_catalog.py` reads the public releases and writes `catalog.xml`
(AppStream collection metadata, signed by CI). Format 2 adds the information the store shows per package. Every new field is
optional for the reader: an old entry stays valid and the store shows "unknown" for what it does not say.

Check without network (and without writing): `python3 -I scripts/gen_catalog.py --check [packages.toml] [--capabilities FILE] [--retired FILE]`.
Every finding is reported at once as `<package>: <field>: <message>`; errors stop the run, warnings do not.

## File level
| Key | Meaning |
|---|---|
| `schema` | `1` (default) or `2`. With `2` the rules marked "format 2" below are **errors**; with `1` they are warnings, so the weekly signing never stops for an old entry. The catalog gets `fs-schema="2"` on `<components>`. |
| `capabilities_ref` | Tag (form `vX.Y.Z`, checked) of `fs-interfaces` whose `schema/capabilities.txt` is THE capability list (default `v0.0.21`). Read with `gh api`; never copied into this repo. `--capabilities FILE` / `$FS_CAPABILITIES_FILE` use a local file (offline). |

## Per package (`[[package]]`)
Write sub-tables (`[package.x]`, `[[package.x]]`) **after** the plain keys of the package: `bump_catalog.py` edits `tag` by text.

| Key | XML | Rule |
|---|---|---|
| `id`, `name`, `summary`, `repo`, `tag`, `asset` | as before | required; `id` lower-case; `tag` `vMAJOR.MINOR.PATCH` (wrapper: `v<upstream>[-fs<N>]`, see below) |
| `kind` | `fs:kind`, component `type` | `program` (default), `frontend`, `component`, `theme`, `server`, `icon-theme`. AppStream type: program and frontend `desktop-application`, component and theme `addon`, server `service`, icon-theme `icon-theme`. `server` and `icon-theme` are new. Today's stores (before 0.0.13) **drop** such an entry ("unknown fs:kind", listed as skipped; the catalog and the other packages stay fine); a locked "not supported by this store version" offer is shown only by stores from 0.0.13 on (the reader fix is in progress). So they are written only with `schema = 2` AND `min_store`, and go into the REAL catalog only AFTER a store with the fixed reader is released. |
| `description` | `<description>` | text, or a table `{ en = "..", de = ".." }` (variants of ONE description, `xml:lang`; `en` required, written first). Blank line = new paragraph. Format 2: required (it is the fallback of the store). |
| `icon`, `icon_sha256` | `<icon type="remote" fs-sha256>` | https address of a **PNG of at most 1 MiB** (SVG is refused, as in the store). The generator downloads it, checks the PNG signature, writes its SHA-256 (and compares with `icon_sha256` when given). Format 2: **required for every package**. |
| `provides`, `requires`, `recommends` | `fs:provides` ... | list of capabilities `"name"` or `"name major.minor"` (also `name>=1.2`). Names ONLY from `capabilities.txt` of fs-interfaces; unknown name = error with a "did you mean". A `planned` name is a warning. No level = any. Kept apart from rights. |
| `[[package.feature]]` | `fs:features`, `fs:feature.<key>.provides/requires/recommends/name` | a feature: `key` (required), `name`, and its own `provides`/`requires`/`recommends`. May stay empty (`key` only). |
| `mediatypes` | `<provides><mediatype>` | list like `["text/calendar"]` (as AppStream). |
| `installed_size` | `<size type="installed">` | table `{ "0.0.7" = bytes }`; only the entry of the offered version is written (the tag moves by itself, the number must not go stale). |
| (from GitHub) | `<size type="download">` | size of the release file, taken from the release; also on rpm/deb/exe files. |
| `[[package.history]]` | `<release version date><description xml:lang>` | per release: `version`, `changes` (text or language table, `en` required), `date` `YYYY-MM-DD` (required for older releases). The entry of the offered version is the text of the current release (its date comes from GitHub). Older ones become releases without files (change list only). No entry for the current version = a warning (never an error: `bump` raises tags alone). |
| `upstream` | `fs:upstream` | https address where the maker publishes it (mirror source). |
| `upstream_signature` | `fs:upstream-signature` | maker's signature: key fingerprint (hex) or https address; needs `upstream`. |
| `source_code` | `fs:source-code` | https address of the source code of this version. Format 2: required when `upstream` is set (ADR 0068, mirrored with the package). |
| `maker` | `fs:maker` | name of the maker. |
| `[package.description_wiki]` | `fs:description-wiki` (block id), `-source-rev`, optional `-lang` | ADR 0072, Nutzerentscheid: DE/EN are ONE page with language variants, so ONE block id (UUIDv7) and the variants live inside the block. `block`, `source_rev` (number, required: the rev this entry was made from, so the store can tell the wiki moved on), `lang` optional (only a wish for reading, never a second block). No `translationOf`, no block per language. The text description stays the fallback. |
| `min_store` | `fs:min-store` | first fs-packages version that reads this entry, `MAJOR.MINOR.PATCH`. It protects only from store 0.0.13 on: older stores ignore `fs:min-store` for kinds they know (program, ...); for unknown kinds they just leave the entry out (skipped), they do not fail. **Required for `server` and `icon-theme`**, which are written only with `schema = 2`. |
| `replaces` | `<replaces><id>` | list of old ids this package takes over from (a renamed program), e.g. `["fs-wiki"]` (ADR 0080). Only with `schema = 2`. Each id once, not the package's own id, and **not also an entry of its own** (the old entry leaves the catalog); one old id has only one new entry. The store then shows the new entry as an update of the installed old one. With `--retired FILE` (`scripts/retired-names.txt` of fs-release) an id that is not on the list is a warning, and an entry whose id is on the list (given up, never given out again) is an error. |
| `[[package.screenshot]]` | `<screenshots><screenshot><image type="source" fs-sha256 fs-license fs-source><caption xml:lang>` | `url` https, `license` clear (SPDX id; `unknown`, `none`, `proprietary`, `all rights reserved` and odd characters are refused: **no clear licence, no picture**), `source` (address or maker), `caption` (text or language table), `sha256` optional (downloaded and compared; the computed hash is written). PNG, JPEG or WebP, at most 5 MiB. The first picture is the default. |

Per kind (format 2): `program` and `server` must have `provides`; `frontend` must have `requires`; `theme`, `icon-theme`, `component` need nothing extra.

## Wrapper: `v<upstream version>` and `-fs<N>`
`vMAJOR.MINOR.PATCH` is the tag of our **own** programs (ADR 0064). A package that wraps a **foreign** program (a mirror, ADR 0068; so far `kind = "server"`,
but the rule does not depend on the kind) takes the upstream version **unchanged** into its tag and must name `upstream` (that is how the generator
tells it from an own program):
- first build of an upstream version: `v<upstream version>`, e.g. `v26.11_2` (upstream Zentinel `26.11_2`), `v1.12.1` (upstream Kanidm `1.12.1`);
- every further build of OUR packaging of the same upstream version: `v<upstream version>-fs<N>` with N >= 2, e.g. `v26.11_2-fs2`, `v1.12.1-fs2`.
  `-fs1` does not exist (build 1 has no suffix); `N` has no leading zero. A new upstream version starts again without suffix.

The upstream part may use any of `.`, `_`, `-`, `+`, `~`, ASCII letters and ASCII digits 0-9 (it starts with a digit and ends with a letter or digit) and is never changed or
split, so the rule is the same for every upstream. `-fs` appears in no upstream version we know; an upstream version that contains `-fs` is **refused**
(the rule would no longer be unambiguous), so is a second `-fs` suffix. Only the lower-case `-fs` forms the suffix: `v1.0-Fs2` is build 1 of the
upstream version `1.0-Fs2`. A trailing newline is refused. The catalog version is the tag without `v` (`26.11_2-fs2`).
Package files keep the native revision of their format (`zentinel_26.11.2-1_amd64.deb`). `min_store` and `schema` keep the plain `MAJOR.MINOR.PATCH`.
Existing tags are not renamed. Order (bump, history), as in rpm/dpkg: by upstream version first, then by `N`. Numbers compare numerically left to right, `_` like `.`
(`26.11_3` after `26.11_2`, `26.11_3` before `27.0`); a word (rc, alpha, beta, any letters) before the end of the version is a pre-release marker and sorts
**before** the same version without it: `1.0~rc1` < `1.0-rc1` < `1.0` < `1.0.1`, `rc1` < `rc2` < `rc10`, `alpha` < `beta` < `rc` (words compare
case-insensitively); `~` sorts before everything, also before the end; a `+build` part is ignored. Price: `1.1.1a` < `1.1.1` (OpenSSL spelling). So bump never
goes from a final version back to a pre-release. If an upstream changes its scheme, bump does not take the new version; a person sets that tag. A package with `upstream` takes only wrapper tags, one without only `vMAJOR.MINOR.PATCH`; the families are never mixed.

A package may ask for format 2 alone: `schema = 2` inside its `[[package]]` table makes the format-2 rules errors for that package only, while the
file stays at `schema = 1` for the older entries. A `server` is offered only when its release has a signed rpm or deb (ADR 0077 section 3); the generator skips it otherwise.
The neutral server icon is `icons/server.png` (MIT, own drawing of the FreeSynergy project, from the fs-icons set; see `icons/README.md`).

## Downloads and failures
Icons and pictures are fetched over https only (also after redirects, `--proto =https --proto-redir =https`, at most 3 redirects), with a size limit; the FIRST host is refused when it resolves to a loopback or private address (a redirect, at most 3 and https only, or DNS rebinding between that check and the download is **not** covered: the generator runs on a GitHub runner with no internal services and reads only public pictures); the file type is checked by its first bytes (WebP only with `WEBP` at offset 8; no SVG, no XML). A **failed download never stops bump or sign**: the package is skipped with a warning and the entry of the last signed catalog is kept. A wrong file (not a picture, hash differs, too large) is an error. Under `schema = 1` wrong capability names are only warnings, and the list is read from GitHub only when a package names a capability (if it cannot be read: a warning).

## What the store reads (see `fs_store_catalog::Details`)
`<size type="download">` of the artifact, `<release date>`, the first `<description>` of the release (English), `fs:provides/requires/recommends`
(comma list, `name major.minor`), `fs:upstream*`, `fs:source-code`, `fs:description-wiki` (the whole value is the block id), `<icon>`, `<screenshot>`
(https + `fs-sha256` + clear `fs-license`, else withheld). Not yet read by the store (see CHANGES-FOR-STORE.md): `xml:lang` choice, `<size type="installed">`,
`fs:maker`, `fs-source`, `fs:feature.*`, `<provides><mediatype>`, `fs:description-wiki-source-rev`/`-lang`, kinds `server`/`icon-theme`.

## Examples and tests
`examples/packages.example.toml` shows every field; `examples/catalog.example.xml` is what the generator makes from it (offline, checked by the tests);
`examples/make_images.py` makes the pictures (generated for this repo, CC0-1.0). Tests: `python3 -I -m unittest discover -s tests`.
Refresh the golden file after a change on purpose: `python3 -I tests/support.py --write-golden`.
