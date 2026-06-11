# Contributing

Contributions that improve portability, safety, tests, documentation, or
maintainer automation are welcome.

## Development Setup

The public package uses only the Python standard library.

```bash
git clone https://github.com/kax168/hermes-agent-content-ops.git
cd hermes-agent-content-ops
python3 -m unittest discover -s tests
python3 scripts/run_finish_audit.py
```

## Pull Requests

1. Open an issue first for large behavioral changes.
2. Keep credentials and private prompts out of commits, fixtures, and logs.
3. Add or update tests for behavioral changes.
4. Preserve draft-first behavior and human approval for irreversible actions.
5. Run the unit tests and audit before submitting a pull request.

Small documentation fixes may be submitted directly.

## Issues

Include the Python version, operating system, command run, expected behavior,
and sanitized output. Never include API keys, account identifiers, unpublished
content, or private source material.
