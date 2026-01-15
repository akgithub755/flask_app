# log_generator.py
import logging
import random
from logging.handlers import RotatingFileHandler

class EnterpriseLogGenerator:
    LEVELS = [logging.INFO, logging.WARNING, logging.ERROR, logging.CRITICAL]
    MODULES = ["auth_module", "payment_module", "order_module", "user_module"]
    MESSAGES = {
        logging.INFO: "Operation completed successfully",
        logging.WARNING: "Retrying due to transient issue",
        logging.ERROR: "Failed operation due to system error",
        logging.CRITICAL: "System outage detected"
    }

    def __init__(self, log_file: str):
        self.logger = logging.getLogger("EnterpriseLogger")
        self.logger.setLevel(logging.INFO)

        handler = RotatingFileHandler(
            log_file,
            maxBytes=50 * 1024 * 1024,  # 50MB
            backupCount=10
        )

        formatter = logging.Formatter(
            "%(asctime)s %(levelname)s %(module)s %(message)s"
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def generate(self, lines: int = 1_000_000):
        for _ in range(lines):
            level = random.choice(self.LEVELS)
            component = random.choice(self.MODULES)
            msg = self.MESSAGES[level]

            self.logger.log(level, msg, extra={"component": component})
