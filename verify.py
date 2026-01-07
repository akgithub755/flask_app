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
