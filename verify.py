import logging
from logging.handlers import RotatingFileHandler
import random
import time
from datetime import datetime

# ---------------- CONFIG ----------------
LOG_FILE = "enterprise.log"
MAX_BYTES = 50 * 1024 * 1024      # 50 MB per file
BACKUP_COUNT = 5                 # rotation files
TOTAL_LINES = 200_000            # generate 200k log lines

MODULES = ["auth", "payment", "order", "user"]
LEVELS = [logging.INFO, logging.WARNING, logging.ERROR, logging.CRITICAL]

ERROR_MESSAGES = {
    "auth": [
        "Failed login attempt",
        "Invalid authentication token",
        "User session expired"
    ],
    "payment": [
        "Payment gateway timeout",
        "Insufficient balance",
        "Transaction declined"
    ],
    "order": [
        "Order creation failed",
        "Order not found",
        "Inventory unavailable"
    ],
    "user": [
        "User profile update failed",
        "User not found",
        "Email already exists"
    ]
}

INFO_MESSAGES = {
    "auth": ["User logged in", "User logged out"],
    "payment": ["Payment initiated", "Payment successful"],
    "order": ["Order placed", "Order shipped"],
    "user": ["User registered", "User profile updated"]
}

# -------------- LOGGER SETUP --------------
def setup_logger():
    logger = logging.getLogger("enterprise_logger")
    logger.setLevel(logging.INFO)

    handler = RotatingFileHandler(
        LOG_FILE,
        maxBytes=MAX_BYTES,
        backupCount=BACKUP_COUNT
    )

    formatter = logging.Formatter(
        "%(asctime)s %(levelname)s %(component)s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.propagate = False

    return logger


# -------------- LOG GENERATION --------------
def generate_logs():
    logger = setup_logger()

    for _ in range(TOTAL_LINES):
        component = random.choice(MODULES)
        level = random.choices(
            LEVELS,
            weights=[70, 15, 10, 5]   # realistic production distribution
        )[0]

        if level >= logging.ERROR:
            message = random.choice(ERROR_MESSAGES[component])
        else:
            message = random.choice(INFO_MESSAGES[component])

        logger.log(
            level,
            message,
            extra={"component": component}
        )

        # tiny delay to make timestamps realistic
        time.sleep(0.0001)


# -------------- MAIN --------------
if __name__ == "__main__":
    print("Generating enterprise logs...")
    generate_logs()
    print("Log generation completed.")
