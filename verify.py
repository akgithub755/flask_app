# # import pandas as pd
# # import re

# # # Sample dataframe
# # data = {'column_name': [
# #     "This is a test sentence. set Attribute value to: 42. More text here.",
# #     "Some other text. DEFAULT VALUE TO: hello world. Even more text.",
# #     "Set Attribute value to: 100. Another sentence here.",
# #     "No relevant phrase here."
# # ]}
# # df = pd.DataFrame(data)

# # # Function to extract 'some value'
# # def extract_value(text):
# #     match = re.search(r'(set attribute value to|default value to):\s*(.*?)(?:\.|\s|$)', text, re.IGNORECASE)
# #     return match.group(2) if match else None

# # # Apply function to each row in the dataframe
# # df['extracted_value'] = df['column_name'].apply(extract_value)

# # print(df)



# # import pandas as pd
# # import re

# # # Sample dataframe
# # data = {'column_name': [
# #     "Some text here. set attribute value to: a1 from: a2. More text here.",
# #     "Default Value To: b1 from: b2. Other content.",
# #     "Set Attribute Value to: c1 from: c2. Yet more text.",
# #     "Irrelevant sentence without any target phrases."
# # ]}
# # df = pd.DataFrame(data)

# # # Function to extract both 't1' and 't2' values
# # def extract_values(text):
# #     match = re.search(r'(set attribute value to|default value to):\s*(.*?)\s+from:\s*(.*?)(?:\.|\s|$)', text, re.IGNORECASE)
# #     if match:
# #         return match.group(2), match.group(3)  # t1, t2
# #     return None, None  # If no match, return None for both

# # # Apply function to each row in the dataframe
# # df[['t1', 't2']] = df['column_name'].apply(lambda x: pd.Series(extract_values(x)))

# # print(df)



# # def get_ancestors(data, target, ancestors=None):
# #     """
# #     Recursively find all ancestors of the target node.
# #     """
# #     if ancestors is None:
# #         ancestors = []

# #     if data["value"] == target:
# #         return ancestors

# #     for child in data["children"]:
# #         result = get_ancestors(child, target, ancestors + [data["value"]])
# #         if result:
# #             return result

# #     return None


# # def get_descendants(node):
# #     """
# #     Recursively find all descendants of the given node.
# #     """
# #     descendants = []
# #     for child in node["children"]:
# #         descendants.append(child["value"])
# #         descendants.extend(get_descendants(child))
# #     return descendants


# # def find_node(data, target):
# #     """
# #     Find the node with the given target value.
# #     """
# #     if data["value"] == target:
# #         return data

# #     for child in data["children"]:
# #         result = find_node(child, target)
# #         if result:
# #             return result

# #     return None


# # def get_all_parents_and_children(tree_data, target):
# #     """
# #     Get all parents (ancestors) and children (descendants) of the target node.
# #     """
# #     # Get ancestors
# #     ancestors = get_ancestors(tree_data, target)

# #     # Find the target node to get its descendants
# #     target_node = find_node(tree_data, target)
# #     if not target_node:
# #         return None  # Target not found

# #     descendants = get_descendants(target_node)

# #     return {
# #         "value": target,
# #         "ancestors": ancestors,
# #         "descendants": descendants
# #     }


# # # Complex Example Data
# # tree_data = {
# #     "value": "root",
# #     "children": [
# #         {
# #             "value": "a1",
# #             "children": [
# #                 {"value": "b1", "children": []},
# #                 {
# #                     "value": "b2",
# #                     "children": [
# #                         {"value": "c1", "children": []},
# #                         {"value": "c2", "children": []},
# #                         {"value": "c3", "children": []}
# #                     ]
# #                 },
# #                 {"value": "b3", "children": []}
# #             ]
# #         },
# #         {
# #             "value": "a2",
# #             "children": [
# #                 {"value": "b4", "children": []},
# #                 {
# #                     "value": "b5",
# #                     "children": [
# #                         {"value": "c4", "children": []},
# #                         {"value": "c5", "children": []}
# #                     ]
# #                 }
# #             ]
# #         }
# #     ]
# # }

# # # Test the function for "b2"
# # result = get_all_parents_and_children(tree_data, "b2")
# # print(result)


# import tkinter as tk
# from tkinter import messagebox

# # Function to handle button click
# def display_message():
#     name = name_entry.get()
#     age = age_entry.get()
    
#     if not name or not age:
#         messagebox.showerror("Input Error", "Please fill in all fields.")
#         return

#     try:
#         age = int(age)
#         greeting = f"Hello, {name}! You are {age} years old."
#         output_label.config(text=greeting)
#     except ValueError:
#         messagebox.showerror("Input Error", "Please enter a valid number for age.")

# # Create the main window
# root = tk.Tk()
# root.title("Simple Tkinter App")
# root.geometry("400x300")

# # Add a label and entry for name
# tk.Label(root, text="Enter your name:").pack(pady=5)
# name_entry = tk.Entry(root, width=30)
# name_entry.pack(pady=5)

# # Add a label and entry for age
# tk.Label(root, text="Enter your age:").pack(pady=5)
# age_entry = tk.Entry(root, width=30)
# age_entry.pack(pady=5)

# # Add a button to display the message
# submit_button = tk.Button(root, text="Submit", command=display_message)
# submit_button.pack(pady=10)

# # Label to display the output message
# output_label = tk.Label(root, text="", font=("Helvetica", 12))
# output_label.pack(pady=20)

# # Run the application
# root.mainloop()
import tkinter as tk
from tkinter import ttk
import pandas as pd

# Dummy dataset with additional columns
data = {
    'a1': ['test1', 'test4', 'test7'],
    'a2': ['test2', 'test5', None],
    'a3': ['test3', None, 'test9'],
    'extra1': [10, 20, 30],
    'extra2': [40, 50, 60]
}

# Convert data to DataFrame
df = pd.DataFrame(data)

def search_data():
    search_value = search_entry.get().strip()
    if not search_value:
        result_label.config(text="Please enter a value to search.")
        return
    
    # Filter rows where any of the a1, a2, a3 columns contain the search value
    filtered_df = df[df[['a1', 'a2', 'a3']].apply(lambda x: search_value in x.values, axis=1)]
    
    if filtered_df.empty:
        result_label.config(text="No matching results found.")
        tree.delete(*tree.get_children())  # Clear any existing data
        tree["columns"] = ()  # Clear column headers
        return
    
    # Keep only columns a1, a2, a3 and exclude empty columns in the result
    filtered_df = filtered_df[['a1', 'a2', 'a3']].dropna(axis=1, how='all')
    
    # Update result label
    result_label.config(text=f"Results for '{search_value}':")
    
    # Clear existing table data
    tree.delete(*tree.get_children())
    
    # Define the dynamic columns in the Treeview
    tree["columns"] = list(filtered_df.columns)
    
    # Set table headings dynamically with bold column names
    style = ttk.Style()
    style.configure("Treeview.Heading", font=("Arial", 10, "bold"))
    
    for col in filtered_df.columns:
        tree.heading(col, text=col)
        tree.column(col, anchor=tk.CENTER, width=100)
    
    # Insert filtered rows into the table
    for _, row in filtered_df.iterrows():
        tree.insert("", tk.END, values=row.tolist())

def clear_data():
    # Clear the tree, column headers, and result label
    tree.delete(*tree.get_children())
    tree["columns"] = ()  # Clear column headers
    result_label.config(text="")
    search_entry.delete(0, tk.END)

# Initialize the Tkinter window
root = tk.Tk()
root.title("Search App")
root.geometry("650x500")

# Title
title_label = tk.Label(root, text="Linkage", font=("Helvetica", 16, "bold"))
title_label.pack(pady=10)

# Input field
input_frame = tk.Frame(root)
input_frame.pack(pady=5)

input_label = tk.Label(input_frame, text="Enter search value:")
input_label.pack(side=tk.LEFT, padx=5)

search_entry = tk.Entry(input_frame, width=30)
search_entry.pack(side=tk.LEFT, padx=5)

# Buttons
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

search_button = tk.Button(button_frame, text="Search", command=search_data)
search_button.pack(side=tk.LEFT, padx=5)

clear_button = tk.Button(button_frame, text="Clear", command=clear_data)
clear_button.pack(side=tk.LEFT, padx=5)

# Result label
result_label = tk.Label(root, text="")
result_label.pack(pady=10)

# Treeview for displaying results
tree_frame = tk.Frame(root, padx=10, pady=10)
tree_frame.pack(fill=tk.BOTH, expand=True)

tree = ttk.Treeview(tree_frame, show="headings")
tree.pack(pady=10, fill=tk.BOTH, expand=True)

# Add padding below output
root.pack_propagate(False)
tree_frame.pack_propagate(False)
tree_frame.config(padx=20, pady=20)

# Run the Tkinter event loop
root.mainloop()

