# Quant Strategy Memory

This repository is the shared memory base for 量外策略 research across machines.

Recommended use:

- Store stable decisions in `memory/decisions.md`.
- Store data-source contracts in `references/data-sources.md`.
- Store strategy hypotheses and experiments in `memory/strategy-log.md`.
- Keep secrets, brokerage credentials, API keys, cookies, and personal account data out of this repo.

To sync across machines, create a private GitHub repository and push this folder:

```bash
git remote add origin git@github.com:<your-user>/<your-private-repo>.git
git push -u origin main
```
