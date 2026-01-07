from __future__ import annotations

import argparse
import csv
import datetime
import shutil
import sys
import time
import zipfile
from pathlib import Path
from typing import Optional

import psutil
import win32com.client

import TraceLib  # existing enterprise logger


# ===============================
# Constants
# ===============================

TRACELIB_ID = "Comparison Mapping"
EXCEL_PROCESS_NAME = "EXCEL.EXE"


# ===============================
# Utility Functions
# ===============================

def format_time(elapsed_seconds: float) -> str:
    """
    Convert elapsed seconds to HH:MM:SS.mmm
    """
    hours, remainder = divmod(elapsed_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{int(hours):02}:{int(minutes):02}:{seconds:06.3f}"


def kill_excel_processes() -> None:
    """
    Kill all running Excel processes to avoid file locks.
    """
    for proc in psutil.process_iter(["name"]):
        if proc.info["name"] == EXCEL_PROCESS_NAME:
            proc.kill()


def copy_file(source: Path, destination: Path) -> Path:
    """
    Copy a file and return the destination path.
    """
    shutil.copyfile(source, destination)
    return destination


def unzip_file(zip_path: Path, extract_to: Path) -> None:
    """
    Extract ZIP file to destination folder.
    """
    try:
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(extract_to)
        time.sleep(2)  # allow filesystem to settle
    except Exception as exc:
        raise RuntimeError(f"Failed to unzip {zip_path}") from exc


def extract_mapping_file(
    file_path: Path,
    temp_root: Path,
    is_first: bool
) -> Path:
    """
    Extract mapping ZIP and return usable Excel file path.
    """
    extraction_dir = temp_root / ("PM1" if is_first else "P")
    extraction_dir.mkdir(parents=True, exist_ok=True)

    unzip_file(file_path, extraction_dir)

    extracted_files = list(extraction_dir.iterdir())

    for file in extracted_files:
        if file.suffix.lower() == ".xlsx":
            return file

    raise FileNotFoundError("No XLSX file found after extraction")


# ===============================
# Excel Automation
# ===============================

def run_excel_macro(
    macro_file: Path,
    module_name: str,
    method_name: str,
    mapping1: Path,
    mapping2: Path,
    temp_dir: Path
) -> None:
    """
    Open Excel and execute VBA macro.
    """
    excel = win32com.client.Dispatch("Excel.Application")
    excel.Visible = False

    workbook = excel.Workbooks.Open(str(macro_file.resolve()))

    try:
        excel.Application.Run(
            f"{module_name}.{method_name}",
            str(mapping1),
            str(mapping2),
            str(temp_dir)
        )
    finally:
        workbook.Close(SaveChanges=False)
        excel.Quit()


# ===============================
# Argument Parsing
# ===============================

def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Excel VBA Macro via Python")

    parser.add_argument("--VBAMacroFilePath", required=True)
    parser.add_argument("--ModuleName", required=True)
    parser.add_argument("--MethodName", required=True)
    parser.add_argument("--Mapping1", required=True)
    parser.add_argument("--Mapping2", required=True)

    return parser.parse_args()


# ===============================
# Main Execution
# ===============================

def main() -> int:
    args = parse_arguments()

    program_start = time.perf_counter()
    trace_id = TraceLib.Start(TRACELIB_ID)

    try:
        kill_excel_processes()

        macro_path = Path(args.VBAMacroFilePath)
        mapping1_zip = Path(args.Mapping1)
        mapping2_zip = Path(args.Mapping2)

        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        temp_dir = Path.home() / "Documents" / f"ComparisonMapping_{timestamp}"
        temp_dir.mkdir(parents=True, exist_ok=True)

        TraceLib.Info(trace_id, "Extracting mapping files")

        mapping1_xlsx = extract_mapping_file(mapping1_zip, temp_dir, True)
        mapping2_xlsx = extract_mapping_file(mapping2_zip, temp_dir, False)

        macro_copy = temp_dir / f"{macro_path.stem}_{timestamp}{macro_path.suffix}"
        copy_file(macro_path, macro_copy)

        TraceLib.Info(trace_id, "Starting Excel macro execution")

        run_excel_macro(
            macro_file=macro_copy,
            module_name=args.ModuleName,
            method_name=args.MethodName,
            mapping1=mapping1_xlsx,
            mapping2=mapping2_xlsx,
            temp_dir=temp_dir
        )

        TraceLib.Info(trace_id, "Excel macro execution completed")

        return_code = 0

    except Exception as exc:
        TraceLib.Error(trace_id, str(exc))
        return_code = 1

    finally:
        elapsed = time.perf_counter() - program_start
        TraceLib.Info(trace_id, f"Elapsed Time: {format_time(elapsed)}")

        kill_excel_processes()
        shutil.rmtree(temp_dir, ignore_errors=True)

        TraceLib.Stop(trace_id)

    return return_code


if __name__ == "__main__":
    sys.exit(main())



'''

EXPLANATION OF CODE AFTER IMAGE REVIEW
====================================

1. OVERALL PURPOSE
------------------
The code is designed to automate an Excel-based comparison process using Python.
It takes two mapping ZIP files, extracts Excel files from them, copies a VBA-enabled
Excel macro file, and executes a specific VBA macro inside Excel using Python.

Python acts as an orchestrator, not as the computation engine.
The actual comparison logic lives inside Excel VBA.

------------------------------------------------------------

2. KEY COMPONENTS EXPLAINED
--------------------------

2.1 TraceLib
------------
TraceLib is an enterprise-grade logging utility.

Why it is used:
- Centralized logging
- Consistent log format across applications
- Execution timing and error tracking
- Used in batch jobs and automation pipelines

Typical lifecycle:
- TraceLib.Start() → begin execution tracking
- TraceLib.Info() → informational logs
- TraceLib.Error() → error logs
- TraceLib.Stop() → close trace session

This is preferred over print() in corporate environments.

------------------------------------------------------------

2.2 Argument Parsing (optparse / argparse)
------------------------------------------
The script accepts runtime parameters such as:
- VBA macro file path
- Module name
- Method name
- Mapping ZIP files

Originally:
- optparse (deprecated)

Modern replacement:
- argparse

Why arguments are used:
- Script becomes reusable
- No hardcoded values
- Easier CI/CD integration
- Supports automation tools

------------------------------------------------------------

2.3 Process Handling (psutil)
-----------------------------
Before and after execution, all Excel processes are killed.

Why:
- Excel locks files
- Hung Excel processes break automation
- Ensures clean environment

psutil scans OS processes and terminates EXCEL.EXE safely.

------------------------------------------------------------

2.4 File Handling & ZIP Extraction
----------------------------------
Steps:
1. Create a timestamped temp directory
2. Copy macro file to temp directory
3. Unzip mapping files
4. Detect .xlsx files inside extracted folders

Why this design:
- Prevents overwriting original files
- Ensures reproducibility
- Avoids manual cleanup

------------------------------------------------------------

2.5 Excel Automation (win32com)
-------------------------------
Python opens Excel using COM automation.

Flow:
- Launch Excel silently
- Open macro workbook
- Call VBA macro using Application.Run
- Pass parameters (file paths)
- Close Excel

Python does NOT:
- Read Excel data
- Perform comparisons

Excel VBA does everything internally.

------------------------------------------------------------

3. EXECUTION FLOW
-----------------
1. Parse command-line arguments
2. Start TraceLib logging
3. Kill existing Excel processes
4. Prepare temp workspace
5. Extract mapping ZIP files
6. Copy macro workbook
7. Execute VBA macro
8. Log execution time
9. Cleanup temp files
10. Stop TraceLib session

------------------------------------------------------------

4. HOW TO EXECUTE THE SCRIPT
----------------------------
Command-line example:

python run_vba_macro.py ^
--VBAMacroFilePath "C:\Path\Macro.xlsm" ^
--ModuleName "MainModule" ^
--MethodName "RunComparison" ^
--Mapping1 "C:\Path\Mapping1.zip" ^
--Mapping2 "C:\Path\Mapping2.zip"

------------------------------------------------------------

5. MODERN PYTHON REWRITE
-----------------------
Changes made in new version:
- optparse → argparse
- os.path → pathlib
- Better function isolation
- Clear typing hints
- Cleaner error handling
- Production-ready structure

Logic remains unchanged.

------------------------------------------------------------

6. WHY THIS DESIGN IS USED
--------------------------
- Excel business logic already exists
- VBA validated by business users
- Python only automates execution
- Faster than rewriting legacy VBA

------------------------------------------------------------

7. REAL-WORLD USE CASES
----------------------
- Risk analytics comparison tools
- Regulatory reporting automation
- Data reconciliation
- Batch Excel validation jobs
- Legacy system integration

------------------------------------------------------------

END OF DOCUMENT

'''