import pandas as pd
from pathlib import Path
from datetime import datetime


class ExcelReconciler:
    COMPARE_COLUMNS = ["a", "b", "c"]

    def __init__(self, excel1: str, excel2: str, output_dir: str = None):
        self.excel1 = excel1
        self.excel2 = excel2
        self.output_dir = Path(output_dir) if output_dir else Path(__file__).parent

        self.df_old = None
        self.df_new = None
        self.differences = {}

    # -----------------------------
    # Load Excel data
    # -----------------------------
    def _load_data(self):
        self.df_old = pd.read_excel(self.excel1, sheet_name="data")
        self.df_new = pd.read_excel(self.excel2, sheet_name="data")

        for df, name in [(self.df_old, "excel1"), (self.df_new, "excel2")]:
            if "pid" not in df.columns:
                raise ValueError(f"'pid' column missing in {name}")

        self.df_old.set_index("pid", inplace=True)
        self.df_new.set_index("pid", inplace=True)

    # -----------------------------
    # Compare ONLY common PIDs
    # -----------------------------
    def _compare(self):
        self.differences.clear()

        # ✅ IMPORTANT CHANGE
        common_pids = self.df_old.index.intersection(self.df_new.index)

        for pid in common_pids:
            for col in self.COMPARE_COLUMNS:
                old_val = self.df_old.at[pid, col]
                new_val = self.df_new.at[pid, col]

                # Ignore NaN vs NaN
                if pd.isna(old_val) and pd.isna(new_val):
                    continue

                if old_val != new_val:
                    self.differences.setdefault(pid, {})
                    self.differences[pid][col] = {
                        "old": old_val,
                        "new": new_val
                    }

    # -----------------------------
    # Apply updates to Excel1 data
    # -----------------------------
    def _apply_updates(self):
        for pid, cols in self.differences.items():
            for col, values in cols.items():
                self.df_old.at[pid, col] = values["new"]

    # -----------------------------
    # Build audit DataFrame
    # -----------------------------
    def _build_audit(self) -> pd.DataFrame:
        audit_rows = []

        for pid, cols in self.differences.items():
            original_row = self.df_old.loc[pid].to_dict()
            original_row["pid"] = pid

            for col, values in cols.items():
                audit_rows.append({
                    **original_row,
                    "changed_column": col,
                    "old_value": values["old"],
                    "new_value": values["new"]
                })

        return pd.DataFrame(audit_rows)

    # -----------------------------
    # Build summary with PID list
    # -----------------------------
    def _build_summary(self) -> pd.DataFrame:
        impacted_pids = list(self.differences.keys())

        return pd.DataFrame({
            "metric": [
                "Total pids with differences",
                "Impacted pids"
            ],
            "value": [
                len(impacted_pids),
                ", ".join(map(str, impacted_pids)) if impacted_pids else "None"
            ]
        })

    # -----------------------------
    # Resolve output path
    # -----------------------------
    def _resolve_output_path(self) -> Path:
        weekday = datetime.now().strftime("%a").upper()
        date_str = datetime.now().strftime("%Y%m%d")
        base_name = f"{weekday}WD{date_str}.xlsx"

        path = self.output_dir / base_name
        counter = 1

        while path.exists():
            path = self.output_dir / f"{weekday}WD{date_str}_{counter}.xlsx"
            counter += 1

        return path

    # -----------------------------
    # Run reconciliation
    # -----------------------------
    def run(self):
        self._load_data()
        self._compare()
        self._apply_updates()

        updated_df = self.df_old.reset_index()
        summary_df = self._build_summary()
        audit_df = self._build_audit()

        output_path = self._resolve_output_path()

        with pd.ExcelWriter(output_path, engine="xlsxwriter") as writer:
            updated_df.to_excel(writer, sheet_name="Updated_Data", index=False)
            summary_df.to_excel(writer, sheet_name="Summary", index=False)
            audit_df.to_excel(writer, sheet_name="Audit_Details", index=False)

        print(f"Reconciliation completed successfully: {output_path}")
