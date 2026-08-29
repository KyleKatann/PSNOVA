# Data

This directory is reserved for authoritative structured PSNOVA game data.

Rules:

- `docs/` contains published GitHub Pages output only.
- `tools/` contains generators, migration utilities, and legacy editing helpers.
- `data/` contains source-of-truth structured data used by generators.
- Do not edit generated HTML to change gameplay values once an equivalent dataset exists here.
- Migrate one dataset at a time and verify row counts/sentinel values before making it authoritative.

The migration begins with weapon data and expands only after generated output matches the existing site.
