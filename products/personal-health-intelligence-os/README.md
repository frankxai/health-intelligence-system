# Personal Health Intelligence OS

An owned daily health workspace with native Google and Notion editions, portable agent instructions, source provenance and a partner installation process.

Version 0.1.0 is a Stage 1 release candidate. Native templates are implemented in the connected workspaces. Public duplication, checkout, cross-account installation and provider revocation acceptance remain release gates. Complete Edition synchronization is designed and reference-tested, not installed. The offline web cockpit is a synthetic demonstration and does not sync with native workspaces.

## Start

- [Installation](docs/INSTALL.md)
- [Product specification](canonical/spec.json)
- [Field dictionary](docs/DATA_DICTIONARY.md)
- [Portable agent pack](agents/README.md)
- [Partner delivery](docs/PARTNER_DELIVERY.md)
- [Interactive synthetic cockpit](web/index.html)
- [Draft product page](web/product.html)
- [Release receipt](docs/RELEASE_RECEIPT.md)

## Build and verify

Use an environment with the dependencies listed in requirements-product.txt. This pack does not install credentials or send data anywhere.

```bash
python3 scripts/validate.py synthetic/demo.json
python3 scripts/validate.py synthetic/blank.json
python3 -m unittest discover -s tests -v
python3 scripts/build_adapters.py
python3 scripts/build_notion_rows.py
node web/build-demo.mjs
node design/verify-demo-core.mjs
```

Workbook authoring uses the Codex primary runtime's @oai/artifact-tool. Run scripts/build_workbook.mjs from an ephemeral directory linked to that runtime, with HEALTH_OS_ROOT pointing to this directory. Its local XLSX must be imported as native Google Sheets. Native post-import verification and repair are required: the initial conversion in this build dropped OOXML date values and chart series. The repair contract is recorded in the release receipt; a local screenshot is not proof of native behavior.

The product specification generates platform schemas, CSV templates and synthetic demo content. Native workbook headers are human-readable; packaged CSV headers use canonical field names. Nested record arrays use JSON cells in Stage 1. These adapters provide mappings and provisioning payloads; they are not unattended import or synchronization services.

## Rights and maintenance

This pack extends the existing Health Intelligence System repository. The parent MIT license applies to the public source. Customers pay for maintained curation, installation, delivery assets and support, not removal of their rights in the public core. No third-party media or proprietary food database is bundled. Native platform accounts and optional AI subscriptions belong to the customer.

Maintenance owner: product maintainer. Recheck platform documentation and installation receipts before each release. Do not accept real health records in public issues or git history.
