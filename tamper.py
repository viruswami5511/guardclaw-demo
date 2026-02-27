#!/usr/bin/env python3
"""
guardclaw-demo / tamper.py

Simulates an insider attack: edits entry #2 in the ledger
to hide an unauthorized API call. No re-signing possible
without the private key.

Usage:
    python tamper.py
"""

import json
from pathlib import Path

LEDGER_PATH = Path("demo_ledger.jsonl")
TARGET_SEQ  = 2   # entry #2 — the external API call


def main():
    print()
    print("=" * 60)
    print("  GuardClaw Demo  —  Simulating Tamper Attack")
    print("=" * 60)
    print()

    if not LEDGER_PATH.exists():
        print("  ERROR: demo_ledger.jsonl not found.")
        print("  Run:   python run_demo.py  first.")
        print()
        return

    lines = LEDGER_PATH.read_text(encoding="utf-8").splitlines()
    entry = json.loads(lines[TARGET_SEQ])

    print(f"  Target entry   : sequence #{TARGET_SEQ}")
    print(f"  Original payload:")
    for k, v in entry["payload"].items():
        print(f"    {k}: {v}")

    # ── Attacker modifies the payload to hide evidence ────────
    entry["payload"]["endpoint"] = "https://legitimate-api.internal/safe"
    entry["payload"]["result"]   = "low_risk_cleared"

    print()
    print(f"  Modified payload (attacker hides real endpoint + result):")
    for k, v in entry["payload"].items():
        print(f"    {k}: {v}")

    # ── Write tampered ledger back to disk ────────────────────
    lines[TARGET_SEQ] = json.dumps(entry)
    LEDGER_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print()
    print("  Ledger modified on disk.")
    print("  The signature for entry #2 is now invalid.")
    print("  The causal hash for entry #3 is now broken.")
    print()
    print("  Run:  python verify.py  to see the violations.")
    print()


if __name__ == "__main__":
    main()
