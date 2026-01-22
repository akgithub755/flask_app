import requests
import time
import logging
from datetime import datetime


# -------------------------
# LOGGING SETUP
# -------------------------
logging.basicConfig(
    filename="url_monitor.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)


class URLMonitorSystem:
    """
    Simple monolithic URL monitoring system using OOP
    """

    def __init__(self, url_file, check_interval=5, timeout=3, max_failures=3):
        self.url_file = url_file
        self.check_interval = check_interval
        self.timeout = timeout
        self.max_failures = max_failures

        self.urls = self._load_urls()
        self.history = {}        # URL → list of checks
        self.failure_count = {} # URL → consecutive failures

    # -------------------------
    # LOAD URLS
    # -------------------------
    def _load_urls(self):
        with open(self.url_file) as f:
            return [line.strip() for line in f if line.strip()]

    # -------------------------
    # CHECK SINGLE URL
    # -------------------------
    def check_url(self, url):
        start = time.time()
        try:
            response = requests.get(url, timeout=self.timeout)
            latency = int((time.time() - start) * 1000)

            is_up = 200 <= response.status_code < 300
            status = response.status_code

        except requests.RequestException:
            latency = int((time.time() - start) * 1000)
            is_up = False
            status = "TIMEOUT"

        return {
            "time": datetime.utcnow(),
            "latency_ms": latency,
            "status": status,
            "up": is_up
        }

    # -------------------------
    # RECORD HISTORY
    # -------------------------
    def record_status(self, url, result):
        self.history.setdefault(url, []).append(result)

        if result["up"]:
            self.failure_count[url] = 0
        else:
            self.failure_count[url] = self.failure_count.get(url, 0) + 1

    # -------------------------
    # ALERT LOGIC
    # -------------------------
    def check_alert(self, url):
        if self.failure_count.get(url, 0) >= self.max_failures:
            logging.error(
                f"ALERT: {url} DOWN for {self.failure_count[url]} consecutive checks"
            )

    # -------------------------
    # RUN MONITOR
    # -------------------------
    def run(self, cycles=5):
        logging.info("Starting URL monitoring")

        for cycle in range(cycles):
            print(f"\n--- Monitoring cycle {cycle + 1} ---")

            for url in self.urls:
                result = self.check_url(url)
                self.record_status(url, result)
                self.check_alert(url)

                print(
                    f"{url} | "
                    f"Status: {result['status']} | "
                    f"Latency: {result['latency_ms']}ms | "
                    f"Up: {result['up']}"
                )

                logging.info(f"{url} | {result}")

            time.sleep(self.check_interval)

        self.generate_report()

    # -------------------------
    # FINAL REPORT
    # -------------------------
    def generate_report(self):
        print("\n===== FINAL REPORT =====")
        for url, records in self.history.items():
            total = len(records)
            up = sum(1 for r in records if r["up"])
            uptime = (up / total) * 100

            print(f"{url} → Uptime: {uptime:.2f}% ({up}/{total})")
            logging.info(f"REPORT | {url} | Uptime {uptime:.2f}%")


# -------------------------
# EXECUTION
# -------------------------
if __name__ == "__main__":
    monitor = URLMonitorSystem(
        url_file="imp.txt",
        check_interval=5,
        timeout=3,
        max_failures=2
    )

    monitor.run(cycles=5)
