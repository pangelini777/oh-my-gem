import sys, json, hashlib, re

# OMO Hashline Protocol
# Read: injects LINE#HASH| content
# Write/Replace: VERIFIES LINE#HASH| matches file before edit

def compute_line_hash(line_num, content):
    data = f"{line_num}:{content}".encode('utf-8')
    return hashlib.sha256(data).hexdigest()[:8]

def transform_line(line):
    parts = line.split(": ", 1)
    if len(parts) != 2: parts = line.split("| ", 1)
    if len(parts) == 2:
        try:
            ln = int(parts[0].strip())
            h = compute_line_hash(ln, parts[1])
            return f"{ln}#{h}|{parts[1]}"
        except: return line
    return line

def verify_hashlines(file_path, old_string):
    if not os.path.exists(file_path): return True
    with open(file_path, 'r') as f:
        lines = f.readlines()
    
    # Extract line references from old_string if they exist
    # Pattern: "123#abc12345| content"
    matches = re.findall(r"^(\d+)#([0-9a-f]{8})\|", old_string, re.M)
    for ln_str, expected_h in matches:
        ln = int(ln_str)
        if ln > len(lines): return False
        actual_content = lines[ln-1].rstrip('\n')
        actual_h = compute_line_hash(ln, actual_content)
        if actual_h != expected_h:
            return False
    return True

def main():
    try:
        input_data = sys.stdin.read()
        if not input_data: return
        data = json.loads(input_data)
        
        # AfterTool (Read)
        if "tool" in data and "output" in data:
            tool = data["tool"].lower()
            if tool == "read_file" and isinstance(data["output"], str):
                lines = data["output"].split('\n')
                if lines and (":" in lines[0] or "|" in lines[0]):
                    data["output"] = '\n'.join([transform_line(l) for l in lines])
            elif tool == "write_file":
                data["output"] = "File written successfully."
        
        # BeforeTool (Write/Replace Guard)
        if "tool" in data and "args" in data:
            tool = data["tool"].lower()
            if tool in ["replace", "write_file"]:
                fp = data["args"].get("file_path")
                old_s = data["args"].get("old_string", "")
                if fp and old_s and "#" in old_s:
                    if not verify_hashlines(fp, old_s):
                        sys.stderr.write(f"OMO ERROR: Hashline mismatch in {fp}. File changed since last read.\n")
                        sys.exit(2) # Block tool execution

        print(json.dumps(data))
    except Exception as e:
        sys.stderr.write(f"Hook Error: {e}\n")
        sys.exit(0)

if __name__ == "__main__":
    import os
    main()
