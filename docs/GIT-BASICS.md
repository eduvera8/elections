# How this repo works, if you're new to git and GitHub

## The mental model

- **Your folder on disk** is the working copy. You edit files here normally.
- **git** is a local history of snapshots of that folder. Each snapshot is a *commit*.
- **GitHub** is a copy of that history stored on a server, so it is backed up and shareable.

Nothing goes to GitHub automatically. You take snapshots locally (`commit`), then send them
up (`push`). Those are two separate steps, deliberately.

## The four commands you will use 95% of the time

```bash
git status                     # what have I changed? run this constantly
git add .                      # stage everything you've changed for the next snapshot
git commit -m "what I did"     # take the snapshot, locally
git push                       # send local snapshots to GitHub
```

And to get other people's (or another machine's) changes:

```bash
git pull                       # fetch and merge whatever is on GitHub into your folder
```

A good habit: `git pull` before you start working, `git push` when you stop.

## Writing commit messages

Say what changed and why, in one line. `"add padron age data loader"` is good.
`"update"`, `"stuff"`, `"fix"` are not — in six months they tell you nothing, and the whole
point of the history is being able to find when something changed.

## What belongs in this repo and what doesn't

Committed: code (`src/`), documentation (`docs/`), the README.

Not committed: data (`data/`), PDFs (`refs/`). The `.gitignore` file enforces this
automatically — git will simply ignore anything matching the patterns in it.

Why: git keeps every version of every file forever, so a committed 500MB dataset makes the
repository permanently 500MB even if you delete the file later. And `data/README.md` explains
a second reason specific to this project — the RUV's access terms likely prohibit
redistributing individualised victim records.

The test of whether you've done this right: someone clones the repo, runs the scripts in
`src/`, and gets `data/processed/` back. Code and instructions travel; data is re-fetched.

## Branches

A *branch* is a parallel line of history. Right now everything is on `main`. You don't need
branches while you're working alone — commit to `main` and push.

When they become useful: you want to try a restructuring of the analysis without disturbing
the version that works.

```bash
git switch -c try-province-level   # create a branch and switch to it
# ... work, commit as usual ...
git switch main                    # go back; your experiment is still on the branch
```

## If something goes wrong

- **"I changed a file and want the committed version back"**
  `git restore path/to/file`
- **"I committed but want to redo the message"**
  `git commit --amend -m "better message"` (only before pushing)
- **"I want to see what changed"**
  `git diff` (unstaged) or `git log --oneline` (history)
- **"push was rejected"** — usually someone/something else pushed first.
  `git pull` then `git push` again.

Almost nothing in git is truly unrecoverable once committed. The things that *are* dangerous
are `git reset --hard` and `git push --force`, which throw work away. Don't use either
without knowing exactly what you're discarding.

## Where this repo lives

GitHub: https://github.com/eduvera8/elections
