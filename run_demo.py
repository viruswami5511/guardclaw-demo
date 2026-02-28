
#!/usr/bin/env python3
"""
guardclaw-demo / run_demo.py

Simulates an AI compliance agent running 5 tasks.
Writes a cryptographically signed GEF ledger.
No LLM required.

Usage:
    python run_demo.py
"""

import json
from pathlib import Path

from guardclaw.core.crypto import Ed25519KeyManager
from guardclaw.core.models import ExecutionEnvelope, RecordType

LEDGER_PATH = Path("demo_ledger.jsonl")
KEY_PATH    = Path("demo_key.json")

TASKS = [
    (RecordType.INTENT,    {"action": "scan_accounts",  "authorized": True}),
    (RecordType.EXECUTION, {"action": "query_db",       "rows_returned": 42}),
    (RecordType.EXECUTION, {"action": "call_risk_api",  "endpoint": "https://risk.internal", "result": "high_risk"}),
    (RecordType.EXECUTION, {"action": "write_report",   "flagged": 7}),
    (RecordType.RESULT,    {"action": "notify_team",    "status": "completed"}),
]


def main():
    print()
    print("=" * 60)
    print("  GuardClaw Demo  —  Generating Signed Ledger")
    print("=" * 60)
    print()

    # ── Key ───────────────────────────────────────────────────
if KEY_PATH.exists():
    key = Ed25519KeyManager.from_file(KEY_PATH)   # was .load()
else:
    key = Ed25519KeyManager.generate()
    key.save(KEY_PATH)

    print(f"  Public key   : {key.public_key_hex[:32]}...")  # property, no ()
    print()

    # ── Write ledger ──────────────────────────────────────────
    LEDGER_PATH.unlink(missing_ok=True)

    prev = None
    with open(LEDGER_PATH, "w", encoding="utf-8") as f:
        for seq, (record_type, payload) in enumerate(TASKS):
            env = ExecutionEnvelope.create(
                record_type=       record_type,
                agent_id=          "demo-compliance-agent-v1",
                signer_public_key= key.public_key_hex,   # property, no ()
                sequence=          seq,
                payload=           payload,
                prev=              prev,
            )
            env.sign(key)

            f.write(json.dumps(env.to_dict()) + "\n")

            print(
                f"  [{seq}] {str(record_type):<12}  "
                f"nonce={env.nonce[:10]}...  "
                f"chain=...{env.causal_hash[-8:]}"
            )
            prev = env

    size = LEDGER_PATH.stat().st_size
    print()
    print(f"  Ledger written : {LEDGER_PATH}  ({size:,} bytes)")
    print()
    print("  Next steps:")
    print("    python verify.py          <- confirm ledger is clean")
    print("    python tamper.py          <- simulate an attacker")
    print("    python verify.py          <- watch it get caught")
    print()


if __name__ == "__main__":
    main()
