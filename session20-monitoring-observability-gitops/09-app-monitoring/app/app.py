import logging
import random
import time

from flask import Flask, Response, jsonify
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Histogram, generate_latest

app = Flask(__name__)

# one log line per event, key=value so it is easy to grep / parse in a log system
logging.basicConfig(level=logging.INFO, format="%(asctime)s level=%(levelname)s %(message)s")
log = logging.getLogger("demo-app")
logging.getLogger("werkzeug").setLevel(logging.WARNING)

REQUESTS = Counter("app_requests_total", "HTTP requests", ["endpoint", "status"])
LATENCY = Histogram("app_request_duration_seconds", "Request latency", ["endpoint"])
ORDERS = Counter("app_orders_total", "Orders placed")


@app.route("/")
def home():
    with LATENCY.labels("/").time():
        REQUESTS.labels("/", "200").inc()
        return jsonify(status="ok", app="session20-demo")


@app.route("/order")
def order():
    with LATENCY.labels("/order").time():
        time.sleep(random.uniform(0.01, 0.3))
        if random.random() < 0.1:  # ~10% simulated failures
            REQUESTS.labels("/order", "500").inc()
            log.error("event=order_failed reason=payment_failed")
            return jsonify(error="payment failed"), 500
        ORDERS.inc()
        log.info("event=order_placed")
        REQUESTS.labels("/order", "200").inc()
        return jsonify(order="placed")


@app.route("/health")
def health():
    return jsonify(status="UP")


@app.route("/metrics")
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
