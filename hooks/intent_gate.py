import sys, json, re

# OMO Intent Categories
INTENTS = {
    "research": ["explain", "how", "what is", "research", "documentation", "find"],
    "fix": ["fix", "bug", "error", "broken", "issue", "failure", "crash"],
    "implementation": ["implement", "build", "create", "add", "feature", "new"],
    "investigation": ["look into", "check", "verify", "investigate", "examine", "debug"],
    "evaluation": ["think", "opinion", "better", "approach", "compare", "trade-off"],
    "open-ended": ["refactor", "improve", "clean up", "optimize", "polish"]
}

def classify(content):
    content = content.lower()
    for intent, keywords in INTENTS.items():
        if any(kw in content for kw in keywords):
            return intent
    return "open-ended"

def main():
    try:
        input_data = sys.stdin.read()
        if not input_data:
            return
        data = json.loads(input_data)
        
        # OMO Mandate: Verbalize Intent + Approach
        if "messages" in data and len(data["messages"]) > 0:
            last_msg = data["messages"][-1]
            if last_msg.get("role") == "user":
                content = last_msg.get("content", "")
                intent = classify(content)
                
                # We inject the mandate as a system reminder if not already classified by agent
                # (since this is BeforeModel, we can't see assistant output yet)
                reminder = f"\n\n[SYSTEM]: I detect {intent} intent. You MUST verbalize this intent and your approach (e.g., 'I detect {intent} intent. My approach is...') before any tool call."
                last_msg["content"] += reminder

        print(json.dumps(data))
    except Exception:
        sys.exit(0)

if __name__ == "__main__":
    main()
