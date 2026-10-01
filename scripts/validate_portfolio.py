#!/usr/bin/env python3
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ALLOWED_SUFFIXES = {".md", ".svg", ".json", ".py", ".yml", ".yaml"}
FORBIDDEN_NAMES = {".env", ".npmrc", ".pypirc", "id_rsa", "id_ed25519"}
FORBIDDEN_SUFFIXES = {".pem", ".key", ".p12", ".pfx", ".sqlite", ".sqlite3", ".db"}

PATTERNS = {
    "private key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "AWS access key": re.compile(r"AKIA[0-9A-Z]{16}"),
    "GitHub token": re.compile(r"gh[pousr]_[A-Za-z0-9_]{20,}"),
    "Slack token": re.compile(r"xox[baprs]-[A-Za-z0-9-]{10,}"),
    "credential assignment": re.compile(r"(?i)(?:api[_-]?key|client[_-]?secret|access[_-]?token|password)\\s*[:=]\\s*['\"][^'\"]{8,}['\"]"),
    "private IPv4 URL": re.compile(r"https?://(?:10\\.|192\\.168\\.|172\\.(?:1[6-9]|2[0-9]|3[01])\\.)"),
}

def tracked_files():
    for path in ROOT.rglob("*"):
        if not path.is_file() or ".git" in path.parts:
            continue
        yield path

def fail(message):
    print(f"::error::{message}")
    return 1

def main():
    errors = 0
    for path in tracked_files():
        rel = path.relative_to(ROOT)
        if path.name in FORBIDDEN_NAMES or path.suffix.lower() in FORBIDDEN_SUFFIXES:
            errors += fail(f"Forbidden sensitive file type/name: {rel}")
            continue
        if path.suffix.lower() not in ALLOWED_SUFFIXES:
            errors += fail(f"Unexpected file type in public profile repository: {rel}")
            continue
        if path.stat().st_size > 1_500_000:
            errors += fail(f"Unexpectedly large public portfolio file: {rel}")
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            errors += fail(f"Non-text file detected: {rel}")
            continue
        for label, pattern in PATTERNS.items():
            if pattern.search(text):
                errors += fail(f"Potential {label} detected in {rel}")

    manifest_path = ROOT / "data" / "projects.json"
    if manifest_path.exists():
        data = json.loads(manifest_path.read_text(encoding="utf-8"))
        if data.get("schema_version") != 1:
            errors += fail("Unsupported projects manifest schema_version")
        ids = set()
        for project in data.get("projects", []):
            pid = project.get("id")
            if not pid or pid in ids:
                errors += fail(f"Invalid or duplicate project id: {pid}")
            ids.add(pid)
            case = ROOT / project.get("case_study", "")
            if not case.is_file():
                errors += fail(f"Missing case study for {pid}: {case.relative_to(ROOT)}")

    if errors:
        print(f"Portfolio guard failed with {errors} issue(s).")
        return 1
    print("Portfolio guard passed.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
