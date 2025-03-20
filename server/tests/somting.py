#!/usr/bin/python
import time
import sys

def loading_line():
    length = 30  # Length of the line
    for i in range(length + 1):
        line = "[" + "=" * i + " " * (length - i) + "]"
        sys.stdout.write("\r" + line)
        sys.stdout.flush()
        time.sleep(0.1)
    print()  # Move to the next line when done

loading_line()

