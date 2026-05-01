import sys, json, os, tempfile

TODO_FILE = ".oh-my-gem/taskboard.md"
STATE_FILE = os.path.join(tempfile.gettempdir(), "oh-my-gem-todo-stagnation")

def main():
    try:
        input_data = sys.stdin.read()
        if not input_data:
            return
        data = json.loads(input_data)
        
        if os.path.exists(TODO_FILE):
            with open(TODO_FILE, "r") as f:
                content = f.read()
            
            # Count incomplete tasks (checkboxes or table rows with TODO/IN-PROGRESS or empty rows)
            incomplete = content.count("- [ ]")
            incomplete += content.count("| TODO |") + content.count("| IN_PROGRESS |") + content.count("| IN-PROGRESS |")
            incomplete += content.count("| | | | | |")
            
            # Check stagnation
            prev_content = ""
            stagnation_count = 0
            if os.path.exists(STATE_FILE):
                with open(STATE_FILE, "r") as f:
                    try:
                        state = json.load(f)
                        prev_content = state.get("content", "")
                        stagnation_count = state.get("count", 0)
                    except: pass
            
            if content == prev_content and incomplete > 0:
                stagnation_count += 1
            else:
                stagnation_count = 0
            
            # Update state
            with open(STATE_FILE, "w") as f:
                json.dump({"content": content, "count": stagnation_count}, f)
            
            if stagnation_count >= 3:
                # OMO behavior: inject warning about stagnation
                # In Gemini CLI, we can add a system reminder for the next turn
                data["next_prompt_prefix"] = f"[SYSTEM]: STAGNATION DETECTED. {TODO_FILE} has not changed for 3 turns. You MUST reassess your approach or ask the user for help."

        print(json.dumps(data))
    except Exception:
        sys.exit(0)

if __name__ == "__main__":
    main()
