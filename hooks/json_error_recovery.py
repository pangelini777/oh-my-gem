import sys, json

# OMO JSON Error Recovery
# Catch JSON decode errors in tool calls and provide fix reminders

def main():
    try:
        input_data = sys.stdin.read()
        if not input_data: return
        data = json.loads(input_data)
        
        # AfterTool
        if "output" in data and isinstance(data["output"], str):
            if "json" in data["output"].lower() and "decode" in data["output"].lower():
                data["output"] += "\n\n[RECOVERY SUGGESTION]: You likely produced invalid JSON in a tool call (e.g. unescaped newlines or quotes). Ensure your JSON is valid and string values are properly escaped."

        print(json.dumps(data))
    except Exception:
        sys.exit(0)

if __name__ == "__main__":
    main()
