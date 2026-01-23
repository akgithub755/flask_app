#metadata

from dataclasses import dataclass
from pathlib import Path
from datetime import datetime
from .file_type import FileTypeDetector

@dataclass(frozen=True)
class FileMetadata:
    name: str
    path: Path
    extension: str
    size_bytes: int
    created_at: datetime
    modified_at: datetime
    file_type: str
    hash_value: str | None = None


class FileMetadataExtractor:
    def extract(self, path: Path) -> FileMetadata:
        stat = path.stat()

        return FileMetadata(
            name=path.name,
            path=path.resolve(),
            extension=path.suffix.lower(),
            size_bytes=stat.st_size,
            created_at=datetime.fromtimestamp(stat.st_ctime),
            modified_at=datetime.fromtimestamp(stat.st_mtime),
            file_type=FileTypeDetector.detect(path.suffix)
        )


#hasing

import hashlib
from pathlib import Path

class HashCalculator:
    def __init__(self, algorithm="sha256", chunk_size=1024 * 1024):
        self.algorithm = algorithm
        self.chunk_size = chunk_size

    def calculate(self, file_path: Path) -> str:
        hasher = hashlib.new(self.algorithm)

        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(self.chunk_size), b""):
                hasher.update(chunk)

        return hasher.hexdigest()


#duplicates
from collections import defaultdict

class DuplicateDetector:
    def __init__(self):
        self.hash_map = defaultdict(list)

    def process(self, metadata):
        self.hash_map[metadata.hash_value].append(metadata.path)

    def get_duplicates(self):
        return {
            h: paths for h, paths in self.hash_map.items()
            if len(paths) > 1
        }


#analyzer
from collections import Counter

class FileAnalyzer:
    def __init__(self):
        self.total_size = 0
        self.file_count = 0
        self.type_counter = Counter()
        self.largest_files = []

    def analyze(self, metadata):
        self.file_count += 1
        self.total_size += metadata.size_bytes
        self.type_counter[metadata.file_type] += 1
        self.largest_files.append(metadata)

    def finalize(self, top_n):
        self.largest_files.sort(
            key=lambda x: x.size_bytes,
            reverse=True
        )
        self.largest_files = self.largest_files[:top_n]


#report

class ReportGenerator:
    def generate(self, analyzer, duplicates):
        print("\n========== FILE SCAN REPORT ==========")
        print(f"Total files scanned : {analyzer.file_count}")
        print(f"Total disk usage   : {analyzer.total_size / (1024**2):.2f} MB")

        print("\nFile count by type:")
        for file_type, count in analyzer.type_counter.items():
            print(f"  {file_type}: {count}")

        print("\nLargest files:")
        for file in analyzer.largest_files:
            print(f"  {file.path} ({file.size_bytes / (1024**2):.2f} MB)")

        print("\nDuplicate files:")
        for hash_val, paths in duplicates.items():
            print(f"\nHash: {hash_val}")
            for path in paths:
                print(f"  {path}")


#engine

import logging
from .scanner import DirectoryScanner
from .metadata import FileMetadataExtractor
from .hashing import HashCalculator
from .duplicates import DuplicateDetector
from .analyzer import FileAnalyzer
from .report import ReportGenerator

class ProcessingEngine:
    def __init__(self, root_path, hash_algo, chunk_size, top_n):
        self.scanner = DirectoryScanner(root_path)
        self.extractor = FileMetadataExtractor()
        self.hasher = HashCalculator(hash_algo, chunk_size)
        self.duplicate_detector = DuplicateDetector()
        self.analyzer = FileAnalyzer()
        self.reporter = ReportGenerator()
        self.top_n = top_n

    def run(self):
        for file_path in self.scanner.scan():
            try:
                metadata = self.extractor.extract(file_path)
                metadata = metadata.__class__(
                    **metadata.__dict__,
                    hash_value=self.hasher.calculate(file_path)
                )

                self.duplicate_detector.process(metadata)
                self.analyzer.analyze(metadata)

            except Exception as e:
                logging.error(f"Error processing {file_path}: {e}")

        self.analyzer.finalize(self.top_n)
        self.reporter.generate(
            self.analyzer,
            self.duplicate_detector.get_duplicates()
        )


#main   
from config.settings import (
    ROOT_SCAN_PATH,
    HASH_ALGORITHM,
    HASH_CHUNK_SIZE,
    TOP_LARGEST_FILES,
    LOG_LEVEL
)
from utils.logger import setup_logger
from core.engine import ProcessingEngine

def main():
    setup_logger(LOG_LEVEL)

    engine = ProcessingEngine(
        root_path=ROOT_SCAN_PATH,
        hash_algo=HASH_ALGORITHM,
        chunk_size=HASH_CHUNK_SIZE,
        top_n=TOP_LARGEST_FILES
    )
    engine.run()

if __name__ == "__main__":
    main()
