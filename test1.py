class DuplicateRowFinder:

    def __init__(self, input_file, output_file):
        if not input_file or not output_file:
            raise ValueError("Input and output file paths are mandatory")

        self.input_file = input_file
        self.output_file = output_file
        self.seen_rows = {}
        self.duplicates = []
        self.headers = []

    def read_and_find_duplicates(self):
        """
        Reads CSV file and identifies duplicate rows
        """
        with open(self.input_file, "r", encoding="utf-8") as file:
            # Read header
            header_line = file.readline().strip()
            self.headers = header_line.split(",")

            row_number = 1  # header row number

            for line in file:
                row_number += 1
                row_values = line.strip().split(",")

                row_key = tuple(row_values)

                if row_key in self.seen_rows:
                    original_row_number = self.seen_rows[row_key]
                    self.duplicates.append(
                        (original_row_number, row_values)
                    )
                else:
                    self.seen_rows[row_key] = row_number

    def write_duplicates_to_file(self):
        """
        Writes duplicate rows with original row number and headers
        """
        with open(self.output_file, "w", encoding="utf-8") as file:
            # Write new header
            new_headers = ["original_row_number"] + self.headers
            file.write(",".join(new_headers) + "\n")

            for original_row, row_data in self.duplicates:
                output_row = [str(original_row)] + row_data
                file.write(",".join(output_row) + "\n")

    def process(self):
        """
        Main execution method
        """
        self.read_and_find_duplicates()
        self.write_duplicates_to_file()
