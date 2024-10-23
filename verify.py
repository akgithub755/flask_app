import os
import time

def verify_file(file_path):
    if not os.path.exists(file_path):
        yield "File not found\n"
        return

    yield "Starting verification...\n"
    time.sleep(1)

    # Simulate file type check
    if file_path.endswith(('.xlsx', '.xls')):
        yield "File type check passed.\n"
        time.sleep(1)
        yield "Verification Successful\n"
    else:
        yield "Invalid file type. Verification failed.\n"


import sqlparse
from sqlparse.sql import IdentifierList, Identifier
from sqlparse.tokens import Keyword, DML

def extract_tables_from_sql(query):
    tables = set()  # Using a set to avoid duplicates
    parsed = sqlparse.parse(query)
    for stmt in parsed:
        if stmt.get_type() != 'SELECT':
            continue
        from_seen = False
        for token in stmt.tokens:
            # If token is a DML (like SELECT, INSERT, etc.)
            if token.ttype is DML and token.value.upper() == 'SELECT':
                from_seen = True
            # If token is a Keyword 'FROM', 'JOIN', etc., we start looking for table names
            if from_seen and token.ttype is Keyword:
                from_seen = False
            if from_seen:
                if isinstance(token, IdentifierList):
                    for identifier in token.get_identifiers():
                        tables.add(identifier.get_real_name())
                elif isinstance(token, Identifier):
                    tables.add(token.get_real_name())
            if token.ttype is Keyword and token.value.upper() in ['FROM', 'JOIN']:
                from_seen = True
    return list(tables)

# Example usage
query = """
SELECT t1.column1, t2.column2
FROM table1 AS t1
JOIN table2 AS t2 ON t1.id = t2.id
WHERE t1.column3 = 'some_value'
"""
table_names = extract_tables_from_sql(query)
print(table_names)
