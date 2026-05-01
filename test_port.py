import subprocess
import json
import os
import shutil
import tempfile
import unittest
import sys

def run_hook(hook_name, input_dict, args=None):
    hook_path = f'hooks/{hook_name}.py'
    cmd = [sys.executable, hook_path]
    if args:
        cmd.extend(args)
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    stdout, stderr = proc.communicate(input=json.dumps(input_dict))
    return stdout, stderr, proc.returncode

class TestHooks(unittest.TestCase):
    def test_output_truncate(self):
        limit = 150000
        large_output = "A" * (limit + 100)
        inp = {"tool": "grep_search", "output": large_output}
        stdout, _, _ = run_hook('output_truncate', inp)
        out = json.loads(stdout)
        self.assertIn("[TRUNCATED", out['output'])
        self.assertLess(len(out['output']), limit + 100)

    def test_agent_status(self):
        inp = {"agent": "prometheus"}
        stdout, stderr, _ = run_hook('agent_status', inp)
        self.assertIn("[OMO AGENT]: 🚀 PROMETHEUS active", stderr)
        self.assertEqual(json.loads(stdout), inp)

    def test_dump(self):
        dump_file = "hooks/last_hook_input.json"
        if os.path.exists(dump_file): os.remove(dump_file)
        inp = {"test": "data"}
        stdout, _, _ = run_hook('dump', inp)
        self.assertEqual(json.loads(stdout), inp)
        with open(dump_file, 'r') as f:
            self.assertEqual(json.load(f), inp)

    def test_edit_error_recovery(self):
        inp = {"output": "Error: hash mismatch occurred"}
        stdout, _, _ = run_hook('edit_error_recovery', inp)
        out = json.loads(stdout)
        self.assertIn("[RECOVERY SUGGESTION]", out['output'])
        self.assertIn("read_file", out['output'])

    def test_find_symbols(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            py_file = os.path.join(tmpdir, "test.py")
            with open(py_file, "w") as f:
                f.write("class MyClass:\n    def my_func(): pass")
            
            # find_symbols is not a JSON hook, it's a CLI tool
            hook_path = 'hooks/find_symbols.py'
            proc = subprocess.run([sys.executable, hook_path, 'MyClass', tmpdir], capture_output=True, text=True)
            self.assertIn("test.py:1 | MyClass", proc.stdout)

    def test_hashline_wrapper_read(self):
        inp = {"tool": "read_file", "output": "1: line one\n2: line two"}
        stdout, _, _ = run_hook('hashline_wrapper', inp)
        out = json.loads(stdout)
        self.assertIn("1#", out['output'])
        self.assertIn("|line one", out['output'])

    def test_hashline_wrapper_guard_fail(self):
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as tmp:
            tmp.write("actual content")
            tmp_path = tmp.name
        try:
            # Hash for line 1 "wrong content"
            # compute_line_hash(1, "wrong content") -> ...
            import hashlib
            wrong_hash = hashlib.sha256(f"1:wrong content".encode('utf-8')).hexdigest()[:8]
            
            inp = {
                "tool": "replace",
                "args": {
                    "file_path": tmp_path,
                    "old_string": f"1#{wrong_hash}|wrong content"
                }
            }
            stdout, stderr, code = run_hook('hashline_wrapper', inp)
            self.assertEqual(code, 2)
            self.assertIn("Hashline mismatch", stderr)
        finally:
            os.remove(tmp_path)

    def test_intent_gate(self):
        inp = {"messages": [{"role": "user", "content": "fix the bug"}]}
        stdout, _, _ = run_hook('intent_gate', inp)
        out = json.loads(stdout)
        self.assertIn("I detect fix intent", out['messages'][0]['content'])

    def test_json_error_recovery(self):
        inp = {"output": "JSON decode error at line 1"}
        stdout, _, _ = run_hook('json_error_recovery', inp)
        out = json.loads(stdout)
        self.assertIn("[RECOVERY SUGGESTION]", out['output'])

    def test_keyword_detector(self):
        inp = {"messages": [{"role": "user", "content": "I need to fix a bug"}]}
        stdout, _, _ = run_hook('keyword_detector', inp)
        out = json.loads(stdout)
        self.assertIn("[OMO SUGGESTION]", out['messages'][0]['content'])
        self.assertIn("/refactor", out['messages'][0]['content'])

    def test_lsp_bridge_diagnostics(self):
        # Requires flake8 in environment
        with tempfile.NamedTemporaryFile(suffix=".py", mode='w', delete=False) as tmp:
            tmp.write("import os\nx = 1") # Unused import
            tmp_path = tmp.name
        try:
            hook_path = 'hooks/lsp_bridge.py'
            proc = subprocess.run([sys.executable, hook_path, 'diagnostics', tmp_path], capture_output=True, text=True)
            # Depending on flake8 config, might have output or not
            # Just check it ran
            self.assertEqual(proc.returncode, 0)
        finally:
            os.remove(tmp_path)

    def test_map_codebase(self):
        hook_path = 'hooks/map_codebase.py'
        proc = subprocess.run([sys.executable, hook_path], capture_output=True, text=True)
        self.assertIn("--- CODEBASE MAP", proc.stdout)
        self.assertIn("📄 GEMINI.md", proc.stdout)

    def test_ralph_loop(self):
        inp = {
            "history": [
                {"role": "assistant", "content": "I am working on it."}
            ]
        }
        stdout, _, _ = run_hook('ralph_loop', inp)
        out = json.loads(stdout)
        self.assertIn("Ralph Loop", out.get("next_prompt_prefix", ""))

    def test_tmux_manager(self):
        # We can't easily test tmux in CI without tmux installed
        # But we can check if it handles the 'has-session' failure gracefully
        stdout, _, _ = run_hook('tmux_manager', {"test": "data"})
        # Should just pass through stdin to stdout if tmux fails or works
        self.assertIn("test", stdout)

    def test_todo_enforcer(self):
        todo_path = "todo.md"
        state_path = os.path.join(tempfile.gettempdir(), "oh-my-gem-todo-stagnation")
        if os.path.exists(state_path): os.remove(state_path)
        
        with open(todo_path, "w") as f:
            f.write("- [ ] Task 1")
        
        try:
            inp = {"test": "data"}
            # Run 3 times to trigger stagnation
            run_hook('todo_enforcer', inp)
            run_hook('todo_enforcer', inp)
            run_hook('todo_enforcer', inp)
            stdout, _, _ = run_hook('todo_enforcer', inp)
            out = json.loads(stdout)
            self.assertIn("STAGNATION DETECTED", out.get("next_prompt_prefix", ""))
        finally:
            pass

if __name__ == "__main__":
    unittest.main()
