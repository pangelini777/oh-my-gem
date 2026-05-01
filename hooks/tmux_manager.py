import sys, json, subprocess

# OMO Tmux Session Manager
# Ensures a persistent 'oh-my-gem' tmux session exists for interactive work

SESSION_NAME = "oh-my-gem"

def main():
    if sys.platform == "win32":
        print(sys.stdin.read())
        return
        
    try:
        # Check if session exists
        res = subprocess.run(["tmux", "has-session", "-t", SESSION_NAME], capture_output=True)
        if res.returncode != 0:
            # Create it
            subprocess.run(["tmux", "new-session", "-d", "-s", SESSION_NAME])
            sys.stderr.write(f"OMO: Created persistent tmux session '{SESSION_NAME}'\n")
            
        print(sys.stdin.read())
    except Exception:
        sys.exit(0)

if __name__ == "__main__":
    main()
