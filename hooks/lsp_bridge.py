import os, sys, re, subprocess, json

# OMO Deep LSP Bridge
# Provides Diagnostics, Definitions, and Symbols for parity

def get_diagnostics(file_path):
    if file_path.endswith('.py'):
        try:
            res = subprocess.run(['flake8', '--format=%(path)s:%(row)d:%(col)s: %(code)s %(text)s', file_path], capture_output=True, text=True, shell=(sys.platform == 'win32'))
            return res.stdout
        except: return "LSP Error: flake8 failed"
    return "LSP Error: Unsupported language for diagnostics"

def get_definition(symbol, target_dir="."):
    # Use find_symbols logic
    from find_symbols import search_file
    all_defs = []
    for root, dirs, files in os.walk(target_dir):
        dirs[:] = [d for d in dirs if d not in {'.git', 'node_modules', '.gemini', '.sisyphus'}]
        for f in files:
            defs = search_file(os.path.join(root, f))
            all_defs.extend([d for d in defs if d['name'] == symbol])
    return all_defs

def main():
    if len(sys.argv) < 2: return
    cmd = sys.argv[1]
    
    if cmd == "diagnostics":
        print(get_diagnostics(sys.argv[2]))
    elif cmd == "definition":
        defs = get_definition(sys.argv[2])
        print(json.dumps(defs))
    elif cmd == "symbols":
        from find_symbols import search_file
        print(json.dumps(search_file(sys.argv[2])))

if __name__ == "__main__":
    # Add parent dir to path for imports
    sys.path.append(os.path.dirname(__file__))
    main()
