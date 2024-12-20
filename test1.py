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



import tkinter as tk
from tkinter import ttk
import pandas as pd
from tkinter import messagebox

# Example datasets
dataset1 = pd.DataFrame({
    'a1': ['test1', None, 'test7'],
    'a2': ['test2', 'test5', 'test1'],
    'a3': ['test3', 'test1', None],
    'm1': [100, 200, 300],
    'm2': [400, 500, 600],
    'm3': [700, 800, 900],
    'bl1': ['extra1', 'extra2', 'extra3'],
    'bl2': ['more1', 'more2', 'more3']
})

dataset2 = pd.DataFrame({
    'b1': ['apple', 'banana', None],
    'b2': ['grape', None, 'mango'],
    'b3': ['cherry', 'peach', 'apple'],
    'n1': [1.1, 2.2, 3.3],
    'n2': [4.4, 5.5, 6.6],
    'n3': [7.7, 8.8, 9.9],
    'bl1': ['extraA', 'extraB', 'extraC'],
    'bl2': ['moreA', 'moreB', 'moreC']
})

# Define datasets with dropdown and display columns
datasets = {
    "Dataset 1": {
        "df": dataset1,
        "dropdown_cols": ['a1', 'a2', 'a3'],
        "display_cols": ['a1', 'm1', 'a2', 'm2', 'a3', 'm3'],
        "extra_cols": ['bl1', 'bl2']
    },
    "Dataset 2": {
        "df": dataset2,
        "dropdown_cols": ['b1', 'b2', 'b3'],
        "display_cols": ['b1', 'n1', 'b2', 'n2', 'b3', 'n3'],
        "extra_cols": ['bl1', 'bl2']
    }
}

current_dataset = dataset1.copy()
dropdown_columns = ['a1', 'a2', 'a3']
display_columns = ['a1', 'm1', 'a2', 'm2', 'a3', 'm3']
extra_columns = ['bl1', 'bl2']
matching_rows = pd.DataFrame()  # Store the filtered rows for extra column display


def update_dropdown():
    unique_values = set(current_dataset[dropdown_columns].stack().dropna().astype(str))
    search_entry['values'] = sorted(unique_values)
    search_entry.set('')


def switch_dataset(event):
    global current_dataset, dropdown_columns, display_columns, extra_columns
    dataset_name = dataset_dropdown.get()
    if dataset_name in datasets:
        dataset_info = datasets[dataset_name]
        current_dataset = dataset_info["df"]
        dropdown_columns = dataset_info["dropdown_cols"]
        display_columns = dataset_info["display_cols"]
        extra_columns = dataset_info["extra_cols"]
        update_dropdown()


def search_data():
    global matching_rows
    search_value = search_entry.get().strip()

    if not search_value:
        result_label.config(text="Please enter or select a value.")
        tree.delete(*tree.get_children())
        extra_tree.delete(*extra_tree.get_children())
        return

    # Filter the rows based on the entered search value
    matched_rows = current_dataset[dropdown_columns].apply(
        lambda row: search_value in row.astype(str).values, axis=1
    )
    matching_rows = current_dataset.loc[matched_rows, display_columns]

    matching_rows = matching_rows.apply(lambda row: row.dropna(), axis=1)

    if matching_rows.empty:
        result_label.config(text=f"No results found for '{search_value}'.")
        tree.delete(*tree.get_children())
        extra_tree.delete(*extra_tree.get_children())
        return

    result_label.config(text=f"Results for '{search_value}':")
    display_results(matching_rows)


def display_results(filtered_df):
    tree.delete(*tree.get_children())
    tree["columns"] = filtered_df.columns.tolist()

    for col in filtered_df.columns:
        tree.heading(col, text=col)
        tree.column(col, anchor=tk.CENTER, width=100)

    for _, row in filtered_df.iterrows():
        tree.insert("", tk.END, values=list(row))


def display_extra_columns():
    # Display extra columns only for the matched rows from the search
    if matching_rows.empty:
        extra_label.config(text="No extra columns to display.")
        return

    # Extract the matched rows
    matched_extra_df = current_dataset.loc[matching_rows.index]

    # Get the selected value from the extra column dropdown
    selected_extra_col = extra_col_dropdown.get()

    # Determine which extra columns to display based on the selected value
    if selected_extra_col == "Both":
        selected_columns = extra_columns  # Display both bl1 and bl2
    elif selected_extra_col == "bl1":
        selected_columns = ['bl1']  # Display only bl1
    elif selected_extra_col == "bl2":
        selected_columns = ['bl2']  # Display only bl2
    else:
        selected_columns = []  # No columns selected

    # Select the relevant extra columns
    matched_extra_df = matched_extra_df[selected_columns]

    # Clear the treeview and set up columns
    extra_tree.delete(*extra_tree.get_children())
    extra_tree["columns"] = matched_extra_df.columns.tolist()

    if matched_extra_df.empty:
        extra_label.config(text="No extra columns to display.")
        return

    extra_label.config(text="Extra Columns:")

    # Add headers for extra columns
    for col in matched_extra_df.columns:
        extra_tree.heading(col, text=col)
        extra_tree.column(col, anchor=tk.CENTER, width=100)

    # Insert rows for extra columns
    for _, row in matched_extra_df.iterrows():
        extra_tree.insert("", tk.END, values=list(row))


def clear_data():
    tree.delete(*tree.get_children())
    tree["columns"] = ()
    extra_tree.delete(*extra_tree.get_children())
    extra_tree["columns"] = ()
    result_label.config(text="")
    extra_label.config(text="")
    search_entry.set('')
    global matching_rows
    matching_rows = pd.DataFrame()  # Reset matching rows


def export_to_excel():
    # Collect data from the UI
    tree_data = []
    for item in tree.get_children():
        tree_data.append(tree.item(item, "values"))
    
    extra_tree_data = []
    for item in extra_tree.get_children():
        extra_tree_data.append(extra_tree.item(item, "values"))

    # Create a DataFrame to combine data
    if tree_data:
        tree_df = pd.DataFrame(tree_data, columns=tree["columns"])
    else:
        tree_df = pd.DataFrame()

    if extra_tree_data:
        extra_tree_df = pd.DataFrame(extra_tree_data, columns=extra_tree["columns"])
    else:
        extra_tree_df = pd.DataFrame()

    # Save the data to an Excel file
    with pd.ExcelWriter("output_data.xlsx", engine="xlsxwriter") as writer:
        if not tree_df.empty:
            tree_df.to_excel(writer, sheet_name="Main Data", index=False)
        if not extra_tree_df.empty:
            extra_tree_df.to_excel(writer, sheet_name="Extra Columns", index=False)

    messagebox.showinfo("Export Complete", "Data exported to 'output_data.xlsx' successfully!")


root = tk.Tk()
root.title("Dynamic Dataset Search Tool")
root.geometry("900x800")

title_label = tk.Label(root, text="Dynamic Dataset Search", font=("Helvetica", 16, "bold"))
title_label.pack(pady=10)

dataset_frame = tk.Frame(root)
dataset_frame.pack(pady=5)

dataset_label = tk.Label(dataset_frame, text="Select Dataset:")
dataset_label.pack(side=tk.LEFT, padx=5)

dataset_dropdown = ttk.Combobox(dataset_frame, state="readonly", values=list(datasets.keys()), width=30)
dataset_dropdown.pack(side=tk.LEFT, padx=5)
dataset_dropdown.bind("<<ComboboxSelected>>", switch_dataset)
dataset_dropdown.set("Dataset 1")

# Add search and extra columns widgets
input_frame = tk.Frame(root)
input_frame.pack(pady=5)

search_label = tk.Label(input_frame, text="Enter or Select Value:")
search_label.pack(side=tk.LEFT, padx=5)

search_entry = ttk.Combobox(input_frame, state="normal", width=30)
search_entry.pack(side=tk.LEFT, padx=5)

# Moving 'Select Extra Columns' dropdown here
extra_dropdown_frame = tk.Frame(root)
extra_dropdown_frame.pack(pady=5)

extra_col_label = tk.Label(extra_dropdown_frame, text="Select Extra Columns:")
extra_col_label.pack(side=tk.LEFT, padx=5)

extra_col_dropdown = ttk.Combobox(extra_dropdown_frame, state="readonly", values=["Both", "bl1", "bl2"], width=30)
extra_col_dropdown.pack(side=tk.LEFT, padx=5)
extra_col_dropdown.set("Both")

# Updated button layout
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

search_button = tk.Button(button_frame, text="Search", command=search_data)
search_button.pack(side=tk.LEFT, padx=10)

extra_button = tk.Button(button_frame, text="Display Extra Columns", command=display_extra_columns)
extra_button.pack(side=tk.LEFT, padx=10)

clear_button = tk.Button(button_frame, text="Clear", command=clear_data)
clear_button.pack(side=tk.LEFT, padx=10)

export_button = tk.Button(button_frame, text="Export to Excel", command=export_to_excel)
export_button.pack(side=tk.LEFT, padx=10)

result_label = tk.Label(root, text="")
result_label.pack(pady=5)

# Merging output window
output_frame = tk.Frame(root, padx=10, pady=10)
output_frame.pack(fill=tk.BOTH, expand=True)

# Create combined tree view
tree_frame = tk.Frame(output_frame)
tree_frame.pack(fill=tk.BOTH, expand=True)

tree = ttk.Treeview(tree_frame, show="headings")
tree.pack(pady=10, fill=tk.BOTH, expand=True)

extra_label = tk.Label(output_frame, text="")
extra_label.pack(pady=5)

extra_tree_frame = tk.Frame(output_frame, padx=10, pady=10)
extra_tree_frame.pack(fill=tk.BOTH, expand=True)

extra_tree = ttk.Treeview(extra_tree_frame, show="headings")
extra_tree.pack(pady=10, fill=tk.BOTH, expand=True)

# Initial dropdown and dataset setup
update_dropdown()

root.mainloop()

























import tkinter as tk
from tkinter import ttk
import pandas as pd
from tkinter import messagebox

# Example datasets
dataset1 = pd.DataFrame({
    'a1': ['test1', None, 'test7'],
    'a2': ['test2', 'test5', 'test1'],
    'a3': ['test3', 'test1', None],
    'm1': [100, 200, 300],
    'm2': [400, 500, 600],
    'm3': [700, 800, 900],
    'bl1': ['extra1', 'extra2', 'extra3'],
    'bl2': ['more1', 'more2', 'more3']
})

dataset2 = pd.DataFrame({
    'b1': ['apple', 'banana', None],
    'b2': ['grape', None, 'mango'],
    'b3': ['cherry', 'peach', 'apple'],
    'n1': [1.1, 2.2, 3.3],
    'n2': [4.4, 5.5, 6.6],
    'n3': [7.7, 8.8, 9.9],
    'bt1': ['extraA', 'extraB', 'extraC'],
    'bt2': ['moreA', 'moreB', 'moreC']
})

# Define datasets with dropdown and display columns
datasets = {
    "Dataset 1": {
        "df": dataset1,
        "dropdown_cols": ['a1', 'a2', 'a3'],
        "display_cols": ['a1', 'm1', 'a2', 'm2', 'a3', 'm3'],
        "extra_cols": ['bl1', 'bl2']  # Dataset 1 extra columns
    },
    "Dataset 2": {
        "df": dataset2,
        "dropdown_cols": ['b1', 'b2', 'b3'],
        "display_cols": ['b1', 'n1', 'b2', 'n2', 'b3', 'n3'],
        "extra_cols": ['bt1', 'bt2']  # Dataset 2 extra columns
    }
}


current_dataset = dataset1.copy()
dropdown_columns = ['a1', 'a2', 'a3']
display_columns = ['a1', 'm1', 'a2', 'm2', 'a3', 'm3']
extra_columns = ['bl1', 'bl2']
matching_rows = pd.DataFrame()  # Store the filtered rows for extra column display


def update_dropdown():
    unique_values = set(current_dataset[dropdown_columns].stack().dropna().astype(str))
    search_entry['values'] = sorted(unique_values)
    search_entry.set('')


def update_extra_columns_dropdown():
    extra_col_dropdown['values'] = ['Both'] + extra_columns
    extra_col_dropdown.set('Both')


def switch_dataset(event):
    global current_dataset, dropdown_columns, display_columns, extra_columns
    dataset_name = dataset_dropdown.get()
    if dataset_name in datasets:
        dataset_info = datasets[dataset_name]
        current_dataset = dataset_info["df"]
        dropdown_columns = dataset_info["dropdown_cols"]
        display_columns = dataset_info["display_cols"]
        extra_columns = dataset_info["extra_cols"]
        update_dropdown()
        update_extra_columns_dropdown()


def search_data():
    global matching_rows
    search_value = search_entry.get().strip()

    if not search_value:
        result_label.config(text="Please enter or select a value.")
        tree.delete(*tree.get_children())
        extra_tree.delete(*extra_tree.get_children())
        return

    # Filter the rows based on the entered search value
    matched_rows = current_dataset[dropdown_columns].apply(
        lambda row: search_value in row.astype(str).values, axis=1
    )
    matching_rows = current_dataset.loc[matched_rows, display_columns]

    matching_rows = matching_rows.apply(lambda row: row.dropna(), axis=1)

    if matching_rows.empty:
        result_label.config(text=f"No results found for '{search_value}'.")
        tree.delete(*tree.get_children())
        extra_tree.delete(*extra_tree.get_children())
        return

    result_label.config(text=f"Results for '{search_value}':")
    display_results(matching_rows)


def display_results(filtered_df):
    tree.delete(*tree.get_children())
    tree["columns"] = filtered_df.columns.tolist()

    for col in filtered_df.columns:
        tree.heading(col, text=col)
        tree.column(col, anchor=tk.CENTER, width=100)

    for _, row in filtered_df.iterrows():
        tree.insert("", tk.END, values=list(row))


def display_extra_columns():
    # Display extra columns only for the matched rows from the search
    if matching_rows.empty:
        extra_label.config(text="No extra columns to display.")
        return

    # Extract the matched rows
    matched_extra_df = current_dataset.loc[matching_rows.index]

    # Get the selected value from the extra column dropdown
    selected_extra_col = extra_col_dropdown.get()

    # Determine which extra columns to display based on the selected value
    if selected_extra_col == "Both":
        selected_columns = extra_columns  # Display both bl1 and bl2
    elif selected_extra_col == "bl1":
        selected_columns = ['bl1']  # Display only bl1
    elif selected_extra_col == "bl2":
        selected_columns = ['bl2']  # Display only bl2
    elif selected_extra_col == "bt1":
        selected_columns = ['bt1']  # Display only bl1
    elif selected_extra_col == "bt2":
        selected_columns = ['bt2']
    else:
        selected_columns = []  # No columns selected

    # Select the relevant extra columns
    matched_extra_df = matched_extra_df[selected_columns]

    # Clear the treeview and set up columns
    extra_tree.delete(*extra_tree.get_children())
    extra_tree["columns"] = matched_extra_df.columns.tolist()

    if matched_extra_df.empty:
        extra_label.config(text="No extra columns to display.")
        return

    extra_label.config(text="Extra Columns:")

    # Add headers for extra columns
    for col in matched_extra_df.columns:
        extra_tree.heading(col, text=col)
        extra_tree.column(col, anchor=tk.CENTER, width=100)

    # Insert rows for extra columns
    for _, row in matched_extra_df.iterrows():
        extra_tree.insert("", tk.END, values=list(row))


def clear_data():
    tree.delete(*tree.get_children())
    tree["columns"] = ()
    extra_tree.delete(*extra_tree.get_children())
    extra_tree["columns"] = ()
    result_label.config(text="")
    extra_label.config(text="")
    search_entry.set('')
    global matching_rows
    matching_rows = pd.DataFrame()  # Reset matching rows


def export_to_excel():
    # Collect data from the UI
    tree_data = []
    for item in tree.get_children():
        tree_data.append(tree.item(item, "values"))
    
    extra_tree_data = []
    for item in extra_tree.get_children():
        extra_tree_data.append(extra_tree.item(item, "values"))

    # Create a DataFrame to combine data
    if tree_data:
        tree_df = pd.DataFrame(tree_data, columns=tree["columns"])
    else:
        tree_df = pd.DataFrame()

    if extra_tree_data:
        extra_tree_df = pd.DataFrame(extra_tree_data, columns=extra_tree["columns"])
    else:
        extra_tree_df = pd.DataFrame()

    # Prepare input details
    input_details = {
        "Dataset": [dataset_dropdown.get()],
        "Searched Value": [search_entry.get()],
        "Selected Extra Columns": [extra_col_dropdown.get()]
    }
    input_df = pd.DataFrame(input_details)

    # Save the data to an Excel file
    with pd.ExcelWriter("output_data.xlsx", engine="xlsxwriter") as writer:
        if not input_df.empty:
            input_df.to_excel(writer, sheet_name="Input Data", index=False)
        if not tree_df.empty:
            tree_df.to_excel(writer, sheet_name="Main Data", index=False)
        if not extra_tree_df.empty:
            extra_tree_df.to_excel(writer, sheet_name="Extra Columns", index=False)

    messagebox.showinfo("Export Complete", "Data exported to 'output_data.xlsx' successfully!")



root = tk.Tk()
root.title("Dynamic Dataset Search Tool")
root.geometry("900x800")

title_label = tk.Label(root, text="Dynamic Dataset Search", font=("Helvetica", 16, "bold"))
title_label.pack(pady=10)

dataset_frame = tk.Frame(root)
dataset_frame.pack(pady=5)

dataset_label = tk.Label(dataset_frame, text="Select Dataset:")
dataset_label.pack(side=tk.LEFT, padx=5)

dataset_dropdown = ttk.Combobox(dataset_frame, state="readonly", values=list(datasets.keys()), width=30)
dataset_dropdown.pack(side=tk.LEFT, padx=5)
dataset_dropdown.bind("<<ComboboxSelected>>", switch_dataset)
dataset_dropdown.set("Dataset 1")

# Add search and extra columns widgets
input_frame = tk.Frame(root)
input_frame.pack(pady=5)

search_label = tk.Label(input_frame, text="Enter or Select Value:")
search_label.pack(side=tk.LEFT, padx=5)

search_entry = ttk.Combobox(input_frame, state="normal", width=30)
search_entry.pack(side=tk.LEFT, padx=5)

# Moving 'Select Extra Columns' dropdown here
extra_dropdown_frame = tk.Frame(root)
extra_dropdown_frame.pack(pady=5)

extra_col_label = tk.Label(extra_dropdown_frame, text="Select Extra Columns:")
extra_col_label.pack(side=tk.LEFT, padx=5)

extra_col_dropdown = ttk.Combobox(extra_dropdown_frame, state="readonly", values=["Both", "bl1", "bl2"], width=30)
extra_col_dropdown.pack(side=tk.LEFT, padx=5)
extra_col_dropdown.set("Both")

# Updated button layout
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

search_button = tk.Button(button_frame, text="Search", command=search_data)
search_button.pack(side=tk.LEFT, padx=10)

extra_button = tk.Button(button_frame, text="Display Extra Columns", command=display_extra_columns)
extra_button.pack(side=tk.LEFT, padx=10)

clear_button = tk.Button(button_frame, text="Clear", command=clear_data)
clear_button.pack(side=tk.LEFT, padx=10)

export_button = tk.Button(button_frame, text="Export to Excel", command=export_to_excel)
export_button.pack(side=tk.LEFT, padx=10)

result_label = tk.Label(root, text="")
result_label.pack(pady=5)

# Merging output window
output_frame = tk.Frame(root, padx=10, pady=10)
output_frame.pack(fill=tk.BOTH, expand=True)

# Create combined tree view
tree_frame = tk.Frame(output_frame)
tree_frame.pack(fill=tk.BOTH, expand=True)

tree = ttk.Treeview(tree_frame, show="headings")
tree.pack(pady=10, fill=tk.BOTH, expand=True)

extra_label = tk.Label(output_frame, text="")
extra_label.pack(pady=5)

extra_tree_frame = tk.Frame(output_frame, padx=10, pady=10)
extra_tree_frame.pack(fill=tk.BOTH, expand=True)

extra_tree = ttk.Treeview(extra_tree_frame, show="headings")
extra_tree.pack(pady=10, fill=tk.BOTH, expand=True)

# Initial dropdown and dataset setup
update_dropdown()

root.mainloop()










import tkinter as tk
from tkinter import ttk
import pandas as pd
from tkinter import messagebox

# Example datasets with source column
dataset1 = pd.DataFrame({
    'a1': ['test1', None, 'test7'],
    'a2': ['test2', 'test5', 'test1'],
    'a3': ['test3', 'test1', None],
    'm1': [100, 200, 300],
    'm2': [400, 500, 600],
    'm3': [700, 800, 900],
    'bl1': ['extra1', 'extra2', 'extra3'],
    'bl2': ['more1', 'more2', 'more3'],
    'source': ['s1', 's2', 's1']  # Added source column
})

dataset2 = pd.DataFrame({
    'b1': ['apple', 'banana', None],
    'b2': ['grape', None, 'mango'],
    'b3': ['cherry', 'peach', 'apple'],
    'n1': [1.1, 2.2, 3.3],
    'n2': [4.4, 5.5, 6.6],
    'n3': [7.7, 8.8, 9.9],
    'bt1': ['extraA', 'extraB', 'extraC'],
    'bt2': ['moreA', 'moreB', 'moreC'],
    'source': ['s1', 's2', 's2']  # Added source column
})

# Define datasets with dropdown and display columns
datasets = {
    "Dataset 1": {
        "df": dataset1,
        "dropdown_cols": ['a1', 'a2', 'a3'],
        "display_cols": ['a1', 'm1', 'a2', 'm2', 'a3', 'm3'],
        "extra_cols": ['bl1', 'bl2'],
        "sources": ['s1', 's2']  # Dataset 1 sources
    },
    "Dataset 2": {
        "df": dataset2,
        "dropdown_cols": ['b1', 'b2', 'b3'],
        "display_cols": ['b1', 'n1', 'b2', 'n2', 'b3', 'n3'],
        "extra_cols": ['bt1', 'bt2'],
        "sources": ['s1', 's2']  # Dataset 2 sources
    }
}

current_dataset = dataset1.copy()
dropdown_columns = ['a1', 'a2', 'a3']
display_columns = ['a1', 'm1', 'a2', 'm2', 'a3', 'm3']
extra_columns = ['bl1', 'bl2']
matching_rows = pd.DataFrame()  # Store the filtered rows for extra column display
current_source = 's1'  # Default source


def update_source_dropdown():
    source_dropdown['values'] = datasets[dataset_dropdown.get()]["sources"]
    source_dropdown.set(current_source)


def update_dropdown():
    # Filter the dataset by the current source
    filtered_df = current_dataset[current_dataset['source'] == current_source]
    
    # Get unique values from the relevant columns, drop any NaNs and convert to strings
    unique_values = set(filtered_df[dropdown_columns].stack().dropna().astype(str))
    
    # Update the search entry dropdown values with unique values from the selected source
    search_entry['values'] = sorted(unique_values)
    search_entry.set('')  # Clear the selected value



def update_extra_columns_dropdown():
    extra_col_dropdown['values'] = ['Both'] + extra_columns
    extra_col_dropdown.set('Both')


def switch_dataset(event):
    global current_dataset, dropdown_columns, display_columns, extra_columns, current_source
    dataset_name = dataset_dropdown.get()
    if dataset_name in datasets:
        dataset_info = datasets[dataset_name]
        current_dataset = dataset_info["df"]
        dropdown_columns = dataset_info["dropdown_cols"]
        display_columns = dataset_info["display_cols"]
        extra_columns = dataset_info["extra_cols"]
        current_source = dataset_info["sources"][0]  # Default source
        update_source_dropdown()
        update_dropdown()
        update_extra_columns_dropdown()


def switch_source(event):
    global current_source
    current_source = source_dropdown.get()
    update_dropdown()


def search_data():
    global matching_rows
    search_value = search_entry.get().strip()

    if not search_value:
        result_label.config(text="Please enter or select a value.")
        tree.delete(*tree.get_children())
        extra_tree.delete(*extra_tree.get_children())
        return

    # Filter the rows based on the entered search value
    matched_rows = current_dataset[current_source][dropdown_columns].apply(
        lambda row: search_value in row.astype(str).values, axis=1
    )
    matching_rows = current_dataset.loc[matched_rows, display_columns]

    matching_rows = matching_rows.apply(lambda row: row.dropna(), axis=1)

    if matching_rows.empty:
        result_label.config(text=f"No results found for '{search_value}'.")
        tree.delete(*tree.get_children())
        extra_tree.delete(*extra_tree.get_children())
        return

    result_label.config(text=f"Results for '{search_value}':")
    display_results(matching_rows)


def display_results(filtered_df):
    tree.delete(*tree.get_children())
    tree["columns"] = filtered_df.columns.tolist()

    for col in filtered_df.columns:
        tree.heading(col, text=col)
        tree.column(col, anchor=tk.CENTER, width=100)

    for _, row in filtered_df.iterrows():
        tree.insert("", tk.END, values=list(row))


def display_extra_columns():
    # Display extra columns only for the matched rows from the search
    if matching_rows.empty:
        extra_label.config(text="No extra columns to display.")
        return

    # Extract the matched rows
    matched_extra_df = current_dataset.loc[matching_rows.index]

    # Get the selected value from the extra column dropdown
    selected_extra_col = extra_col_dropdown.get()

    # Determine which extra columns to display based on the selected value
    if selected_extra_col == "Both":
        selected_columns = extra_columns  # Display both bl1 and bl2
    elif selected_extra_col == "bl1":
        selected_columns = ['bl1']  # Display only bl1
    elif selected_extra_col == "bl2":
        selected_columns = ['bl2']  # Display only bl2
    elif selected_extra_col == "bt1":
        selected_columns = ['bt1']  # Display only bt1
    elif selected_extra_col == "bt2":
        selected_columns = ['bt2']
    else:
        selected_columns = []  # No columns selected

    # Select the relevant extra columns
    matched_extra_df = matched_extra_df[selected_columns]

    # Clear the treeview and set up columns
    extra_tree.delete(*extra_tree.get_children())
    extra_tree["columns"] = matched_extra_df.columns.tolist()

    if matched_extra_df.empty:
        extra_label.config(text="No extra columns to display.")
        return

    extra_label.config(text="Extra Columns:")

    # Add headers for extra columns
    for col in matched_extra_df.columns:
        extra_tree.heading(col, text=col)
        extra_tree.column(col, anchor=tk.CENTER, width=100)

    # Insert rows for extra columns
    for _, row in matched_extra_df.iterrows():
        extra_tree.insert("", tk.END, values=list(row))


def clear_data():
    tree.delete(*tree.get_children())
    tree["columns"] = ()
    extra_tree.delete(*extra_tree.get_children())
    extra_tree["columns"] = ()
    result_label.config(text="")
    extra_label.config(text="")
    search_entry.set('')
    global matching_rows
    matching_rows = pd.DataFrame()  # Reset matching rows


def export_to_excel():
    # Collect data from the UI
    tree_data = []
    for item in tree.get_children():
        tree_data.append(tree.item(item, "values"))
    
    extra_tree_data = []
    for item in extra_tree.get_children():
        extra_tree_data.append(extra_tree.item(item, "values"))

    # Create a DataFrame to combine data
    if tree_data:
        tree_df = pd.DataFrame(tree_data, columns=tree["columns"])
    else:
        tree_df = pd.DataFrame()

    if extra_tree_data:
        extra_tree_df = pd.DataFrame(extra_tree_data, columns=extra_tree["columns"])
    else:
        extra_tree_df = pd.DataFrame()

    # Prepare input details
    input_details = {
        "Dataset": [dataset_dropdown.get()],
        "Searched Value": [search_entry.get()],
        "Selected Extra Columns": [extra_col_dropdown.get()],
        "Selected Source": [source_dropdown.get()]
    }
    input_df = pd.DataFrame(input_details)

    # Save the data to an Excel file
    with pd.ExcelWriter("output_data.xlsx", engine="xlsxwriter") as writer:
        if not input_df.empty:
            input_df.to_excel(writer, sheet_name="Input Data", index=False)
        if not tree_df.empty:
            tree_df.to_excel(writer, sheet_name="Main Data", index=False)
        if not extra_tree_df.empty:
            extra_tree_df.to_excel(writer, sheet_name="Extra Columns", index=False)

    messagebox.showinfo("Export Complete", "Data exported to 'output_data.xlsx' successfully!")


root = tk.Tk()
root.title("Dynamic Dataset Search Tool")
root.geometry("900x800")

title_label = tk.Label(root, text="Dynamic Dataset Search", font=("Helvetica", 16, "bold"))
title_label.pack(pady=10)

dataset_frame = tk.Frame(root)
dataset_frame.pack(pady=5)

dataset_label = tk.Label(dataset_frame, text="Select Dataset:")
dataset_label.pack(side=tk.LEFT, padx=5)

dataset_dropdown = ttk.Combobox(dataset_frame, state="readonly", values=list(datasets.keys()), width=30)
dataset_dropdown.pack(side=tk.LEFT, padx=5)
dataset_dropdown.bind("<<ComboboxSelected>>", switch_dataset)
dataset_dropdown.set("Dataset 1")

# Add source dropdown
source_frame = tk.Frame(root)
source_frame.pack(pady=5)

source_label = tk.Label(source_frame, text="Select Source:")
source_label.pack(side=tk.LEFT, padx=5)

source_dropdown = ttk.Combobox(source_frame, state="readonly", width=30)
source_dropdown.pack(side=tk.LEFT, padx=5)
source_dropdown.bind("<<ComboboxSelected>>", switch_source)

# Add search and extra columns widgets
input_frame = tk.Frame(root)
input_frame.pack(pady=5)

search_label = tk.Label(input_frame, text="Enter or Select Value:")
search_label.pack(side=tk.LEFT, padx=5)

search_entry = ttk.Combobox(input_frame, width=50)
search_entry.pack(side=tk.LEFT, padx=5)

# Add the tree view to display the main data
tree_frame = tk.Frame(root)
tree_frame.pack(pady=10)

tree = ttk.Treeview(tree_frame, show="headings")
tree.pack()

# Add the extra columns tree view
extra_tree_frame = tk.Frame(root)
extra_tree_frame.pack(pady=10)

extra_tree = ttk.Treeview(extra_tree_frame, show="headings")
extra_tree.pack()

# Display buttons and export functionality
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

search_button = tk.Button(button_frame, text="Search", command=search_data)
search_button.pack(side=tk.LEFT, padx=5)

clear_button = tk.Button(button_frame, text="Clear", command=clear_data)
clear_button.pack(side=tk.LEFT, padx=5)

extra_col_label = tk.Label(button_frame, text="Select Extra Columns:")
extra_col_label.pack(side=tk.LEFT, padx=5)

extra_col_dropdown = ttk.Combobox(button_frame, state="readonly", width=15)
extra_col_dropdown.pack(side=tk.LEFT, padx=5)

extra_col_button = tk.Button(button_frame, text="Show Extra Columns", command=display_extra_columns)
extra_col_button.pack(side=tk.LEFT, padx=5)

export_button = tk.Button(button_frame, text="Export to Excel", command=export_to_excel)
export_button.pack(side=tk.LEFT, padx=5)

# Initial setup
update_source_dropdown()
update_dropdown()

root.mainloop()





import pandas as pd
import tkinter as tk
from tkinter import ttk

# Sample datasets
data1 = {'source': ['a1', 'a2', 'a1'], 't1': [10, 20, 30], 't2': [40, 50, 60], 't3': [70, 80, 90]}
data2 = {'source': ['m1', 'm2', 'm3'], 'f1': [100, 200, 300], 'f2': [400, 500, 600], 'f3': [700, 800, 900]}

df1 = pd.DataFrame(data1)
df2 = pd.DataFrame(data2)

# Combine unique sources from both datasets
all_sources = sorted(set(df1['source']).union(set(df2['source'])))

# Function to filter data and update UI dynamically
def search():
    selected_source = source_var.get()
    if not selected_source:
        return

    # Clear the treeview
    for row in tree.get_children():
        tree.delete(row)

    # Check which dataset contains the selected source
    if selected_source in df1['source'].values:
        dataset = df1[df1['source'] == selected_source]
    elif selected_source in df2['source'].values:
        dataset = df2[df2['source'] == selected_source]
    else:
        return

    # Dynamically update treeview columns based on the dataset
    tree["columns"] = list(dataset.columns)
    for col in dataset.columns:
        tree.heading(col, text=col)
        tree.column(col, width=120)

    # Add rows to the treeview
    for _, row in dataset.iterrows():
        tree.insert('', 'end', values=row.tolist())

# Create the Tkinter window
root = tk.Tk()
root.title("Source Search Tool")

# Dropdown menu for sources
tk.Label(root, text="Select Source:").grid(row=0, column=0, padx=10, pady=10)
source_var = tk.StringVar()
source_dropdown = ttk.Combobox(root, textvariable=source_var, values=all_sources, state='readonly')
source_dropdown.grid(row=0, column=1, padx=10, pady=10)
source_dropdown.set("Select a source")

# Search button
search_button = tk.Button(root, text="Search", command=search)
search_button.grid(row=0, column=2, padx=10, pady=10)

# Treeview for displaying results
tree = ttk.Treeview(root, show='headings', height=10)
tree.grid(row=1, column=0, columnspan=3, padx=10, pady=10)

# Run the Tkinter event loop
root.mainloop()


