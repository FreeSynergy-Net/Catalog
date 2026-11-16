# Changelog

## Unreleased (unreviewed/catalog-zentinel)

- `capabilities_ref` is `v0.0.21` (packages.toml, default in `scripts/catalog_check.py`, docs, example, test fixture). fs-interfaces v0.0.21 names
  `gateway.reverse-proxy`, `messages.matrix`, `messages.matrix.oidc-server` (all `planned`), so the `zentinel` entry now passes the real check.
- The test filter that hid the `gateway.reverse-proxy` error for `zentinel` is removed.
