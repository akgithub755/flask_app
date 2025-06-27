import pandas as pd
import tkinter as tk
from tkinter import ttk

# Sample Dataset 1
df1 = pd.DataFrame({
    'a1': ['A1', 'A2', 'A3', 'A1', 'A2'],
    'b1': ['x', 'y', 'z', 'x', 'm'],
    'c1': ['A1', 'C2', 'C3', 'A1', 'C2'],
    'd1': ['p', 'x', 'r', 's', 'x']
})

# Sample Dataset 2
df2 = pd.DataFrame({
    'alpha': ['A1', 'B2', 'B3', 'A1', 'B2'],
    'beta': ['z', 'm', 'x', 'x', 'y'],
    'gamma': ['D1', 'D2', 'D3', 'D1', 'D2'],
    'delta': ['A1', 'z', 'r', 'A1', 'z']
})

datasets = {
    "Dataset 1": df1,
    "Dataset 2": df2
}

# Tkinter Setup
root = tk.Tk()
root.title("Live Column Search by Value")

# Dataset Selector
ttk.Label(root, text="Select Dataset:").pack()
selected_dataset = tk.StringVar()
dataset_dropdown = ttk.Combobox(root, textvariable=selected_dataset, values=list(datasets.keys()), state="readonly")
dataset_dropdown.pack()
dataset_dropdown.set("Dataset 1")  # Default selection

# Value Entry
ttk.Label(root, text="Enter value to search:").pack()
search_value = tk.StringVar()
value_entry = ttk.Entry(root, textvariable=search_value)
value_entry.pack()

# Result Dropdown
ttk.Label(root, text="Columns containing the value:").pack()
col_result_var = tk.StringVar()
column_dropdown = ttk.Combobox(root, textvariable=col_result_var, state="readonly")
column_dropdown.pack()

# Function to update column list on value change
def update_column_dropdown(*args):
    val = search_value.get()
    ds_name = selected_dataset.get()
    if not val or not ds_name:
        column_dropdown['values'] = []
        column_dropdown.set('')
        return

    df = datasets[ds_name]
    matching_cols = [col for col in df.columns if df[col].astype(str).eq(val).any()]
    column_dropdown['values'] = matching_cols
    if matching_cols:
        column_dropdown.set(matching_cols[0])
    else:
        column_dropdown.set('')

# Bind text changes to update function
search_value.trace_add("write", update_column_dropdown)
dataset_dropdown.bind("<<ComboboxSelected>>", update_column_dropdown)

root.mainloop()
