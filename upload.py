# # import pandas as pd

# # def process_excel_file(file_path):
# #     # Example logic: process the Excel file
# #     print(f"Processing file: {file_path}")
    
# #     df = pd.read_excel(file_path)
    
# #     print("File loaded successfully.")
# #     print(f"Number of rows: {df.shape[0]}")
# #     print("Sample data:")
# #     print(df.head())

# #     print('####################')
# #     print("File loaded successfully.")
# #     print(f"Number of rows: {df.shape[0]}")
# #     print("Sample data:")
# #     print(df.head())

# #     print('####################')
# #     print("File loaded successfully.")
# #     print(f"Number of rows: {df.shape[0]}")
# #     print("Sample data:")
# #     print(df.head())

# #     print('####################')
# #     print("File loaded successfully.")
# #     print(f"Number of rows: {df.shape[0]}")
# #     print("Sample data:")
# #     print(df.head())

# #     print('####################')
# #     print("File loaded successfully.")
# #     print(f"Number of rows: {df.shape[0]}")
# #     print("Sample data:")
# #     print(df.head())

# #     print('####################')
# #     print("File loaded successfully.")
# #     print(f"Number of rows: {df.shape[0]}")
# #     print("Sample data:")
# #     print(df.head())


# #     print('####################')
# #     print("File loaded successfully.")
# #     print(f"Number of rows: {df.shape[0]}")
# #     print("Sample data:")
# #     print(df.head())


# #     print('####################')
# #     print("File loaded successfully.")
# #     print(f"Number of rows: {df.shape[0]}")
# #     print("Sample data:")
# #     print(df.head())


# #     print('####################')
# #     print("File loaded successfully.")
# #     print(f"Number of rows: {df.shape[0]}")
# #     print("Sample data:")
# #     print(df.head())


# #     print('####################')
# #     print("File loaded successfully.")
# #     print(f"Number of rows: {df.shape[0]}")
# #     print("Sample data:")
# #     print(df.head())


# #     print('####################')
# #     print("File loaded successfully.")
# #     print(f"Number of rows: {df.shape[0]}")
# #     print("Sample data:")
# #     print(df.head())


    
# #     # Add any business logic you need here
# #     print("Processing complete.")

# import pandas as pd
# import time

# def process_excel_file(file_path):
#     # Example: Use yield to send logs to the client in real-time
#     yield f"Processing file: {file_path}"
    
#     try:
#         df = pd.read_excel(file_path)
#         yield "File loaded successfully."
#         yield f"Number of rows: {df.shape[0]}"
#         yield "Sample data:"
#         yield df.head().to_string()



#         df = pd.read_excel(file_path)
#         yield "File loaded successfully."
#         yield f"Number of rows: {df.shape[0]}"
#         yield "Sample data:"
#         yield df.head().to_string()


#         df = pd.read_excel(file_path)
#         yield "File loaded successfully."
#         yield f"Number of rows: {df.shape[0]}"
#         yield "Sample data:"
#         yield df.head().to_string()


#         df = pd.read_excel(file_path)
#         yield "File loaded successfully."
#         yield f"Number of rows: {df.shape[0]}"
#         yield "Sample data:"
#         yield df.head().to_string()


#         df = pd.read_excel(file_path)
#         yield "File loaded successfully."
#         yield f"Number of rows: {df.shape[0]}"
#         yield "Sample data:"
#         yield df.head().to_string()


#         df = pd.read_excel(file_path)
#         yield "File loaded successfully."
#         yield f"Number of rows: {df.shape[0]}"
#         yield "Sample data:"
#         yield df.head().to_string()
        
#         # Simulate longer processing
#         yield "Processing rows..."
#         for i in range(5):
#             yield f"Processed row {i + 1}"
#             time.sleep(1)  # Simulate time-consuming task
            
#         yield "Processing complete."
        
#     except Exception as e:
#         yield f"Error processing file: {e}"


import time

def process_file(file_path):
    yield "Starting file upload...\n"
    time.sleep(1)
    yield f"Processing file: {file_path}\n"
    time.sleep(2)
    yield "Performing some calculations...\n"
    time.sleep(2)
    yield "File upload and processing complete!\n"





import tkinter as tk
from tkinter import ttk
import pandas as pd
import ttkbootstrap as tb

# Sample DataFrame (Added "mex" column)
data = {
    "mex": ["Type A", "Type B", "Type C", "Type A", "Type B", "Type C"],
    "a1": ["Apple", "Banana", "Cherry", "Apple", "Banana", "Cherry"],
    "b1": ["Red", "Yellow", "Red", "Green", "Yellow", "Pink"],
    "c1": ["Small", "Medium", "Large", "Small", "Large", "Medium"],
    "d1": ["Fresh", "Rotten", "Fresh", "Rotten", "Fresh", "Rotten"],
    "e1": ["Yes", "No", "Yes", "No", "Yes", "No"]
}

df = pd.DataFrame(data)

# Extract unique values
checkbox_values = sorted(df["a1"].unique().tolist())
checkbox_values.insert(0, "All")  # Add "All" option

dropdown_values = {
    "mex": sorted(df["mex"].dropna().unique().tolist()),  # Add MEX column
    "b1": sorted(df["b1"].dropna().unique().tolist()),
    "c1": sorted(df["c1"].dropna().unique().tolist()),
    "d1": sorted(df["d1"].dropna().unique().tolist()),
    "e1": sorted(df["e1"].dropna().unique().tolist()),
}

# Initialize Tkinter Window
root = tb.Window(themename="cosmo")
root.title("Dynamic UI with DataFrame")
root.geometry("600x500")
root.resizable(False, False)

# -------- Left Section: Checkboxes (a1) -------- #
left_frame = ttk.Frame(root)
left_frame.pack(side="left", fill="y", padx=20, pady=20)

ttk.Label(left_frame, text="Select Option:", font=("Arial", 12, "bold")).pack(anchor="w", pady=5)

checkbox_vars = {}
checkbox_widgets = {}

def on_checkbox_click(selected_value):
    """Handles 'All' selection logic."""
    if selected_value == "All":
        if checkbox_vars["All"].get():
            # If "All" is checked, check and disable all checkboxes
            for key in checkbox_vars:
                checkbox_vars[key].set(1)
                checkbox_widgets[key].configure(state="disabled")
            checkbox_widgets["All"].configure(state="normal")  # Keep "All" clickable
        else:
            # If "All" is unchecked, enable all checkboxes again
            for key in checkbox_vars:
                checkbox_widgets[key].configure(state="normal")
    
    else:
        # If any other checkbox is clicked, enable all checkboxes and uncheck "All"
        checkbox_vars["All"].set(0)
        for key in checkbox_vars:
            checkbox_widgets[key].configure(state="normal")

# Create checkboxes
for value in checkbox_values:
    var = tk.IntVar()
    checkbox_vars[value] = var
    chk = ttk.Checkbutton(left_frame, text=value, variable=var, bootstyle="success-round-toggle",
                          command=lambda v=value: on_checkbox_click(v))
    chk.pack(anchor="w", pady=2)
    checkbox_widgets[value] = chk  # Store the widget reference

# -------- Middle Section: Dropdowns -------- #
middle_frame = ttk.Frame(root)
middle_frame.pack(side="left", expand=True, fill="both", padx=20, pady=20)

dropdown_vars = {}

def create_dropdown(label, column):
    ttk.Label(middle_frame, text=label, font=("Arial", 12, "bold")).pack(anchor="w", pady=5)
    var = tk.StringVar()
    combobox = ttk.Combobox(middle_frame, textvariable=var, values=["Select"] + dropdown_values[column], font=("Arial", 12), width=25)
    combobox.pack(fill="x", pady=3)
    combobox.set("Select")  # Default placeholder
    dropdown_vars[column] = var

# Create MEX dropdown at the top
create_dropdown("MEX", "mex")

# Create dropdowns for b1, c1, d1, e1
for col in ["b1", "c1", "d1", "e1"]:
    create_dropdown(col.upper(), col)

# -------- "Get Data" Button -------- #
def get_selected_data():
    # Get selected checkboxes (a1 column)
    selected_a1 = [key for key, var in checkbox_vars.items() if var.get()]

    # Handle "All" checkbox logic
    if "All" in selected_a1:
        selected_a1 = [""]  # Empty string if "All" is selected
    elif not selected_a1:  
        selected_a1 = [""]  # Return empty string if nothing is selected

    # Get selected dropdown values
    selected_mex = dropdown_vars["mex"].get() if dropdown_vars["mex"].get() != "Select" else ""
    selected_b1 = dropdown_vars["b1"].get() if dropdown_vars["b1"].get() != "Select" else ""
    selected_c1 = dropdown_vars["c1"].get() if dropdown_vars["c1"].get() != "Select" else ""
    selected_d1 = dropdown_vars["d1"].get() if dropdown_vars["d1"].get() != "Select" else ""
    selected_e1 = dropdown_vars["e1"].get() if dropdown_vars["e1"].get() != "Select" else ""

    # Print selected values
    print(f"a1: {selected_a1}, mex: '{selected_mex}', b1: '{selected_b1}', c1: '{selected_c1}', d1: '{selected_d1}', e1: '{selected_e1}'")

get_button = ttk.Button(middle_frame, text="Get Data", bootstyle="primary", width=15, command=get_selected_data)
get_button.pack(pady=20)

# Run Tkinter App
root.mainloop()










import pandas as pd
import tkinter as tk
from tkinter import ttk

# Sample DataFrame with long values
data = {
    "Column1": ["Very_Long_Value_Example_1", "Another_Long_String_Value_2", "Test_Value_3"],
    "Column2": ["Long_Text_XYZ_Example_1", "Sample_Long_Text_Example_2", "Different_Long_Text_3"],
    "Column3": ["Some_Long_Entry_1", "Another_Very_Long_Entry_2", "Short_Val_3"],
    "Column4": ["Random_Long_String_A", "More_Long_Text_B", "Different_Long_Text_C"]
}
df = pd.DataFrame(data)

TABLE_NAME = "your_table_name"
fields = {}

# Function to enable/disable SQL button
def check_fields(event=None):
    if any(fields[col].get() for col in df.columns):
        generate_sql_btn["state"] = "normal"
    else:
        generate_sql_btn["state"] = "disabled"

# Function to update dropdown dynamically based on selection
def update_filters(event=None):
    selected_values = {col: fields[col].get() for col in df.columns if fields[col].get()}
    filtered_df = df.copy()
    for col, val in selected_values.items():
        filtered_df = filtered_df[filtered_df[col] == val]
    for col in df.columns:
        if col not in selected_values:
            fields[col + "_combo"]["values"] = list(filtered_df[col].unique())
    check_fields()

# Function to reset all filters
def reset_filters():
    for col in df.columns:
        fields[col + "_combo"]["values"] = list(df[col].unique())
        fields[col].set("")
    generate_sql_btn["state"] = "disabled"

    # Function to generate SQL query (Fix for single quotes in values)
def generate_sql():
    conditions = []
    
    for col in df.columns:
        value = fields[col].get()
        if value:  # If the field has a value
            escaped_value = value.replace("'", "''")  # Escape single quotes for SQL
            conditions.append(f"{col} = '{escaped_value}'")  

    query = f"SELECT * FROM {TABLE_NAME};" if not conditions else f"SELECT * FROM {TABLE_NAME} WHERE " + " AND ".join(conditions) + ";"
    
    print(query)  # Print the final SQL query



# Create Tkinter Window
root = tk.Tk()
root.title("SQL Query Generator")
root.geometry("800x500")  # Expanded window size
root.resizable(False, False)

# Title Label
title_label = tk.Label(root, text="Generate SQL", font=("Arial", 16, "bold"))
title_label.pack(pady=10)

# Separator Line
separator = tk.Frame(root, height=2, bg="black")
separator.pack(fill="x", padx=50, pady=5)

# Form Frame
form_frame = tk.Frame(root)
form_frame.pack(expand=True, pady=20)

# Create input fields with dropdowns only
for i, column in enumerate(df.columns):
    tk.Label(form_frame, text=column, font=("Arial", 12)).grid(row=i, column=0, padx=10, pady=10, sticky="e")

    field_var = tk.StringVar()
    
    combo = ttk.Combobox(form_frame, textvariable=field_var, font=("Arial", 12), width=40, state="readonly")
    combo["values"] = list(df[column].unique())
    combo.grid(row=i, column=1, padx=10, pady=10, sticky="w")
    combo.bind("<<ComboboxSelected>>", update_filters)

    fields[column] = field_var
    fields[column + "_combo"] = combo

# Buttons
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

generate_sql_btn = tk.Button(button_frame, text="Generate SQL", command=generate_sql, font=("Arial", 12), state="disabled")
generate_sql_btn.grid(row=0, column=0, padx=10)

reset_btn = tk.Button(button_frame, text="Reset", command=reset_filters, font=("Arial", 12))
reset_btn.grid(row=0, column=1, padx=10)

# Run Tkinter event loop
root.mainloop()



import os
import random
import string

# Configuration
base_path = 'generated_folders'
main_folders = 10
sub_folders = 10
files_per_subfolder = 15
target_total_size_mb = 150
file_size_kb = int((target_total_size_mb * 1024) / (main_folders * sub_folders * files_per_subfolder))

# Create random content
def random_text(size):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=size))

# Main folder generation
os.makedirs(base_path, exist_ok=True)

for i in range(main_folders):
    main_folder = os.path.join(base_path, f'main_folder_{i+1}')
    os.makedirs(main_folder, exist_ok=True)

    for j in range(sub_folders):
        sub_folder = os.path.join(main_folder, f'sub_folder_{j+1}')
        os.makedirs(sub_folder, exist_ok=True)

        for k in range(files_per_subfolder):
            file_name = os.path.join(sub_folder, f'file_{k+1}.txt')
            with open(file_name, 'w') as f:
                f.write(random_text(file_size_kb * 1024))  # Convert KB to Bytes

print(f"✅ Folder structure with approx {target_total_size_mb}MB data created at: {os.path.abspath(base_path)}")

import os
import random
import string

# Configuration
base_dir = "generated_files"
num_folders = 5  # You can change this
min_files_per_folder = 5
max_files_per_folder = 15
small_file_size_range = (1 * 1024, 30 * 1024)    # 1KB to 30KB
large_file_size_range = (80 * 1024, 100 * 1024)  # 80KB to 100KB
large_file_probability = 0.2  # 20% of files will be large

def random_filename():
    return ''.join(random.choices(string.ascii_lowercase, k=8)) + ".txt"

def random_content(size):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=size))

# Create base directory
os.makedirs(base_dir, exist_ok=True)

for i in range(num_folders):
    folder_name = f"folder_{i+1}"
    folder_path = os.path.join(base_dir, folder_name)
    os.makedirs(folder_path, exist_ok=True)

    num_files = random.randint(min_files_per_folder, max_files_per_folder)

    for _ in range(num_files):
        is_large_file = random.random() < large_file_probability
        if is_large_file:
            size = random.randint(*large_file_size_range)
        else:
            size = random.randint(*small_file_size_range)

        file_path = os.path.join(folder_path, random_filename())

        # Write content to file
        with open(file_path, 'w') as f:
            f.write(random_content(size))

print(f"Files generated in '{base_dir}' with randomized sizes.")




import os
import random
import string

# CONFIGURATION
base_dir = "generated_files"
total_target_size = 150 * 1024 * 1024  # 150 MB
estimated_file_count = 9000
small_file_size_range = (1 * 1024, 30 * 1024)     # 1KB–30KB
large_file_size_range = (80 * 1024, 100 * 1024)   # 80KB–100KB
large_file_probability = 0.05                     # 5% of files will be large
files_per_folder = 500                            # To distribute files across folders

# HELPERS
def random_filename():
    return ''.join(random.choices(string.ascii_lowercase, k=10)) + ".txt"

def random_content(size):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=size))

# MAIN
os.makedirs(base_dir, exist_ok=True)

file_counter = 0
total_written = 0
folder_index = 1

while total_written < total_target_size and file_counter < estimated_file_count:
    # Create new folder if needed
    if file_counter % files_per_folder == 0:
        folder_path = os.path.join(base_dir, f"folder_{folder_index}")
        os.makedirs(folder_path, exist_ok=True)
        folder_index += 1

    # Decide size of this file
    is_large = random.random() < large_file_probability
    if is_large:
        size = random.randint(*large_file_size_range)
    else:
        size = random.randint(*small_file_size_range)

    # Create file
    filename = random_filename()
    file_path = os.path.join(folder_path, filename)
    with open(file_path, 'w') as f:
        f.write(random_content(size))

    file_counter += 1
    total_written += size

print(f"✅ Done! Generated {file_counter} files (~{total_written / (1024 * 1024):.2f} MB) in '{base_dir}'.")

