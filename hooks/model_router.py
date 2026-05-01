import sys, json

# Model Definitions (Upgraded to confirmed 3.1 Pro and 3 Flash)
MODELS = {
    "reasoning": "gemini-3.1-pro-preview",
    "balanced": "gemini-3.1-pro-preview", 
    "efficiency": "gemini-3-flash-preview",
    "lightweight": "gemini-2.5-flash-lite" # Assuming flash-lite stays at 2.5
}

# Mapping Intents to Model Profiles
INTENT_MODEL_MAP = {
    "research": MODELS["reasoning"],
    "fix": MODELS["balanced"],
    "implementation": MODELS["efficiency"],
    "investigation": MODELS["reasoning"],
    "evaluation": MODELS["reasoning"],
    "open-ended": MODELS["balanced"]
}

def main():
    try:
        input_data = sys.stdin.read()
        if not input_data:
            return
        data = json.loads(input_data)
        
        if "messages" in data and len(data["messages"]) > 0:
            last_msg = data["messages"][-1]
            if last_msg.get("role") == "user":
                content = last_msg.get("content", "")
                
                import os
                sys.path.append(os.path.dirname(__file__))
                try:
                    from intent_gate import classify as get_intent
                except ImportError:
                    print(input_data)
                    return

                intent = get_intent(content)
                target_model = INTENT_MODEL_MAP.get(intent, MODELS["balanced"])
                
                # Update the model for this request
                data["model"] = target_model

        print(json.dumps(data))
    except Exception:
        try:
            print(input_data)
        except:
            pass
        sys.exit(0)

if __name__ == "__main__":
    main()
