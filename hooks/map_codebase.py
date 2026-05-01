import os, sys

# OMO Codebase Mapper
# Generates a high-level summary of the codebase structure and key files

IGNORE_DIRS = {'.git', 'node_modules', '.gemini', '.sisyphus', '__pycache__', 'dist', 'build'}

def map_dir(path, indent=0):
    try:
        items = sorted(os.listdir(path))
    except Exception: return
    
    for item in items:
        if item in IGNORE_DIRS: continue
        full_path = os.path.join(path, item)
        if os.path.isdir(full_path):
            print("  " * indent + f"📁 {item}/")
            map_dir(full_path, indent + 1)
        else:
            # For key files, add a small note
            note = ""
            if item.endswith(('.md', '.toml', '.json', '.yaml')): note = " [Config/Docs]"
            if item in ['GEMINI.md', 'todo.md']: note = " [CORE]"
            print("  " * indent + f"📄 {item}{note}")

if __name__ == "__main__":
    print(f"--- CODEBASE MAP ({os.getcwd()}) ---")
    map_dir('.')
