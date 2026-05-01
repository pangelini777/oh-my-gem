import sys, json

# OMO Edit Error Recovery
# Detects tool failures and injects recovery suggestions

ERRORS = {
    "file not found": "The file does not exist. Use 'ls' or 'glob' to find the correct path.",
    "is not a directory": "Path is a file, not a directory.",
    "ambiguous": "The search string is ambiguous. Provide more context (more lines) in 'old_string'.",
    "hash mismatch": "The file changed since you last read it. You MUST 'read_file' again before editing."
}

def main():
    try:
        input_data = sys.stdin.read()
        if not input_data: return
        data = json.loads(input_data)
        
        # AfterTool
        if "output" in data and isinstance(data["output"], str):
            out = data["output"].lower()
            if "error" in out or "failed" in out or "not found" in out:
                for err_key, suggestion in ERRORS.items():
                    if err_key in out:
                        data["output"] += f"\n\n[RECOVERY SUGGESTION]: {suggestion}"
                        break
        
        print(json.dumps(data))
    except Exception:
        sys.exit(0)

if __name__ == "__main__":
    main()
