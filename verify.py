# url_monitoring_system.py

import time
import threading
import logging
import random
from datetime import datetime
from typing import Dict, List
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests

# =========================
# ENTERPRISE LOGGING SETUP
# =========================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(threadName)s | %(message)s",
    handlers=[
        logging.FileHandler("url_monitoring.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


# =========================
# RESPONSE METRICS
# =========================
class ResponseMetrics:
    """
    Immutable response snapshot
    """

    def __init__(self, url: str, response_time: float, status_code: int, is_up: bool):
        self.url = url
        self.response_time = response_time
        self.status_code = status_code
        self.is_up = is_up
        self.timestamp = datetime.utcnow()

    def __repr__(self):
        return (
            f"ResponseMetrics(url={self.url}, "
            f"status={self.status_code}, "
            f"latency={self.response_time:.2f}ms, "
            f"is_up={self.is_up})"
        )


# =========================
# URL MONITOR
# =========================
class URLMonitor:
    """
    Performs HTTP health checks
    """

    def __init__(self, timeout: float = 3.0):
        self.timeout = timeout

    def check(self, url: str) -> ResponseMetrics:
        start = time.perf_counter()
        try:
            response = requests.get(url, timeout=self.timeout)
            latency = (time.perf_counter() - start) * 1000

            is_up = 200 <= response.status_code < 300

            return ResponseMetrics(
                url=url,
                response_time=latency,
                status_code=response.status_code,
                is_up=is_up
            )

        except requests.RequestException:
            latency = (time.perf_counter() - start) * 1000
            return ResponseMetrics(
                url=url,
                response_time=latency,
                status_code=0,
                is_up=False
            )


# =========================
# STATUS TRACKER
# =========================
class StatusTracker:
    """
    Maintains URL health history & downtime windows
    """

    def __init__(self):
        self.history: Dict[str, List[ResponseMetrics]] = {}
        self.down_since: Dict[str, datetime] = {}

    def record(self, metrics: ResponseMetrics):
        self.history.setdefault(metrics.url, []).append(metrics)

        if metrics.is_up:
            self.down_since.pop(metrics.url, None)
        else:
            self.down_since.setdefault(metrics.url, metrics.timestamp)

    def get_downtime(self, url: str) -> float:
        if url not in self.down_since:
            return 0.0
        return (datetime.utcnow() - self.down_since[url]).total_seconds()


# =========================
# ALERT MANAGER
# =========================
class AlertManager:
    """
    Threshold-based alerting with false-positive protection
    """

    def __init__(self, downtime_threshold: int):
        self.threshold = downtime_threshold
        self.alerted: set = set()

    def evaluate(self, url: str, downtime: float):
        if downtime >= self.threshold and url not in self.alerted:
            self.alerted.add(url)
            self._send_alert(url, downtime)

        if downtime == 0:
            self.alerted.discard(url)

    def _send_alert(self, url: str, downtime: float):
        logger.error(
            f"🚨 ALERT: {url} DOWN for {int(downtime)} seconds"
        )


# =========================
# REPORT GENERATOR
# =========================
class ReportGenerator:
    """
    Generates availability summaries
    """

    def __init__(self, tracker: StatusTracker):
        self.tracker = tracker

    def generate(self):
        logger.info("========= MONITORING REPORT =========")

        for url, metrics in self.tracker.history.items():
            total = len(metrics)
            up = sum(1 for m in metrics if m.is_up)
            uptime = (up / total) * 100 if total else 0

            logger.info(
                f"{url} | Checks: {total} | Uptime: {uptime:.2f}%"
            )


# =========================
# MONITOR SCHEDULER
# =========================
class MonitorScheduler:
    """
    High-concurrency monitoring engine
    """

    def __init__(
        self,
        urls: List[str],
        interval: int,
        workers: int,
        downtime_threshold: int
    ):
        self.urls = urls
        self.interval = interval
        self.monitor = URLMonitor()
        self.tracker = StatusTracker()
        self.alert_manager = AlertManager(downtime_threshold)
        self.reporter = ReportGenerator(self.tracker)
        self.executor = ThreadPoolExecutor(max_workers=workers)
        self._stop_event = threading.Event()

    def start(self):
        logger.info("Starting URL Monitoring System")

        try:
            while not self._stop_event.is_set():
                futures = {
                    self.executor.submit(self.monitor.check, url): url
                    for url in self.urls
                }

                for future in as_completed(futures):
                    metrics = future.result()
                    self.tracker.record(metrics)

                    downtime = self.tracker.get_downtime(metrics.url)
                    self.alert_manager.evaluate(metrics.url, downtime)

                time.sleep(self.interval)

        except KeyboardInterrupt:
            logger.info("Graceful shutdown initiated")

        finally:
            self.shutdown()

    def shutdown(self):
        self.executor.shutdown(wait=True)
        self.reporter.generate()
        logger.info("Monitoring stopped cleanly")


# =========================
# EXAMPLE EXECUTION
# =========================
if __name__ == "__main__":
    # Simulated URLs
    urls = [f"http://example.com/api/{i}" for i in range(100)]

    scheduler = MonitorScheduler(
        urls=urls,
        interval=5,
        workers=20,
        downtime_threshold=15
    )

    scheduler.start()
