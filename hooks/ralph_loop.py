import sys, json, re

# OMO implementation uses <promise>DONE</promise>
# We'll support <promise>...any text...</promise> or <promise>DONE</promise>
PROMISE_PATTERN = re.compile(r"<promise>.*?</promise>", re.IGNORECASE | re.DOTALL)

def main():
    try:
        input_data = sys.stdin.read()
        if not input_data:
            return
        data = json.loads(input_data)
        
        # In Gemini CLI AfterAgent hook:
        # data["history"] contains the session turns.
        # we check the last ASSISTANT message for a promise.
        
        history = data.get("history", [])
        if not history:
            print(json.dumps(data))
            return

        last_assistant_turn = None
        for turn in reversed(history):
            if turn.get("role") == "assistant":
                last_assistant_turn = turn
                break
        
        if last_assistant_turn:
            content = last_assistant_turn.get("content", "")
            has_promise = bool(PROMISE_PATTERN.search(content))
            
            if not has_promise:
                # OMO logic: if not done, suggest continuation
                # Gemini CLI can't "auto-fire" another turn easily from a hook
                # but it can inject a system message that the agent will see next.
                # However, for a true loop, we want the agent to keep going.
                
                # Check if we already injected a continuation recently to prevent infinite no-op loops
                last_user_turn = None
                for turn in reversed(history):
                    if turn.get("role") == "user":
                        last_user_turn = turn
                        break
                
                is_continuation = last_user_turn and "[SYSTEM]: Ralph Loop" in last_user_turn.get("content", "")
                
                # Limit iterations (simple counter)
                iteration = 1
                if is_continuation:
                    match = re.search(r"Iteration (\d+)", last_user_turn["content"])
                    if match:
                        iteration = int(match.group(1)) + 1
                
                if iteration <= 10: # MAX_ITERATIONS
                    # We inject a "user" prompt that acts as the Ralph Loop trigger
                    # In Gemini CLI, the next model call will see this.
                    # Note: This is an "AfterAgent" hook, so the turn is over.
                    # To force a NEW turn, OMO uses the client API. 
                    # Here we rely on the agent's next prompt or internal loop.
                    
                    data["next_prompt_prefix"] = f"[SYSTEM]: Ralph Loop - Iteration {iteration}. Completion promise not detected. Continue until <promise>DONE</promise> is produced."
        
        print(json.dumps(data))
    except Exception:
        sys.exit(0)

if __name__ == "__main__":
    main()
