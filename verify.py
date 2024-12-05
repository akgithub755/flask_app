# 

import tkinter as tk
from tkinter import ttk
import pandas as pd

# Dummy dataset
data = {
    'a1': ['test1', None, 'test7'],
    'a2': ['test2', 'test5', 'test1'],
    'a3': ['test3', 'test1', None],
    'extra1': [10, 20, 30],
    'extra2': [40, 50, 60]
}

df = pd.DataFrame(data)

def populate_dropdown():
    # Collect unique non-None values from a1, a2, a3
    unique_values = set(df[['a1', 'a2', 'a3']].stack().dropna())
    search_entry['values'] = sorted(unique_values)

def search_data():
    selected_value = search_entry.get().strip()
    if not selected_value:
        result_label.config(text="Please enter or select a value.")
        return

    # Find all columns containing the selected value
    matched_columns = [col for col in ['a1', 'a2', 'a3'] if selected_value in df[col].values]
    if matched_columns:
        column_info_label.config(text=f"Value found in columns: {', '.join(matched_columns)}")
        
        # Filter rows where the selected value exists in any of the matched columns
        filtered_df = df[df[matched_columns].apply(lambda row: selected_value in row.values, axis=1)]
        filtered_df = filtered_df[['a1', 'a2', 'a3']].dropna(how='all', axis=1)
        
        # Remove columns containing only None values for the current search
        filtered_df = filtered_df.applymap(lambda x: x if pd.notna(x) else '')
        display_results(filtered_df, selected_value)
    else:
        result_label.config(text="No matching results found.")
        tree.delete(*tree.get_children())
        tree["columns"] = ()
        column_info_label.config(text="")

def display_results(filtered_df, search_value):
    result_label.config(text=f"Results for '{search_value}':")
    tree.delete(*tree.get_children())
    tree["columns"] = list(filtered_df.columns)
    
    for col in filtered_df.columns:
        tree.heading(col, text=col)
        tree.column(col, anchor=tk.CENTER, width=100)
    
    for _, row in filtered_df.iterrows():
        # Filter out empty values from the row
        tree.insert("", tk.END, values=[value for value in row if value])

def clear_data():
    tree.delete(*tree.get_children())
    tree["columns"] = ()
    result_label.config(text="")
    column_info_label.config(text="")
    search_entry.set('')

# Initialize the Tkinter window
root = tk.Tk()
root.title("Search App")
root.geometry("650x600")

# Title
title_label = tk.Label(root, text="Linkage", font=("Helvetica", 16, "bold"))
title_label.pack(pady=10)

# Input field and dropdown combo
input_frame = tk.Frame(root)
input_frame.pack(pady=5)

search_label = tk.Label(input_frame, text="Enter or select value:")
search_label.pack(side=tk.LEFT, padx=5)

search_entry = ttk.Combobox(input_frame, state="normal", width=30)
search_entry.pack(side=tk.LEFT, padx=5)

populate_dropdown()

# Buttons for Search and Clear
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

search_button = tk.Button(button_frame, text="Search", command=search_data)
search_button.pack(side=tk.LEFT, padx=10)

clear_button = tk.Button(button_frame, text="Clear", command=clear_data)
clear_button.pack(side=tk.LEFT, padx=10)

# Column info label
column_info_label = tk.Label(root, text="", font=("Arial", 10))
column_info_label.pack(pady=5)

# Result label
result_label = tk.Label(root, text="")
result_label.pack(pady=5)

# Treeview for displaying results
tree_frame = tk.Frame(root, padx=10, pady=10)
tree_frame.pack(fill=tk.BOTH, expand=True)

tree = ttk.Treeview(tree_frame, show="headings")
tree.pack(pady=10, fill=tk.BOTH, expand=True)

# Add padding and configure layout
root.pack_propagate(False)
tree_frame.pack_propagate(False)
tree_frame.config(padx=20, pady=20)

# Run the Tkinter event loop
root.mainloop()
