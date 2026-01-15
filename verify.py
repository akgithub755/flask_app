"""
Enterprise Log Monitoring System
================================
- Streams very large log files safely
- Parses enterprise logging format
- Performs error analytics
- Triggers threshold-based alerts
- Emits execution audit summary

Python 3.x | No external dependencies
"""

from dataclasses import dataclass
from datetime import datetime
from collections import Counter
from abc import ABC, abstractmethod
import heapq
import logging


# =========================================================
# CONFIGURATION
# =========================================================

@dataclass(frozen=True)
class LogConfig:
    ERROR_THRESHOLD: int = 500
    TOP_K_ERRORS: int = 5


# =========================================================
# DOMAIN MODEL
# =========================================================

class LogEntry:
    __slots__ = ("timestamp", "level", "component", "message")

    def __init__(self, timestamp, level, component, message):
        self.timestamp = timestamp
        self.level = level
        self.component = component
        self.message = message


# =========================================================
# LOG PARSER (FORMAT-ALIGNED & STREAMING)
# =========================================================

class LogParser:
    """
    Parses logs of the format:
    YYYY-MM-DD HH:MM:SS LEVEL component message...
    """

    TIMESTAMP_FORMAT = "%Y-%m-%d %H:%M:%S,%f"

    def parse(self, file_path):
        with open(file_path, "r", encoding="utf-8", errors="ignore") as file:
            for line in file:
                try:
                    parts = line.strip().split()

                    # Minimum tokens check
                    if len(parts) < 5:
                        continue

                    timestamp = datetime.strptime(
                        f"{parts[0]} {parts[1]}",
                        self.TIMESTAMP_FORMAT
                    )

                    level = parts[2]
                    component = parts[3]
                    message = " ".join(parts[4:])

                    yield LogEntry(timestamp, level, component, message)

                except Exception:
                    # Malformed lines are skipped intentionally
                    continue


# =========================================================
# ANALYTICS ENGINE
# =========================================================

class LogAnalytics:
    def __init__(self):
        self.errors_per_component = Counter()
        self.error_messages = Counter()
        self.error_levels = Counter()
        self.total_lines = 0

    def consume(self, entry: LogEntry):
        self.total_lines += 1

        if entry.level in ("ERROR", "CRITICAL"):
            self.errors_per_component[entry.component] += 1
            self.error_messages[entry.message] += 1
            self.error_levels[entry.level] += 1

    def get_error_count_per_component(self):
        return self.errors_per_component.copy()

    def get_top_k_errors(self, k: int):
        return heapq.nlargest(
            k,
            self.error_messages.items(),
            key=lambda item: item[1]
        )


# =========================================================
# ALERTING (EXTENSIBLE)
# =========================================================

class AlertHandler(ABC):
    @abstractmethod
    def send(self, message: str):
        pass


class LogAlertHandler(AlertHandler):
    def send(self, message: str):
        logging.critical(f"ALERT | {message}")


# =========================================================
# ORCHESTRATOR
# =========================================================

class LogMonitoringService:
    def __init__(self, config: LogConfig, alert_handler: AlertHandler = None):
        self.config = config
        self.parser = LogParser()
        self.analytics = LogAnalytics()
        self.alert_handler = alert_handler or LogAlertHandler()

    def process_log_file(self, log_file_path: str):
        for entry in self.parser.parse(log_file_path):
            self.analytics.consume(entry)

        self._evaluate_alerts()
        return self._generate_summary()

    def _evaluate_alerts(self):
        threshold = self.config.ERROR_THRESHOLD

        for component, count in self.analytics.errors_per_component.items():
            if count > threshold:
                self.alert_handler.send(
                    f"Component '{component}' exceeded error threshold ({count})"
                )

        for level, count in self.analytics.error_levels.items():
            if count > threshold:
                self.alert_handler.send(
                    f"Error level '{level}' exceeded threshold ({count})"
                )

    def _generate_summary(self):
        return {
            "total_lines_processed": self.analytics.total_lines,
            "errors_per_component": self.analytics.get_error_count_per_component(),
            "top_errors": self.analytics.get_top_k_errors(
                self.config.TOP_K_ERRORS
            )
        }


# =========================================================
# INTERNAL LOGGING SETUP
# =========================================================

def setup_internal_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s"
    )


# =========================================================
# EXECUTION + AUDIT
# =========================================================

if __name__ == "__main__":
    setup_internal_logging()

    config = LogConfig(
        ERROR_THRESHOLD=500,
        TOP_K_ERRORS=5
    )

    service = LogMonitoringService(config)

    summary = service.process_log_file("enterprise_logs.log")

    # ================= EXECUTION AUDIT =================
    print("\n========== LOG MONITORING AUDIT ==========")

    print(f"\nTotal log lines processed: {summary['total_lines_processed']}")

    print("\nError count per component:")
    if summary["errors_per_component"]:
        for component, count in summary["errors_per_component"].items():
            print(f"{component}: {count}")
    else:
        print("No ERROR or CRITICAL entries found")

    print("\nTop recurring error messages:")
    if summary["top_errors"]:
        for message, count in summary["top_errors"]:
            print(f"{count} occurrences | {message}")
    else:
        print("No recurring errors found")

    print("\n========== END OF AUDIT ==========\n")
