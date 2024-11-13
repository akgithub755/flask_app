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



import pandas as pd
import re

# Sample dataframe
data = {'column_name': [
    "Some text here. set attribute value to: a1 from: a2. More text here.",
    "Default Value To: b1 from: b2. Other content.",
    "Set Attribute Value to: c1 from: c2. Yet more text.",
    "Irrelevant sentence without any target phrases."
]}
df = pd.DataFrame(data)

# Function to extract both 't1' and 't2' values
def extract_values(text):
    match = re.search(r'(set attribute value to|default value to):\s*(.*?)\s+from:\s*(.*?)(?:\.|\s|$)', text, re.IGNORECASE)
    if match:
        return match.group(2), match.group(3)  # t1, t2
    return None, None  # If no match, return None for both

# Apply function to each row in the dataframe
df[['t1', 't2']] = df['column_name'].apply(lambda x: pd.Series(extract_values(x)))

print(df)

