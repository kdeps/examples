#!/usr/bin/env python3

import sys

def add_two_numbers(a: float, b: float) -> None:
    result = a + b
    print(f"The sum of {a} and {b} is {result}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python script.py <num1> <num2>")
    else:
        try:
            num1 = float(sys.argv[1])
            num2 = float(sys.argv[2])
            add_two_numbers(num1, num2)
        except ValueError:
            print("Please provide two valid numbers.")

