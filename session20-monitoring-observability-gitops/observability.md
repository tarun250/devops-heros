# Observability — Notes

## Monitoring vs observability

- **Monitoring** answers questions you knew to ask in advance: *is CPU above 80%? is the app up?* — dashboards and alerts on known metrics.
- **Observability** lets you answer questions you didn't plan for: *why are only some `/order` requests slow, and only since the last deploy?* — by combining metrics, logs and traces from the system's outputs.

Monitoring tells you **that** something is wrong; observability helps you find **why**.

## The three pillars

| Pillar | What it is | Example from my demo app | Good for |
|---|---|---|---|
| **Metrics** | numbers over time, cheap to store, easy to aggregate and alert on | `app_requests_total{endpoint="/order",status="500"}`, `process_cpu_seconds_total` | trends, dashboards, alerts ("error rate > 5%") |
| **Logs** | timestamped text events with detail | `level=ERROR event=order_failed reason=payment_failed` | the exact error and context of one event |
| **Traces** | the path of **one request** across services, split into timed spans | browser → frontend → API → DB, with how long each hop took | finding which service/hop is slow in a microservice chain |

They work together: an **alert** fires on a metric → the **trace** shows which service is slow → the **logs** of that service show the actual error.

## Why observability is needed

- Distributed systems (microservices, Kubernetes) fail in ways nobody predicted; one request touches many pods.
- Pods are short-lived — when one crashes, its local state is gone; you need data collected *outside* it.
- Faster incident response (lower MTTR): find the root cause from data instead of guessing.
- Capacity planning and SLOs (e.g. "99.9% of requests under 300 ms").
- Confidence to deploy often — you see quickly if a release made things worse.

## Common tools

| Area | Tools |
|---|---|
| Metrics | **Prometheus**, Grafana Mimir, Thanos, Datadog, CloudWatch |
| Dashboards | **Grafana** |
| Alerting | Prometheus **Alertmanager**, Grafana Alerting, PagerDuty / Opsgenie |
| Logs | Grafana **Loki**, ELK/EFK (Elasticsearch + Fluentd/Fluent Bit + Kibana), CloudWatch Logs |
| Traces | **OpenTelemetry** (instrumentation standard), Jaeger, Grafana Tempo, Zipkin |
| All-in-one | Datadog, New Relic, Dynatrace, Grafana Cloud |

## Kubernetes observability

| What | How |
|---|---|
| Resource usage | **metrics-server** → `kubectl top nodes/pods`, used by HPA |
| Cluster + object state | **kube-state-metrics** (replicas, pod phase, restarts) |
| Node metrics | **node-exporter** (CPU, memory, disk, network per node) |
| Container metrics | cAdvisor inside the kubelet |
| App metrics | `/metrics` endpoint scraped via a **ServiceMonitor** / PodMonitor |
| All of the above, packaged | **kube-prometheus-stack** Helm chart (Prometheus Operator + Grafana + Alertmanager + exporters + default dashboards/alerts) |
| Logs | containers write to stdout/stderr → `kubectl logs`; cluster-wide: Fluent Bit / Promtail DaemonSet → Loki or Elasticsearch |
| Events | `kubectl get events` — scheduling, image pulls, probe failures, OOMKills |
| Traces | OpenTelemetry SDK in the app → OTel Collector → Tempo/Jaeger |
| Health | liveness/readiness/startup probes |

What I built is in [`09-app-monitoring/`](./09-app-monitoring) and the main [README](./README.md): metrics, logs, alerts, CPU/memory and app health for a small Flask app.
