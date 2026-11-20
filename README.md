# mas-harness-execution-plane

The execution plane of the harness programme (repository R08). It will own four harnesses:
protocol interoperability, orchestration (the durable executor), the tool and skill sandbox,
and ML decisions.

## Scope of this shell

This tree is a health-only shell, built by the bootstrap packet PLANE-BOOTSTRAP-R08:

- `src/planeon_execution/health/`: `health()` returns `{"status": "ok", "plane": "execution"}`,
  and a standard-library WSGI callable `application` answers `GET /health` with that mapping
  as JSON (any other path: 404; any other method on `/health`: 405).
- `tests/health/`: the standard-library unittest for it.
- `ci/`: the offline transport (`verify-offline.sh`, `run_packet_argv.py`, `network_canary.py`,
  `warm-source-isolation.sh`), byte copies of the harness-onion files the verifier pins.

Exact CPython 3.12.14, standard library only, no third-party dependency. There is no image,
database, deployment, hosted workflow, model server, Makefile, porting ledger or runtime code.

## Verification

Every pull request is verified by the owner-operated verifier. It runs the packet's offline
acceptance command through `./ci/verify-offline.sh` with all outbound network denied:

    python3 -I -B -m unittest discover -s tests/health

## What comes next

EXEC-001 remains the repository's registered bootstrap packet. It alone owns the Makefile,
`ci/run_make_target.py` and `PORTING.yaml`, and it builds on this shell. Runtime coding stays
behind two gates: CONF-LINUX-001 (a native Linux baseline PASS) and LANG-HOTPATH-DECISION-001
(the implementation language of the hot-path services).

## License

Apache License 2.0; see `LICENSE`.
