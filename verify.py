"""
Stored Procedure Executor using pyodbc
Python 3.x
"""

import time
import logging
from typing import Dict, Any, List
import pyodbc


# ==========================
# Logger
# ==========================

class Logger:
    def __init__(self):
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s | %(levelname)s | %(message)s"
        )
        self.log = logging.getLogger("SP_EXECUTOR")

    def info(self, msg: str):
        self.log.info(msg)

    def error(self, msg: str):
        self.log.error(msg)


# ==========================
# DB Configuration
# ==========================

class DBConfig:
    def __init__(
        self,
        host: str,
        port: int,
        database: str,
        user: str,
        password: str,
        driver: str,
        use_mock: bool = True
    ):
        self.host = host
        self.port = port
        self.database = database
        self.user = user
        self.password = password
        self.driver = driver
        self.use_mock = use_mock


# ==========================
# Mock Database (Sample SPs)
# ==========================

class MockDatabase:
    def connect(self):
        return True

    def execute(self, procedure_name: str, params: Dict[str, Any]):
        if procedure_name == "sp_get_customer_risk":
            return [{
                "customer_id": params.get("customer_id"),
                "risk_score": 70,
                "risk_level": "MEDIUM"
            }]

        if procedure_name == "sp_transaction_summary":
            return [{
                "account_id": params.get("account_id"),
                "txn_count": 120,
                "amount": 450000
            }]

        if procedure_name == "sp_account_balance":
            return [{
                "account_id": params.get("account_id"),
                "balance": 980000,
                "status": "ACTIVE"
            }]

        raise ValueError(f"Stored procedure '{procedure_name}' not found")

    def close(self):
        pass


# ==========================
# Real Database using pyodbc
# ==========================

class RealDatabase:
    def __init__(self, config: DBConfig):
        self.config = config
        self.connection = None

    def connect(self):
        conn_str = (
            f"DRIVER={{{self.config.driver}}};"
            f"SERVER={self.config.host},{self.config.port};"
            f"DATABASE={self.config.database};"
            f"UID={self.config.user};"
            f"PWD={self.config.password};"
        )
        self.connection = pyodbc.connect(conn_str)
        return self.connection

    def execute(self, procedure_name: str, params: Dict[str, Any]):
        cursor = self.connection.cursor()

        if params:
            placeholders = ",".join(["?"] * len(params))
            sql = f"EXEC {procedure_name} {placeholders}"
            cursor.execute(sql, list(params.values()))
        else:
            cursor.execute(f"EXEC {procedure_name}")

        # Fetch result set
        columns = [col[0] for col in cursor.description]
        rows = cursor.fetchall()

        result = [
            dict(zip(columns, row))
            for row in rows
        ]

        cursor.close()
        return result

    def close(self):
        if self.connection:
            self.connection.close()


# ==========================
# Database Manager
# ==========================

class DatabaseManager:
    def __init__(self, config: DBConfig):
        self.config = config
        self.db = MockDatabase() if config.use_mock else RealDatabase(config)

    def connect(self):
        self.db.connect()

    def execute_procedure(self, name: str, params: Dict[str, Any]):
        return self.db.execute(name, params)

    def close(self):
        self.db.close()


# ==========================
# Stored Procedure Model
# ==========================

class StoredProcedure:
    def __init__(self, name: str, params: Dict[str, Any] = None):
        self.name = name
        self.params = params or {}


# ==========================
# Procedure Executor
# ==========================

class ProcedureExecutor:
    def __init__(self, db: DatabaseManager, logger: Logger):
        self.db = db
        self.logger = logger

    def run(self, procedures: List[StoredProcedure]):
        results = {}
        self.db.connect()

        for sp in procedures:
            start = time.time()
            try:
                self.logger.info(f"Executing {sp.name}")
                data = self.db.execute_procedure(sp.name, sp.params)
                duration = round(time.time() - start, 2)

                results[sp.name] = {
                    "rows": len(data),
                    "data": data,
                    "execution_time_sec": duration
                }

            except Exception as e:
                self.logger.error(f"{sp.name} failed: {e}")

        self.db.close()
        return results


# ==========================
# Main Execution
# ==========================

if __name__ == "__main__":

    logger = Logger()

    # --------- DB CONFIG ---------
    db_config = DBConfig(
        host="localhost",
        port=1433,
        database="risk_db",
        user="admin",
        password="secret",
        driver="ODBC Driver 17 for SQL Server",
        use_mock=True   # 🔁 Change to False for real DB
    )

    # --------- STORED PROCEDURES ---------
    procedures = [
        StoredProcedure(
            "sp_get_customer_risk",
            {"customer_id": 101}
        ),
        StoredProcedure(
            "sp_transaction_summary",
            {"account_id": 5001}
        ),
        StoredProcedure(
            "sp_account_balance",
            {"account_id": 5001}
        )
    ]

    # --------- EXECUTION ---------
    db_manager = DatabaseManager(db_config)
    executor = ProcedureExecutor(db_manager, logger)

    output = executor.run(procedures)

    logger.info(f"Final Output: {output}")
