#!/usr/bin/env python3
"""HBI v1.0 conformance validator — reference implementation."""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path

SPEC_VERSION = "1.0"
VALIDATOR_VERSION = "1.0.1"

REQUIRED_FILES = ("MANIFEST.json", "IDEA.md", "HANDOFF.md", "IP_TRIAGE.json", "DISCLOSURE.json")
HANDOFF_DOC_TYPES = frozenset({"HANDOFF", "INSTIGATE"})
HANDOFF_TYPE_MAP = {"HANDOFF": "discuss", "INSTIGATE": "execute"}
ID_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*-\d{4}-\d{2}$")
STAGES = frozenset({"inbox", "half-baked", "packaged", "shipped", "parked"})
IP_STATUSES = frozenset({
    "untriaged",
    "not-patentable",
    "defensive-publication",
    "consider-provisional",
})


def _iso_ok(value: str) -> bool:
    if not isinstance(value, str) or not value:
        return False
    try:
        datetime.fromisoformat(value.replace("Z", "+00:00"))
        return True
    except ValueError:
        return False


def validate_package(path: Path) -> dict:
    errors: list[str] = []
    warnings: list[str] = []

    if not path.is_dir():
        return {"conformant": False, "errors": [f"Not a directory: {path}"], "warnings": []}

    for name in REQUIRED_FILES:
        if not (path / name).is_file():
            errors.append(f"Missing required file: {name}")

    manifest = {}
    manifest_path = path / "MANIFEST.json"
    if manifest_path.is_file():
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"MANIFEST.json invalid: {exc}")
            manifest = {}

    if manifest:
        for field in ("spec_version", "id", "title", "stage", "ip_status", "created", "updated", "author"):
            if field not in manifest or manifest[field] in (None, ""):
                errors.append(f"MANIFEST missing or empty field: {field}")

        if manifest.get("spec_version") != SPEC_VERSION:
            errors.append(f"MANIFEST.spec_version must be '{SPEC_VERSION}'")

        pkg_id = manifest.get("id", "")
        if pkg_id and not ID_RE.match(pkg_id):
            errors.append(f"MANIFEST.id invalid format: {pkg_id}")

        stage = manifest.get("stage")
        if stage and stage not in STAGES:
            errors.append(f"MANIFEST.stage invalid: {stage}")

        ip_status = manifest.get("ip_status")
        if ip_status and ip_status not in IP_STATUSES:
            errors.append(f"MANIFEST.ip_status invalid: {ip_status}")

        for ts_field in ("created", "updated"):
            if manifest.get(ts_field) and not _iso_ok(manifest[ts_field]):
                errors.append(f"MANIFEST.{ts_field} not valid ISO 8601")

    handoff_path = path / "HANDOFF.md"
    handoff_doc_type = ""
    if handoff_path.is_file():
        try:
            handoff = handoff_path.read_text(encoding="utf-8")
        except OSError as exc:
            errors.append(f"HANDOFF.md unreadable: {exc}")
            handoff = ""
        first_line = next((ln.strip() for ln in handoff.splitlines() if ln.strip()), "")
        if not first_line:
            errors.append("HANDOFF.md is empty")
        elif first_line.upper() not in HANDOFF_DOC_TYPES:
            errors.append(f"HANDOFF.md first line must be HANDOFF or INSTIGATE, got: {first_line!r}")
        else:
            handoff_doc_type = first_line.upper()
            rest = handoff.splitlines()
            idx = next(i for i, ln in enumerate(rest) if ln.strip() == first_line)
            body = "\n".join(ln for ln in rest[idx + 1 :] if ln.strip()).strip()
            if not body:
                errors.append("HANDOFF.md must contain directions after the doc-type line")

    idea_path = path / "IDEA.md"
    if idea_path.is_file():
        try:
            idea = idea_path.read_text(encoding="utf-8")
        except OSError as exc:
            errors.append(f"IDEA.md unreadable: {exc}")
            idea = ""
        if not idea.strip():
            errors.append("IDEA.md is empty")
        elif not idea.lstrip().startswith("#"):
            errors.append("IDEA.md must begin with a level-1 heading")
        else:
            for section in ("## Problem", "## Approach"):
                if section not in idea:
                    warnings.append(f"IDEA.md missing recommended section: {section}")

    triage = {}
    triage_path = path / "IP_TRIAGE.json"
    if triage_path.is_file():
        try:
            triage = json.loads(triage_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"IP_TRIAGE.json invalid: {exc}")

    if triage:
        if triage.get("advisory") is not True:
            errors.append("IP_TRIAGE.advisory must be true")
        if not triage.get("rationale"):
            errors.append("IP_TRIAGE.rationale is required")
        if triage.get("status") != manifest.get("ip_status"):
            errors.append("IP_TRIAGE.status must match MANIFEST.ip_status")
        if triage.get("status") and triage["status"] not in IP_STATUSES:
            errors.append(f"IP_TRIAGE.status invalid: {triage['status']}")

    disclosure = {}
    disclosure_path = path / "DISCLOSURE.json"
    if disclosure_path.is_file():
        try:
            disclosure = json.loads(disclosure_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"DISCLOSURE.json invalid: {exc}")

    if disclosure:
        if disclosure.get("gate") != "disclosure":
            errors.append('DISCLOSURE.gate must be "disclosure"')
        status = disclosure.get("status")
        allowed = disclosure.get("distribution_allowed")
        if status == "closed" and allowed is not False:
            errors.append("DISCLOSURE.distribution_allowed must be false when status is closed")
        if status == "approved":
            if allowed is not True:
                errors.append("DISCLOSURE.distribution_allowed must be true when status is approved")
            for field in ("approved_at", "approved_by", "scope"):
                if not disclosure.get(field):
                    errors.append(f"DISCLOSURE missing required field when approved: {field}")

    if manifest and handoff_doc_type:
        expected = HANDOFF_TYPE_MAP[handoff_doc_type]
        actual = manifest.get("handoff_type")
        if actual and actual != expected:
            errors.append(
                f"MANIFEST.handoff_type must be {expected!r} for doc type {handoff_doc_type}, got {actual!r}"
            )

    if manifest.get("stage") == "shipped":
        if disclosure.get("status") != "approved" or disclosure.get("distribution_allowed") is not True:
            errors.append("shipped stage requires approved disclosure with distribution_allowed true")

    if not (path / "CHANGELOG.md").is_file():
        warnings.append("CHANGELOG.md recommended but missing")

    return {
        "conformant": len(errors) == 0,
        "package": str(path),
        "id": manifest.get("id"),
        "stage": manifest.get("stage"),
        "spec_version": SPEC_VERSION,
        "validator_version": VALIDATOR_VERSION,
        "errors": errors,
        "warnings": warnings,
    }


def main() -> int:
    p = argparse.ArgumentParser(description="Validate an HBI v1.0 package")
    p.add_argument("path", type=Path, help="Path to package directory")
    p.add_argument("--json", action="store_true", help="Emit JSON report")
    args = p.parse_args()

    report = validate_package(args.path.resolve())
    if args.json:
        print(json.dumps(report, indent=2))
    else:
        status = "PASS" if report["conformant"] else "FAIL"
        print(f"{status}: {report['package']}")
        for err in report["errors"]:
            print(f"  ERROR: {err}")
        for warn in report["warnings"]:
            print(f"  WARN: {warn}")

    return 0 if report["conformant"] else 1


if __name__ == "__main__":
    sys.exit(main())