# demo_concurrency.py

"""
GuardClaw — Concurrent Write Safety Demo

Shows that two agents writing simultaneously produce a
tamper-evident ledger with zero corruption.
"""

import os
import threading
from guardclaw import GEFLedger, Ed25519KeyManager, RecordType
from guardclaw.core.replay import ReplayEngine

key = Ed25519KeyManager.generate()
ledger = GEFLedger(key_manager=key, agent_id="demo-agent", ledger_path="./demo_ledger")

def write_entries(thread_id):
    for i in range(10):
        ledger.emit(
            record_type=RecordType.EXECUTION,
            payload={"thread": thread_id, "step": i}
        )

t1 = threading.Thread(target=write_entries, args=("thread-1",))
t2 = threading.Thread(target=write_entries, args=("thread-2",))
t1.start(); t2.start()
t1.join(); t2.join()

engine = ReplayEngine(silent=False)
engine.load("./demo_ledger/ledger.jsonl")
summary = engine.verify()

print(f"Entries written : {summary.total_entries}")
print(f"Chain valid     : {summary.chain_valid}")
print(f"Violations      : {len(summary.violations)}")
print(f"Valid sigs      : {summary.valid_signatures}")
