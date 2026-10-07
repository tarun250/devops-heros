# Session 16 — CI/CD & GitHub Actions (Submission)

Pipeline: [`.github/workflows/session16-ci.yml`](../.github/workflows/session16-ci.yml)
App: `session-16-github-actions/session-16-github-actions/10-final-cicd-pipeline` (calculator + pytest)

GitHub only runs workflows from the repo root `.github/workflows/`, so the workflow lives there and uses `working-directory` to point at the session folder.

## Concepts

| Term | Meaning | In my workflow |
|---|---|---|
| CI | every push is built + tested automatically | `test` job on every push |
| CD | tested build is shipped automatically (delivery = ready to release, deployment = released) | `build` uploads the artifact; session 17 deploys to Kubernetes |
| Workflow | YAML file in `.github/workflows/` | `session16-ci.yml` |
| Trigger (`on:`) | what starts it | `push` / `pull_request` to `main`, `paths` filter, `workflow_dispatch` |
| Branch filter | only run for some branches | `branches: [main]` |
| Job | group of steps on one runner; jobs run in parallel unless `needs:` | `test` → `build` + `security-check` in parallel |
| Step | one command (`run:`) or action (`uses:`) | checkout, setup-python, pytest |
| Runner | the machine that runs a job | GitHub-hosted `ubuntu-latest` (self-hosted is possible) |
| Secret | encrypted value, injected as `${{ secrets.NAME }}`, masked as `***` in logs | session 17 uses the built-in `GITHUB_TOKEN` to push to GHCR |
| Artifact | file kept after the run | `calculator-build` (the `build/` folder) |

## Pipeline

| Job | Needs | What it does |
|---|---|---|
| Test Application | – | setup Python 3.12, `pip install`, `pytest -v` |
| Build Application | test | `build.sh`, upload `build/` as artifact `calculator-build` |
| Security Check | test | fails if `.env`, `*.pem`, `*.key` files are committed |

Triggers: push to `main` (only when session 16 files or the workflow change), pull requests, `workflow_dispatch` (manual run button).

## Local run first

```powershell
pytest -v
```
![local pytest](./screenshots/01-local-pytest.png)

```powershell
bash build.sh
```
![local build](./screenshots/02-local-build.png)

## GitHub Actions run

Run: https://github.com/tarun250/devops-heros/actions/runs/37621643045 — all 3 jobs green, 1 artifact.

![actions run](./screenshots/03-actions-run.png)

## Failed run → fix → re-run

Broke `add()` on purpose (`a + b` → `a - b`) and pushed. `Test Application` failed, so `Build` and `Security Check` were skipped (they `need` test). Nothing broken got built.

![failed run](./screenshots/04-failed-run.png)

Reproduced it locally to find the cause:

```powershell
pytest -q --tb=line
```
![reproduce](./screenshots/05-reproduce-failure.png)

Fixed the code, tests pass locally:

![fix](./screenshots/06-fix-local.png)

Pushed the fix, pipeline green again:

![fixed run](./screenshots/07-fixed-run.png)

Run history — red then green:

![history](./screenshots/08-run-history.png)

A failed job can also be re-run from the run page (**Re-run failed jobs**) when the failure was flaky, not a code bug.
