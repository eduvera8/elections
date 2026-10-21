# data/

Nothing in `raw/`, `interim/` or `processed/` is committed to git — see `.gitignore`. Only
this file and the `.gitkeep` placeholders are tracked.

| Folder | Contents | Rule |
|---|---|---|
| `raw/` | Exactly as downloaded | Never edit. Never commit. Record the source URL and date in `docs/02-data-sources.md` |
| `interim/` | Cleaned intermediates | Rebuildable from `raw/` by `src/` |
| `processed/` | Final analysis panels | Rebuildable end to end |

## Why data is not committed

Three reasons. Git stores a full copy of every version of every file, so committing data makes
the repository permanently large even after deletion. Data files change often and produce diffs
nobody can read. And the RUV's 2018 regulation restricts redistribution of individualised victim
information — committing it to a public GitHub repository would likely breach the access terms
under which it was obtained.

If you need to share the data, share it outside git (Zenodo, OSF, institutional storage) and link
to it from `docs/02-data-sources.md`.

## Sensitive data

The CVR and RUV records are individual-level records of killings and disappearances of named
people. Keep them in `raw/`, keep them out of git, and do not publish anything that could
re-identify victims or their families beyond what the source already makes public.
