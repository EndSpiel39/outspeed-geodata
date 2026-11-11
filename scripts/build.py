#!/usr/bin/env python3
"""Build an Xray-compatible GeoSiteList .dat without external dependencies.

Format: v2ray routercommon GeoSiteList protobuf.
Category: OUTSPEED-DIRECT.
"""
from pathlib import Path
import re
import sys

CATEGORY = "OUTSPEED-DIRECT"
PATTERN = re.compile(r"(?=.{1,253}$)[a-z0-9](?:[a-z0-9-]*[a-z0-9])?(?:\.[a-z0-9](?:[a-z0-9-]*[a-z0-9])?)*$")


def varint(value: int) -> bytes:
    out = bytearray()
    while value > 127:
        out.append((value & 0x7F) | 0x80)
        value >>= 7
    out.append(value)
    return bytes(out)


def field_bytes(number: int, value: bytes) -> bytes:
    return varint(number << 3 | 2) + varint(len(value)) + value


def field_int(number: int, value: int) -> bytes:
    return varint(number << 3) + varint(value)


def load_domains(path: Path):
    entries = set()
    for line_no, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = raw.split("#", 1)[0].strip().lower()
        if not line:
            continue
        if ":" not in line:
            raise ValueError(f"Line {line_no}: expected domain: or full: prefix")
        kind, value = line.split(":", 1)
        if kind not in ("domain", "full") or not PATTERN.fullmatch(value):
            raise ValueError(f"Line {line_no}: invalid domain entry {line!r}")
        entries.add((kind, value))
    if not entries:
        raise ValueError("Empty domains list; refusing to publish")
    return sorted(entries)


def build(entries):
    # Domain.Type: RootDomain=2 (domain and all subdomains), Full=3.
    site = field_bytes(1, CATEGORY.encode("ascii"))
    for kind, name in entries:
        domain = field_int(1, 2 if kind == "domain" else 3)
        domain += field_bytes(2, name.encode("ascii"))
        site += field_bytes(2, domain)
    # GeoSiteList.entry = field 1.
    return field_bytes(1, site)


def main():
    root = Path(__file__).resolve().parent.parent
    entries = load_domains(root / "domains.txt")
    target = root / "dist" / "outspeed.dat"
    target.parent.mkdir(exist_ok=True)
    target.write_bytes(build(entries))
    print(f"Created {target} ({target.stat().st_size} bytes); {len(entries)} entries")


if __name__ == "__main__":
    try:
        main()
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(1)
