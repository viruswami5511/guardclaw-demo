\# guardclaw-demo



Minimal demo of \[GuardClaw](https://github.com/viruswami5511/guardclaw) —

cryptographic accountability for AI agents (GEF v1.0).



No LLM required. No API keys. Pure cryptography.



\## Install



```bash

pip install guardclaw

git clone https://github.com/viruswami5511/guardclaw-demo

cd guardclaw-demo

```



\## Run the Demo



\*\*Step 1 — Generate a signed ledger\*\*

```bash

python run\_demo.py

```

```

&nbsp;intent        nonce=3f8a2b1d4e...  chain=...4a2f1c8e

&nbsp;execution     nonce=9c1e5d2f7a...  chain=...b7e39210

&nbsp;execution     nonce=1a7f3e8b2c...  chain=...c4d891b3

&nbsp;execution     nonce=5b2d9c1f4e...  chain=...8f2a1e4d

&nbsp;result        nonce=7e1c4f8a2b...  chain=...2e7b4f1a



Ledger written: demo\_ledger.jsonl

```



\*\*Step 2 — Verify the clean ledger\*\*

```bash

python verify.py

```

```

&nbsp;intent        SIG:OK    CHAIN:OK

&nbsp;execution     SIG:OK    CHAIN:OK

&nbsp;execution     SIG:OK    CHAIN:OK

&nbsp;execution     SIG:OK    CHAIN:OK

&nbsp;result        SIG:OK    CHAIN:OK



RESULT: CLEAN

All signatures valid. Chain intact.

```



\*\*Step 3 — Simulate an attacker editing entry #2\*\*

```bash

python tamper.py

```

```

Target entry   : sequence #2

Original:  endpoint=https://risk.internal  result=high\_risk

Modified:  endpoint=https://legitimate-api.internal/safe  result=low\_risk\_cleared



Ledger modified on disk.

```



\*\*Step 4 — Verify the tampered ledger\*\*

```bash

python verify.py

```

```

&nbsp;intent        SIG:OK    CHAIN:OK

&nbsp;execution     SIG:OK    CHAIN:OK

&nbsp;execution     SIG:FAIL  CHAIN:OK       <- signature broken

&nbsp;execution     SIG:OK    CHAIN:BREAK    <- hash chain broken

&nbsp;result        SIG:OK    CHAIN:OK



RESULT: TAMPERED

2 violation(s) detected:



&nbsp; \[seq 2]  INVALID\_SIGNATURE

&nbsp;           Signature invalid (signer: ...)



&nbsp; \[seq 3]  CHAIN\_BREAK

&nbsp;           causal\_hash mismatch: expected ...c4d891b3, got ...7f1a2e9d



This ledger was modified after signing.

Tampering is cryptographically proven.

```



\## Why This Matters



The attacker changed a payload field — one line in a JSON file.

GuardClaw caught it because:



1\. \*\*Ed25519 signature\*\* signs the exact bytes of the payload. Any change = invalid signature.

2\. \*\*SHA-256 causal hash chain\*\* links each entry to the previous one. Tamper entry #2 = break entry #3.

3\. \*\*Neither can be fixed\*\* without the private key the agent used when it originally ran.



The verifier needs only the \*\*public key\*\* embedded in each envelope.

No central server. No SaaS. Offline verification by anyone.



\## Protocol Specification



\[GEF-SPEC-1.0](https://github.com/viruswami5511/guardclaw/blob/master/SPEC.md)



\## License



Apache 2.0



