import pandas as pd
import matplotlib.pyplot as plt

# Example DataFrame
data = {
    "a1": ["apple", "banana", "cherry", None, "grape"],
    "b1": ["juice", None, "pie", "smoothie", "wine"],
    "a2": ["car", "bike", "train", "plane", "boat"],
    "b2": ["fast", "slow", None, "high", "sail"],
    "a3": ["red", "yellow", "pink", None, "green"],
    "b3": ["fire", "sun", None, "sky", None],
}
df = pd.DataFrame(data)

# Function to generate the flowchart
def draw_flowchart(value):
    # Find the row containing the input value in columns a1, a2, a3
    row_idx = df[(df['a1'] == value) | (df['a2'] == value) | (df['a3'] == value)].index
    if row_idx.empty:
        print("Value not found in a1, a2, or a3.")
        return
    row = df.iloc[row_idx[0]]

    # Filter out None values and retain valid columns
    filtered_values = [(col, row[col]) for col in df.columns if pd.notna(row[col])]

    # Extract values and labels for plotting
    labels, values = zip(*filtered_values)

    # Plotting
    plt.figure(figsize=(12, 6))
    x_positions = range(len(values))  # Create positions for nodes
    y_positions = [0] * len(values)  # All nodes on the same horizontal line

    # Draw nodes
    for i, (x, y, label, val) in enumerate(zip(x_positions, y_positions, labels, values)):
        if "a" in label:  # Circle for 'a' columns
            circle = plt.Circle((x, y), 0.3, color="skyblue", ec="black", zorder=5)
            plt.gca().add_patch(circle)
        else:  # Square for 'b' columns
            square = plt.Rectangle((x - 0.3, y - 0.3), 0.6, 0.6, color="lightgreen", ec="black", zorder=5)
            plt.gca().add_patch(square)
        # Add text
        plt.text(x, y, f"{val}\n({label})", ha="center", va="center", fontsize=9, zorder=10)

    # Draw arrows (right to left)
    for i in range(1, len(values)):
        plt.arrow(x_positions[i], y_positions[i], x_positions[i - 1] - x_positions[i] + 0.4, 0,
                  head_width=0.1, head_length=0.2, fc='black', ec='black', zorder=3)

    # Adjust plot limits and title
    plt.xlim(-1, len(values))
    plt.ylim(-1, 1)
    plt.gca().set_aspect('equal')
    plt.axis('off')
    plt.title(f"Flowchart for Row: {[v for _, v in filtered_values]}")
    plt.show()

# Call the function with an example value
draw_flowchart("cherry")  # Replace "cherry" with any value from a1, a2, or a3




import pandas as pd
import re

# Sample dataframe
data = {'t1': ['select jkhfdkjshfks FROM husdkjhsjkf jhfkjfsf', 
               'select abc from def ghi when condition met',
               'SELECT jkl while checking',
               'SELECT * case when something happens',
               'if condition then action case test']}
df = pd.DataFrame(data)

# Function to break the sentence at keywords like 'from', 'when', 'while', 'case', 'if'
def break_at_keywords(text):
    # Define the keywords to split at, case-insensitive
    keywords = ['from', 'when', 'while', 'case', 'if']
    
    # Find the first keyword's position (case-insensitive)
    keyword_positions = [(keyword, text.lower().find(keyword)) for keyword in keywords]
    
    # Find the first occurrence of any keyword
    keyword_positions = [pos for pos in keyword_positions if pos[1] != -1]
    
    if keyword_positions:
        # Get the first keyword's position
        keyword, pos = min(keyword_positions, key=lambda x: x[1])
        
        # Split the text at that position
        parts = [text[:pos + len(keyword)], text[pos + len(keyword):]]
        
        # Return the first part and the keyword, followed by the second part on a new line
        return parts[0] + keyword + '\n' + parts[1]
    else:
        # If no keyword is found, return the text as is
        return text

# Apply the function to the 't1' column
df['t1'] = df['t1'].apply(break_at_keywords)

# Display the updated dataframe
print(df)




import pandas as pd

# Sample dataframe with multiple newline-separated values
data = {'t1': ['a1\n\n\na2', 'a1\n\n\na3', 'a1\n\n\na2\n\n\na3']}
df = pd.DataFrame(data)

# Function to combine the values in a single line with a comma
def combine_values(text):
    # Split the text by newline, remove empty parts, and join them with commas
    return ','.join(part.strip() for part in text.split('\n') if part.strip())

# Apply the function to the 't1' column
df['t1'] = df['t1'].apply(combine_values)

# Display the updated dataframe
print(df)




import pandas as pd

# Example DataFrame
data = {
    'a1': ['x', 'z', 'y', 'p', 'r'],
    'a2': ['y', 'w', 'x', 'q', 'p']
}
df = pd.DataFrame(data)

# Find common values between a1 and a2
common_values = set(df['a1']).intersection(set(df['a2']))

# Create a new DataFrame to store the results
result_rows = []

# Iterate over common values to find pairs
for value in common_values:
    row_a1 = df[df['a1'] == value].index.tolist()
    row_a2 = df[df['a2'] == value].index.tolist()
    
    # Check if value appears in different rows
    if row_a1 and row_a2 and row_a1[0] != row_a2[0]:
        result_rows.append([value, value])

# Create the result DataFrame
result_df = pd.DataFrame(result_rows, columns=['a1', 'a2'])

print("Original DataFrame:")
print(df)
print("\nNew DataFrame with common values in the same row:")
print(result_df)






import pandas as pd

# Example dataframe
data = {
    'source': ['cat1', 'cat2', 'cat1', 'cat3', 'cat2', 'cat3', 'cat1'],
    'a1': [10, 20, 30, 40, 50, 60, 70],
    'a2': [5, 15, 25, 35, 45, 55, 65],
    'a3': [100, 200, 300, 400, 500, 600, 700],
}

df = pd.DataFrame(data)

# Get the unique categories from the 'source' column
categories = df['source'].unique()

# Create a dictionary to store the DataFrames by category
category_dfs = {}

# Loop through each category and create a DataFrame
for category in categories:
    # Filter the DataFrame for the current category, drop 'source' column, and reset index
    category_dfs[category] = df[df['source'] == category].drop(columns=['source']).reset_index(drop=True)

# Store the dataframes in variables named after their categories
for category, dataframe in category_dfs.items():
    globals()[category] = dataframe

# Now you can access each DataFrame as a variable, e.g., cat1, cat2, cat3
print("cat1 DataFrame:")
print(cat1)
print("\ncat2 DataFrame:")
print(cat2)
print("\ncat3 DataFrame:")
print(cat3)









import pandas as pd

# Input DataFrame
data = {
    "s1": ["asa", "dasd", "test1", "test2"],
    "target_loc": ["dates", "dates_null", "whole_date", "dates"],
    "target_pde": ["business", "business_null", "whole_business", "business"],
    "s2": ["sdsd", "hghh", "exam", "mock"],
    "source_loc": ["whole_date", "dates", "dates_null", "whole_date"],
    "source_pde": ["whole_business", "business", "business_null", "whole_business"]
}

df = pd.DataFrame(data)

# Initialize a list to collect all unique rows
unique_rows = []

# Iterate through all rows in the DataFrame
for _, row in df.iterrows():
    # Find rows where target_loc and target_pde match source_loc and source_pde
    matches = df[
        (df["target_loc"] == row["source_loc"]) &
        (df["target_pde"] == row["source_pde"])
    ]
    
    # Process each match
    for _, match_row in matches.iterrows():
        # Iterate again for potential z_loc, z_pde matches
        for _, z_row in df.iterrows():
            if (
                match_row["source_loc"] == z_row["target_loc"] and
                match_row["source_pde"] == z_row["target_pde"]
            ):
                # Add the unique combination to the list
                unique_rows.append((
                    match_row["source_loc"], match_row["source_pde"],  # l_loc, l_pde
                    match_row["target_loc"], match_row["target_pde"],  # m_loc, m_pde
                    z_row["target_loc"], z_row["target_pde"]          # z_loc, z_pde
                ))

# Convert the list into a DataFrame and drop duplicates
final_df = pd.DataFrame(
    unique_rows,
    columns=["l_loc", "l_pde", "m_loc", "m_pde", "z_loc", "z_pde"]
).drop_duplicates().sort_values(by=["l_loc", "l_pde"]).reset_index(drop=True)

print("Final DataFrame:")
print(final_df)

