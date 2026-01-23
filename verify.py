import os
import random
import string

def create_random_files(
    base_dir: str,
    n: int,
    min_size_kb: int = 5,
    max_size_mb: int = 5
):
    os.makedirs(base_dir, exist_ok=True)

    extensions = [
        ".txt", ".log", ".csv", ".json", ".xml",
        ".jpg", ".png", ".pdf", ".zip", ".bin"
    ]

    for i in range(1, n + 1):
        ext = random.choice(extensions)

        # Random file size
        size_bytes = random.randint(
            min_size_kb * 1024,
            max_size_mb * 1024 * 1024
        )

        filename = f"file_{i}{ext}"
        file_path = os.path.join(base_dir, filename)

        with open(file_path, "wb") as f:
            f.write(os.urandom(size_bytes))

        print(f"Created {filename} | Size: {size_bytes // 1024} KB")


if __name__ == "__main__":
    N = 50        # 🔁 Change this to any number
    create_random_files("test_data", N)
