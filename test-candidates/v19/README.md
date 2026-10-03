# TRU v19 test candidate

Open [`index.html`](./index.html) for the test page or [`TRU-v19.html`](./TRU-v19.html) for the standalone app. This is a public testing candidate, not a canonical release. The app is self-contained and works offline after it is opened or downloaded.

## Candidate integrity

- Size: 35,028,259 bytes
- SHA-256: `504f7511c5695a71ddf025e2dac72c32757061beb3117cb44d36808dac4558b7`
- The release verifier passes all embedded JSON payload checks, validates 14,088 lexicon records, and confirms that every byte outside the embedded lexicon payload is unchanged from v18.

## Data changes

- Reconciled the embedded LOGOS lexicon against the pinned modular source data, restoring 1,096 duplicated definition fields and the H741 usage field.
- Corrected H7965 `def` and `kjv` fields. The definition and KJV verse references are grounded in the cited Blue Letter Bible entry.
- Corrected G1515 `def` using the cited Blue Letter Bible entry.
- Separate BDB coverage gaps remain; no BDB records were fabricated to fill them.

## Test ideas

1. Search `strongs h7965` and inspect the restored definition and KJV references.
2. Search `strongs g1515` and confirm the definition is not garbled or duplicated.
3. Exercise ordinary Scripture lookup, cross-reference, and offline-reader flows.

## Sources

- H7965: [Blue Letter Bible — Strong's H7965](https://www.blueletterbible.org/lexicon/h7965/kjv/wlc/0-1)
- G1515: [Blue Letter Bible — Strong's G1515](https://www.blueletterbible.org/lexicon/g1515/kjv/tr/0-1)

The candidate is served from a new versioned directory. The TRU Shelf homepage and existing paths were not changed.
