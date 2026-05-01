import sys, json

# OMO Keyword Detector
# Suggests OMO commands based on user prompt

KEYWORDS = {
    "fix": "/refactor",
    "bug": "/doctor",
    "implement": "/ultrawork",
    "architecture": "/refactor",
    "broken": "/doctor"
}

def main():
    try:
        input_data = sys.stdin.read()
        if not input_data: return
        data = json.loads(input_data)
        
        # BeforeModel: Check last user message
        if "messages" in data and len(data["messages"]) > 0:
            last_msg = data["messages"][-1]
            if last_msg.get("role") == "user":
                content = last_msg.get("content", "").lower()
                for kw, cmd in KEYWORDS.items():
                    if kw in content and cmd not in content:
                        last_msg["content"] += f"\n\n[OMO SUGGESTION]: Consider using '{cmd}' for this task."
                        break

        print(json.dumps(data))
    except Exception:
        sys.exit(0)

if __name__ == "__main__":
    main()
