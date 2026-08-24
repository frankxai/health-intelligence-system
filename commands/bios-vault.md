# /bios — synthetic contract validation only

This command surface is not approved for personal or clinical data. The reference vault is plaintext
and marked `synthetic_plaintext_prototype`; use invented test labels only.

```bash
PYTHONPATH=bios/src python -m unittest discover -s bios/tests -v
PYTHONPATH=bios/src python -m bios_substrate init \
  --household synthetic-demo --subject synthetic --path ./_local/synthetic-demo
PYTHONPATH=bios/src python -m bios_substrate validate --vault ./_local/synthetic-demo
PYTHONPATH=bios/src python -m bios_substrate packs
PYTHONPATH=bios/src python -m bios_substrate agents
PYTHONPATH=bios/src python -m bios_substrate idea-sources
```

All shipped packs and protocols are synthetic drafts and cannot start. There is no `--force` or other
override. Do not observe, import, hand off, or store real-person data in this reference implementation.
