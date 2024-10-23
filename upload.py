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

