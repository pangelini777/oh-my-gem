import sys
import json
import os

def process():
    data = sys.stdin.read()
    dump_file = os.path.join(os.path.dirname(__file__), "last_hook_input.json")
    with open(dump_file, "w") as f:
        f.write(data)
    print(data)

if __name__ == "__main__":
    process()
