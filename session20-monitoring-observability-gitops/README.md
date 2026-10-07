# Session 20 — Monitoring, Observability & GitOps (Submission)

Prometheus + Grafana with Docker Compose, Argo CD on Minikube.

## Prometheus + Grafana (`04-grafana/`)

```powershell
docker compose up -d
docker compose ps
```
![compose up](./screenshots/01-compose-up.png)

Prometheus scraping itself every 5s — target is `up`:
```powershell
(Invoke-RestMethod 'http://localhost:9090/api/v1/targets').data.activeTargets
```
![prometheus api](./screenshots/02-prometheus-api.png)
![prometheus targets](./screenshots/03-prometheus-targets.png)

Grafana → Prometheus data source (`http://prometheus:9090`, the compose service name), and Grafana querying `up` through it:

![grafana datasource](./screenshots/05-grafana-datasource.png)

Dashboard with 4 panels: `sum(up)`, `rate(prometheus_http_requests_total[1m])` by handler, `process_resident_memory_bytes`, `scrape_samples_scraped`.

![grafana dashboard](./screenshots/04-grafana-dashboard.png)

Data source and dashboard were added through Grafana's HTTP API (same result as clicking through the UI).

## Mini project — GitOps with Argo CD (`08-mini-project/`)

**Install Argo CD**
```powershell
kubectl create namespace argocd
kubectl apply -n argocd --server-side -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
kubectl get pods -n argocd
```
![argocd install](./screenshots/06-argocd-install.png)

**Application** — `app/argocd-application.yaml` points at this repo (`tarun250/devops-heros`, path `session20-monitoring-observability-gitops/08-mini-project/app`). `directory.exclude` keeps the Application file itself out of the synced manifests. Auto-sync with `prune` + `selfHeal`.

```powershell
kubectl apply -f app/argocd-application.yaml
kubectl get applications -n argocd
kubectl get all -n session20
```
![app synced](./screenshots/07-argocd-app-synced.png)

**Self-healing** — scaled to 5 by hand, Argo CD put it back to 2 (what Git says) within ~15s.

![self heal](./screenshots/08-argocd-self-heal.png)

**Git change** — `replicas: 2 → 3`, commit, push. No `kubectl apply`.

![git push](./screenshots/09-git-change-push.png)

Argo CD picked up the commit on its next poll (~3 min) and scaled to 3:

![synced 3](./screenshots/10-argocd-synced-3.png)

Synced revision = the pushed commit `76f8b52`:

![revision](./screenshots/11-argocd-revision.png)

## Viva questions

1. **Monitoring vs observability** — monitoring watches known metrics/alerts; observability lets you ask new questions from metrics, logs and traces.
2. **Metrics / logs / traces** — numbers over time / event text / one request's path across services.
3. **Prometheus** — pull-based time-series DB; scrapes `/metrics` endpoints, queried with PromQL.
4. **Grafana** — dashboards and alerts on top of data sources like Prometheus.
5. **GitOps** — Git holds the desired state; an agent in the cluster makes the cluster match it.
6. **Git as source of truth** — every change is a reviewed, versioned commit; rollback = `git revert`.
7. **Argo CD** — watches a Git path and syncs it into Kubernetes, shows drift.
8. **Desired state** — what's in Git (3 replicas).
9. **Actual state** — what's running in the cluster right now.
10. **Reconciliation** — the loop that compares desired vs actual and fixes the difference.
11. **Self-healing** — manual changes in the cluster are reverted to match Git.
12. **Replicas 2 → 3 in Git** — Argo CD detects the new commit, syncs, Deployment scales to 3.
