import sys, json

# OMO-inspired dynamic truncation
# Matches src/hooks/tool-output-truncator.ts logic

TRUNCATABLE_TOOLS = [
    "grep_search", "glob", "list_directory", "web_fetch", "run_shell_command", "read_file"
]

LIMITS = {
    "web_fetch": 40000,
    "default": 150000
}

def main():
    try:
        input_data = sys.stdin.read()
        if not input_data:
            return
        data = json.loads(input_data)
        
        if "tool" in data and "output" in data:
            tool = data["tool"]
            output = data["output"]
            
            if tool in TRUNCATABLE_TOOLS and isinstance(output, str):
                limit = LIMITS.get(tool, LIMITS["default"])
                if len(output) > limit:
                    msg = f"\n... [TRUNCATED {len(output)-limit} CHARS BY OMO HOOK] ...\n"
                    data["output"] = output[:limit//2] + msg + output[-limit//2:]
        
        print(json.dumps(data))
    except Exception:
        sys.exit(0)

if __name__ == "__main__":
    main()
