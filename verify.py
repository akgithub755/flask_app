import pandas as pd
import re

# Sample dataframe
data = {'column_name': [
    "This is a test sentence. set Attribute value to: 42. More text here.",
    "Some other text. DEFAULT VALUE TO: hello world. Even more text.",
    "Set Attribute value to: 100. Another sentence here.",
    "No relevant phrase here."
]}
df = pd.DataFrame(data)

# Function to extract 'some value'
def extract_value(text):
    match = re.search(r'(set attribute value to|default value to):\s*(.*?)(?:\.|\s|$)', text, re.IGNORECASE)
    return match.group(2) if match else None

# Apply function to each row in the dataframe
df['extracted_value'] = df['column_name'].apply(extract_value)

print(df)
