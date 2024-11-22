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



def get_ancestors(data, target, ancestors=None):
    """
    Recursively find all ancestors of the target node.
    """
    if ancestors is None:
        ancestors = []

    if data["value"] == target:
        return ancestors

    for child in data["children"]:
        result = get_ancestors(child, target, ancestors + [data["value"]])
        if result:
            return result

    return None


def get_descendants(node):
    """
    Recursively find all descendants of the given node.
    """
    descendants = []
    for child in node["children"]:
        descendants.append(child["value"])
        descendants.extend(get_descendants(child))
    return descendants


def find_node(data, target):
    """
    Find the node with the given target value.
    """
    if data["value"] == target:
        return data

    for child in data["children"]:
        result = find_node(child, target)
        if result:
            return result

    return None


def get_all_parents_and_children(tree_data, target):
    """
    Get all parents (ancestors) and children (descendants) of the target node.
    """
    # Get ancestors
    ancestors = get_ancestors(tree_data, target)

    # Find the target node to get its descendants
    target_node = find_node(tree_data, target)
    if not target_node:
        return None  # Target not found

    descendants = get_descendants(target_node)

    return {
        "value": target,
        "ancestors": ancestors,
        "descendants": descendants
    }


# Complex Example Data
tree_data = {
    "value": "root",
    "children": [
        {
            "value": "a1",
            "children": [
                {"value": "b1", "children": []},
                {
                    "value": "b2",
                    "children": [
                        {"value": "c1", "children": []},
                        {"value": "c2", "children": []},
                        {"value": "c3", "children": []}
                    ]
                },
                {"value": "b3", "children": []}
            ]
        },
        {
            "value": "a2",
            "children": [
                {"value": "b4", "children": []},
                {
                    "value": "b5",
                    "children": [
                        {"value": "c4", "children": []},
                        {"value": "c5", "children": []}
                    ]
                }
            ]
        }
    ]
}

# Test the function for "b2"
result = get_all_parents_and_children(tree_data, "b2")
print(result)
