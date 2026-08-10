"""BIOS CLI entrypoint: python -m bios_substrate ..."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

# Allow `python -m bios_substrate` when repo root or bios/src is on PYTHONPATH
_SRC = Path(__file__).resolve().parents[1]
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from bios_substrate import __version__
from bios_substrate.handoff import build_handoff
from bios_substrate.ledger import append_event
from bios_substrate.phenotype import rebuild_phenotype
from bios_substrate.protocol_ops import list_active_runs, list_packs, load_pack, start_protocol
from bios_substrate.validate import ValidationError
from bios_substrate.vault import add_subject, init_household_vault, load_household


def _cmd_init(args: argparse.Namespace) -> int:
    path = Path(args.path)
    hh = init_household_vault(
        path,
        household_name=args.household,
        subject_label=args.subject,
        steward_label=args.steward,
        timezone_name=args.timezone,
    )
    print(json.dumps({"ok": True, "vault": str(path.resolve()), "household": hh}, indent=2))
    return 0


def _cmd_add_subject(args: argparse.Namespace) -> int:
    sub_id = add_subject(
        Path(args.vault),
        display_name=args.name,
        role=args.role,
        timezone_name=args.timezone,
    )
    print(json.dumps({"ok": True, "subject_id": sub_id}, indent=2))
    return 0


def _cmd_observe(args: argparse.Namespace) -> int:
    tags = [t for t in (args.tags or "").split(",") if t.strip()]
    metrics = None
    if args.metric:
        metrics = {}
        for item in args.metric:
            if "=" not in item:
                raise SystemExit(f"metric must be key=value, got {item}")
            k, v = item.split("=", 1)
            try:
                metrics[k] = float(v) if "." in v else int(v)
            except ValueError:
                metrics[k] = v
    event = append_event(
        Path(args.vault),
        subject=args.subject,
        kind=args.kind,
        note=args.note,
        tags=tags or None,
        metrics=metrics,
        sensitivity_class=args.sensitivity,
        channel=args.channel,
    )
    print(json.dumps(event, indent=2))
    return 0


def _cmd_packs_list(_: argparse.Namespace) -> int:
    print(json.dumps({"packs": list_packs()}, indent=2))
    return 0


def _cmd_protocol_list(args: argparse.Namespace) -> int:
    pack = load_pack(args.pack)
    rows = []
    seen = set()
    for proto in pack["protocols"].values():
        pid = proto.get("protocol_id")
        if not pid or pid in seen:
            continue
        seen.add(pid)
        rows.append(
            {
                "protocol_id": pid,
                "title": proto.get("title"),
                "class": proto.get("class"),
                "evidence_floor": proto.get("evidence_floor"),
            }
        )
    print(json.dumps({"pack": args.pack, "protocols": rows}, indent=2))
    return 0


def _cmd_protocol_start(args: argparse.Namespace) -> int:
    try:
        record = start_protocol(
            Path(args.vault),
            subject=args.subject,
            pack_id=args.pack,
            protocol_key=args.id,
            force=args.force,
        )
    except ValidationError as exc:
        print(str(exc), file=sys.stderr)
        return 2
    print(json.dumps({"ok": True, "run": record}, indent=2, default=str))
    return 0


def _cmd_protocol_active(args: argparse.Namespace) -> int:
    runs = list_active_runs(Path(args.vault), args.subject)
    print(json.dumps({"active": runs}, indent=2, default=str))
    return 0


def _cmd_phenotype(args: argparse.Namespace) -> int:
    ph = rebuild_phenotype(Path(args.vault), args.subject)
    print(json.dumps(ph, indent=2))
    return 0


def _cmd_handoff(args: argparse.Namespace) -> int:
    text = build_handoff(Path(args.vault), args.subject)
    if args.out:
        Path(args.out).write_text(text, encoding="utf-8")
        print(f"wrote {args.out}")
    else:
        print(text)
    return 0


def _cmd_validate(args: argparse.Namespace) -> int:
    vault = Path(args.vault)
    hh = load_household(vault)
    errors: list[str] = []
    packs_ok = []
    for pack_id in list_packs():
        try:
            load_pack(pack_id)
            packs_ok.append(pack_id)
        except Exception as exc:  # noqa: BLE001 — surface pack errors
            errors.append(f"pack {pack_id}: {exc}")
    for sub in hh["subjects"]:
        sdir = vault / "subjects" / sub["subject_id"]
        if not (sdir / "ledger.jsonl").exists():
            errors.append(f"missing ledger for {sub['subject_id']}")
        if not (sdir / "egress.json").exists():
            errors.append(f"missing egress for {sub['subject_id']}")
    result = {
        "ok": not errors,
        "household_id": hh["household_id"],
        "subjects": [s["subject_id"] for s in hh["subjects"]],
        "packs_validated": packs_ok,
        "errors": errors,
        "version": __version__,
    }
    print(json.dumps(result, indent=2))
    return 0 if result["ok"] else 1


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="bios_substrate",
        description="BIOS substrate reference CLI (module: bios_substrate)",
    )
    p.add_argument("--version", action="version", version=f"bios_substrate {__version__}")
    sub = p.add_subparsers(dest="command", required=True)

    init = sub.add_parser("init", help="Create a household vault")
    init.add_argument("--household", required=True)
    init.add_argument("--subject", default="self")
    init.add_argument("--steward", default="steward")
    init.add_argument("--path", required=True)
    init.add_argument("--timezone", default="UTC")
    init.set_defaults(func=_cmd_init)

    add = sub.add_parser("add-subject", help="Add a dependent subject (steward model)")
    add.add_argument("--vault", required=True)
    add.add_argument("--name", required=True)
    add.add_argument("--role", default="dependent")
    add.add_argument("--timezone", default="UTC")
    add.set_defaults(func=_cmd_add_subject)

    obs = sub.add_parser("observe", help="Append a ledger event")
    obs.add_argument("--vault", required=True)
    obs.add_argument("--subject", default="self")
    obs.add_argument("--kind", required=True)
    obs.add_argument("--note", default=None)
    obs.add_argument("--tags", default="")
    obs.add_argument("--metric", action="append", default=[])
    obs.add_argument("--sensitivity", default="personal")
    obs.add_argument("--channel", default="human")
    obs.set_defaults(func=_cmd_observe)

    packs = sub.add_parser("packs", help="List domain packs")
    packs.set_defaults(func=_cmd_packs_list)

    pl = sub.add_parser("protocol-list", help="List protocols in a pack")
    pl.add_argument("--pack", required=True)
    pl.set_defaults(func=_cmd_protocol_list)

    ps = sub.add_parser("protocol", help="Protocol run commands")
    ps_sub = ps.add_subparsers(dest="protocol_cmd", required=True)
    start = ps_sub.add_parser("start", help="Start a pack protocol for a subject")
    start.add_argument("--vault", required=True)
    start.add_argument("--subject", default="self")
    start.add_argument("--pack", required=True)
    start.add_argument("--id", required=True, help="protocol id or short key")
    start.add_argument(
        "--force",
        action="store_true",
        help="Override soft gate after human review (still blocks hard jurisdiction locks)",
    )
    start.set_defaults(func=_cmd_protocol_start)

    active = ps_sub.add_parser("active", help="List active protocol runs")
    active.add_argument("--vault", required=True)
    active.add_argument("--subject", default="self")
    active.set_defaults(func=_cmd_protocol_active)

    ph = sub.add_parser("phenotype", help="Phenotype projection")
    ph_sub = ph.add_subparsers(dest="ph_cmd", required=True)
    reb = ph_sub.add_parser("rebuild", help="Rebuild phenotype from ledger")
    reb.add_argument("--vault", required=True)
    reb.add_argument("--subject", default="self")
    reb.set_defaults(func=_cmd_phenotype)

    ho = sub.add_parser("handoff", help="Generate clinician handoff markdown")
    ho.add_argument("--vault", required=True)
    ho.add_argument("--subject", default="self")
    ho.add_argument("--out", default=None)
    ho.set_defaults(func=_cmd_handoff)

    val = sub.add_parser("validate", help="Validate vault + installed packs")
    val.add_argument("--vault", required=True)
    val.set_defaults(func=_cmd_validate)

    return p


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return int(args.func(args))
    except (FileNotFoundError, KeyError, ValidationError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
