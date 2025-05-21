#!/usr/bin/env python3

import os
import sys

def count_file_lines(file_path: str) -> None:
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return
    with open(file_path, 'r') as f:
        line_count = sum(1 for line in f)
    print(f"Number of lines in '{file_path}': {line_count}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script.py <file_path>")
    else:
        count_file_lines(sys.argv[1])

