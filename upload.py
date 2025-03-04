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
