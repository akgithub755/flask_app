import tkinter as tk
from tkinter import ttk
import pandas as pd

# Example datasets
dataset1 = pd.DataFrame({
    'a1': ['test1', None, 'test7'],
    'a2': ['test2', 'test5', 'test1'],
    'a3': ['test3', 'test1', None],
    'm1': [100, 200, 300],
    'm2': [400, 500, 600],
    'm3': [700, 800, 900]
})

dataset2 = pd.DataFrame({
    'b1': ['apple', 'banana', None],
    'b2': ['grape', None, 'mango'],
    'b3': ['cherry', 'peach', 'apple'],
    'n1': [1.1, 2.2, 3.3],
    'n2': [4.4, 5.5, 6.6],
    'n3': [7.7, 8.8, 9.9]
})

# Define datasets with dropdown and display columns
datasets = {
    "Dataset 1": {
        "df": dataset1,
        "dropdown_cols": ['a1', 'a2', 'a3'],  # For dropdown values
        "display_cols": ['a1', 'm1', 'a2', 'm2', 'a3', 'm3']  # For UI display
    },
    "Dataset 2": {
        "df": dataset2,
        "dropdown_cols": ['b1', 'b2', 'b3'],  # For dropdown values
        "display_cols": ['b1', 'n1', 'b2', 'n2', 'b3', 'n3']  # For UI display
    }
}

# Initialize the current dataset, dropdown columns, and display columns
current_dataset = dataset1.copy()
dropdown_columns = ['a1', 'a2', 'a3']
display_columns = ['a1', 'm1', 'a2', 'm2', 'a3', 'm3']


def update_dropdown():
    """Update the value dropdown based on the current dataset."""
    unique_values = set(current_dataset[dropdown_columns].stack().dropna().astype(str))
    search_entry['values'] = sorted(unique_values)
    search_entry.set('')


def switch_dataset(event):
    """Switch dataset and update UI dynamically."""
    global current_dataset, dropdown_columns, display_columns
    dataset_name = dataset_dropdown.get()
    if dataset_name in datasets:
        dataset_info = datasets[dataset_name]
        current_dataset = dataset_info["df"]
        dropdown_columns = dataset_info["dropdown_cols"]
        display_columns = dataset_info["display_cols"]
        update_dropdown()


def search_data():
    """Search for the selected value in the current dataset and display results."""
    search_value = search_entry.get().strip()

    if not search_value:
        result_label.config(text="Please enter or select a value.")
        tree.delete(*tree.get_children())
        return

    # Filter rows containing the search value in any of the dropdown columns
    matched_rows = current_dataset[dropdown_columns].apply(
        lambda row: search_value in row.astype(str).values, axis=1
    )
    filtered_df = current_dataset.loc[matched_rows, display_columns]

    # Remove columns with None values for each row
    filtered_df = filtered_df.apply(lambda row: row.dropna(), axis=1)

    if filtered_df.empty:
        result_label.config(text=f"No results found for '{search_value}'.")
        tree.delete(*tree.get_children())
        return

    result_label.config(text=f"Results for '{search_value}':")
    display_results(filtered_df)


def display_results(filtered_df):
    """Display filtered results in the treeview."""
    tree.delete(*tree.get_children())

    # Dynamically set columns based on the filtered data
    all_columns = filtered_df.columns.tolist()
    tree["columns"] = all_columns

    for col in all_columns:
        tree.heading(col, text=col)
        tree.column(col, anchor=tk.CENTER, width=100)

    for _, row in filtered_df.iterrows():
        tree.insert("", tk.END, values=list(row))


def clear_data():
    """Clear search results and reset the dropdown."""
    tree.delete(*tree.get_children())
    tree["columns"] = ()
    result_label.config(text="")
    search_entry.set('')


# Initialize Tkinter window
root = tk.Tk()
root.title("Dynamic Dataset Search Tool")
root.geometry("900x600")

# Title
title_label = tk.Label(root, text="Dynamic Dataset Search", font=("Helvetica", 16, "bold"))
title_label.pack(pady=10)

# Dataset selection dropdown
dataset_frame = tk.Frame(root)
dataset_frame.pack(pady=5)

dataset_label = tk.Label(dataset_frame, text="Select Dataset:")
dataset_label.pack(side=tk.LEFT, padx=5)

dataset_dropdown = ttk.Combobox(dataset_frame, state="readonly", values=list(datasets.keys()), width=30)
dataset_dropdown.pack(side=tk.LEFT, padx=5)
dataset_dropdown.bind("<<ComboboxSelected>>", switch_dataset)
dataset_dropdown.set("Dataset 1")  # Default selection

# Search entry dropdown
input_frame = tk.Frame(root)
input_frame.pack(pady=5)

search_label = tk.Label(input_frame, text="Enter or Select Value:")
search_label.pack(side=tk.LEFT, padx=5)

search_entry = ttk.Combobox(input_frame, state="normal", width=30)
search_entry.pack(side=tk.LEFT, padx=5)

# Buttons for Search and Clear
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

search_button = tk.Button(button_frame, text="Search", command=search_data)
search_button.pack(side=tk.LEFT, padx=10)

clear_button = tk.Button(button_frame, text="Clear", command=clear_data)
clear_button.pack(side=tk.LEFT, padx=10)

# Result label
result_label = tk.Label(root, text="")
result_label.pack(pady=5)

# Treeview for displaying results
tree_frame = tk.Frame(root, padx=10, pady=10)
tree_frame.pack(fill=tk.BOTH, expand=True)

tree = ttk.Treeview(tree_frame, show="headings")
tree.pack(pady=10, fill=tk.BOTH, expand=True)

# Initialize dropdown values
update_dropdown()

# Run the Tkinter event loop
root.mainloop()
