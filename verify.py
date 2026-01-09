import pandas as pd
from pathlib import Path
from datetime import datetime


class ExcelReconciler:
    COMPARE_COLUMNS = ["a", "b", "c"]

    def __init__(self, input_file: str, output_dir: str = None):
        self.input_file = input_file
        self.output_dir = Path(output_dir) if output_dir else Path(__file__).parent

        self.df1 = None
        self.df2 = None
        self.differences = {}

    # -----------------------------
    # Load Excel data
    # -----------------------------
    def _load_data(self):
        self.df1 = pd.read_excel(self.input_file, sheet_name="data")
        self.df2 = pd.read_excel(self.input_file, sheet_name="data")

        if "pid" not in self.df1.columns or "pid" not in self.df2.columns:
            raise ValueError("Both sheets must contain 'pid' column")

        self.df1.set_index("pid", inplace=True)
        self.df2.set_index("pid", inplace=True)

    # -----------------------------
    # Compare Sheet1 vs Sheet2
    # -----------------------------
    def _compare(self):
        common_pids = self.df1.index.intersection(self.df2.index)

        for pid in common_pids:
            for col in self.COMPARE_COLUMNS:
                v1 = self.df1.at[pid, col]
                v2 = self.df2.at[pid, col]

                if pd.isna(v1) and pd.isna(v2):
                    continue

                if v1 != v2:
                    self.differences.setdefault(pid, {})
                    self.differences[pid][col] = {"old": v1, "new": v2}

    # -----------------------------
    # Apply updates to Sheet 1
    # -----------------------------
    def _apply_updates(self):
        for pid, cols in self.differences.items():
            for col, values in cols.items():
                self.df1.at[pid, col] = values["new"]

    # -----------------------------
    # Build audit DataFrame
    # -----------------------------
    def _build_audit(self) -> pd.DataFrame:
        audit_rows = []

        for pid, cols in self.differences.items():
            base_row = self.df1.loc[pid].to_dict()
            base_row["pid"] = pid

            for col, values in cols.items():
                audit_rows.append({
                    **base_row,
                    "changed_column": col,
                    "old_value": values["old"],
                    "new_value": values["new"]
                })

        return pd.DataFrame(audit_rows)

    # -----------------------------
    # Build summary DataFrame
    # -----------------------------
    def _build_summary(self) -> pd.DataFrame:
        return pd.DataFrame({
            "metric": ["Total pids with differences"],
            "count": [len(self.differences)]
        })

    # -----------------------------
    # Resolve output file path
    # -----------------------------
    def _resolve_output_path(self) -> Path:
        date_str = datetime.now().strftime("%Y%m%d")
        weekday = datetime.now().strftime("%a").upper()
        base_name = f"{weekday}WD{date_str}.xlsx"

        output_path = self.output_dir / base_name
        counter = 1

        while output_path.exists():
            output_path = self.output_dir / f"{weekday}WD{date_str}_{counter}.xlsx"
            counter += 1

        return output_path

    # -----------------------------
    # Run full reconciliation
    # -----------------------------
    def run(self):
        self._load_data()
        self._compare()
        self._apply_updates()

        updated_df = self.df1.reset_index()
        summary_df = self._build_summary()
        audit_df = self._build_audit()

        output_path = self._resolve_output_path()

        with pd.ExcelWriter(output_path, engine="xlsxwriter") as writer:
            updated_df.to_excel(writer, sheet_name="Updated_Data", index=False)
            summary_df.to_excel(writer, sheet_name="Summary", index=False)
            audit_df.to_excel(writer, sheet_name="Audit_Details", index=False)

        print(f"Reconciliation completed successfully: {output_path}")
