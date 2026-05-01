import os, sys, re

# OMO Poor Man's LSP - Symbol Finder
# Uses regex to locate definitions of classes, functions, and interfaces

PATTERNS = {
    'python': [r'^\s*(?:class|def)\s+([a-zA-Z_][a-zA-Z0-9_]*)'],
    'typescript': [
        r'^\s*(?:export\s+)?(?:class|function|interface|type|enum)\s+([a-zA-Z_][a-zA-Z0-9_]*)',
        r'^\s*(?:export\s+)?const\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*(?:async\s*)?\(',
    ],
    'javascript': [
        r'^\s*(?:class|function)\s+([a-zA-Z_][a-zA-Z0-9_]*)',
        r'^\s*const\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*\(',
    ],
    'markdown': [r'^#+\s+(.*)']
}

def search_file(file_path):
    ext = file_path.split('.')[-1]
    lang = None
    if ext == 'py': lang = 'python'
    elif ext in ['ts', 'tsx']: lang = 'typescript'
    elif ext in ['js', 'jsx']: lang = 'javascript'
    elif ext == 'md': lang = 'markdown'
    
    if not lang: return []
    
    symbols = []
    try:
        with open(file_path, 'r') as f:
            for i, line in enumerate(f):
                for pattern in PATTERNS[lang]:
                    match = re.search(pattern, line)
                    if match:
                        symbols.append({
                            'name': match.group(1),
                            'line': i + 1,
                            'type': 'definition',
                            'path': file_path
                        })
    except Exception: pass
    return symbols

def main():
    query = sys.argv[1] if len(sys.argv) > 1 else ""
    target_dir = sys.argv[2] if len(sys.argv) > 2 else "."
    
    all_symbols = []
    for root, dirs, files in os.walk(target_dir):
        # Prune ignored dirs
        dirs[:] = [d for d in dirs if d not in {'.git', 'node_modules', '.gemini', '.sisyphus', '__pycache__'}]
        for file in files:
            all_symbols.extend(search_file(os.path.join(root, file)))
    
    # Filter by query
    if query:
        results = [s for s in all_symbols if query.lower() in s['name'].lower()]
    else:
        results = all_symbols

    for s in results:
        print(f"{s['path']}:{s['line']} | {s['name']}")

if __name__ == "__main__":
    main()
