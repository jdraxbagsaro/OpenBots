# Contributing

Thanks for helping improve OpenDots. Keep changes small, make runtime behavior explicit, and update the docs when a command or configuration value changes.

## Local checks

Requires Python 3.11 or newer. From the repository root:

```bash
python -m unittest discover -s tests -v
PYTHONPATH=src python -m opendots.cli --help
```

On Windows PowerShell, set the source path with `$env:PYTHONPATH = "src"` before running the second command.

## Pull requests

- Explain the user-visible behavior and the reason for the change.
- Add or update focused tests for changed behavior.
- Never include real credentials, private prompts, or user data in tests or examples.
- For a new provider or tool capability, document its network access, permissions, failure modes, and trust boundary.
- Do not describe OpenDots as bypassing model safeguards or as guaranteeing unrestricted output.