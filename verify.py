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
