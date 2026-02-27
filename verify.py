#!/usr/bin/env python3
"""
guardclaw-demo / verify.py

Verifies the GEF ledger using the GuardClaw replay engine.
Exits 0 if clean, 1 if tampered.

Usage:
    python verify.py
"""

import sys
from pathlib import Path

from guardclaw.core.replay import ReplayEngine

LEDGER_PATH = Path("demo_ledger.jsonl")


def main():
    print()
    print("=" * 60)
    print("  GuardClaw Demo  —  Verifying Ledger")
    print("=" * 60)
    print()

    if not LEDGER_PATH.exists():
        print("  ERROR: demo_ledger.jsonl not found.")
        print("  Run:   python run_demo.py  first.")
        print()
        sys.exit(2)

    engine = ReplayEngine(parallel=False, silent=True)

    try:
        engine.load(LEDGER_PATH)
        summary = engine.verify()
    except Exception as exc:
        print(f"  ERROR during verification: {exc}")
        print()
        sys.exit(2)

    # ── Per-entry status ──────────────────────────────────────
    for env in engine.envelopes:
        prev     = engine.envelopes[env.sequence - 1] if env.sequence > 0 else None
        sig_ok   = env.verify_signature()
        chain_ok = env.verify_chain(prev)

        sig_label   = "SIG:OK   " if sig_ok   else "SIG:FAIL "
        chain_label = "CHAIN:OK " if chain_ok else "CHAIN:BREAK"

        print(
            f"  [{env.sequence}] {str(env.record_type):<12}  "
            f"{sig_label}  {chain_label}"
        )

    print()
    print(f"  Entries    : {summary.total_entries}")
    print(f"  Violations : {len(summary.violations)}")
    print()

    # ── Verdict ───────────────────────────────────────────────
    if not summary.violations:
        print("  RESULT: CLEAN")
        print("  All signatures valid. Chain intact.")
        print("  This ledger has not been tampered with.")
        print()
        sys.exit(0)
    else:
        print("  RESULT: TAMPERED")
        print(f"  {len(summary.violations)} violation(s) detected:")
        print()
        for v in summary.violations:
            print(f"    [seq {v.at_sequence}]  {v.violation_type.upper()}")
            print(f"              {v.detail}")
            print()
        print("  This ledger was modified after signing.")
        print("  Tampering is cryptographically proven.")
        print()
        sys.exit(1)


if __name__ == "__main__":
    main()
