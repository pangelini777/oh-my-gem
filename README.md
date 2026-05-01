# Oh My Gem (OMG)
## OMO for Gemini CLI

**Oh My Gem** is a high-fidelity port of the **Oh My OpenCode (OMO)** agent orchestration system to the Gemini CLI. It transforms the standard Gemini session into a professional software engineering team with 12 specialized agents, surgical safety protocols, and robust lifecycle hooks.

---

## 🚀 Quick Start

1. **Install Extension**:
   ```bash
   gemini extensions install https://github.com/pangelini777/oh-my-gem
   ```
2. **Initialize Workspace**:
   ```bash
   /doctor
   ```
3. **Start Working**:
   ```bash
   /ultrawork "implement a new auth system"
   ```

The bundled hooks call `python3`, so Python 3 must be available on your `PATH`.

For local development from a cloned checkout, use:

```bash
gemini extensions link .
```

or install a local copy with:

```bash
gemini extensions install .
```

---

## 🤖 The Team (Agents)

| Agent | Role | Model |
| :--- | :--- | :--- |
| **SISYPHUS** | Main Orchestrator & Project Manager | `gemini-3.1-pro-preview` |
| **PROMETHEUS** | Strategic Planner (Interview Mode) | `gemini-3.1-pro-preview` |
| **HEPHAESTUS** | Autonomous Code Maker (TDD) | `Dynamic (via Model Router)` |
| **ORACLE** | Technical Lead & Architect | `gemini-3.1-pro-preview` |
| **METIS** | Plan Consultant & Gap Finder | `gemini-3.1-pro-preview` |
| **MOMUS** | Ruthless Judge & Reviewer | `gemini-3.1-pro-preview` |
| **EXPLORE** | Fast Scout & Code Search | `gemini-3-flash-preview` |
| **LIBRARIAN** | Doc & GitHub Code Researcher | `gemini-3-flash-preview` |
| **ATLAS** | Taskboard Manager & State Keeper | `gemini-3-flash-preview` |
| **LOOKER** | Vision & UI/UX Analyzer | `gemini-3-flash-preview` |
| **GENERALIST** | Batch Worker & Cleanup | `gemini-3-flash-preview` |
| **SISYPHUS-JR** | Agile Assistant & Quick Edits | `gemini-3-flash-preview` |

> 💡 **Research Strategy**: The Librarian uses a "Three-Pillar" strategy (Context7, GitHub/Grep.app, and Web Search) to provide evidence-based answers. To enable higher rate limits, set the `CONTEXT7_API_KEY` in your environment.

---

## 🛡️ Surgical Safety (Hashline-Edit)

Oh My Gem implements the **OMO Hashline Protocol**. Every file read injects content-addressed hashes (`LINE#HASH|`). 

**The Guard**: The `replace` tool is wrapped in a hook that verifies these hashes. If a file changes on disk after the agent reads it, the hook **blocks** the edit, preventing code corruption and stale-line errors.

## 🔐 Policy Notes

Gemini CLI ignores `allow` decisions contributed by extensions. Oh My Gem only ships extension-safe deny rules; if you want permanent allow rules, add them to your user policy files under `~/.gemini/policies/`.

---

## 🔗 Lifecycle Hooks

*   **Model Router**: Dynamically selects models based on intent (3.1 Pro for reasoning/fix/evaluation, 3 Flash for implementation/efficiency).
*   **Agent Status**: Uses `systemMessage` to inject professional UI banners indicating agent state.
*   **Intent Gate**: Classifies user requests (Research/Fix/Impl) and enforces verbalization.
*   **Todo Enforcer**: Monitors the Taskboard Ledger for stagnation and triggers reassessment if tasks remain un-updated.
*   **Ralph Loop**: Detects missing `<promise>DONE</promise>` and triggers autonomous continuation.
*   **Output Truncator**: Dynamically chops tool outputs (40k for web, 150k default) to save context.
*   **Error Recovery**: Injects actionable suggestions when JSON or Edit tools fail.
*   **Tmux Manager**: Ensures a persistent `oh-my-gem` terminal session is always available.
*   **Codebase Mapper**: Generates structural intelligence for the agents.

---

## 🛠️ Custom Commands

- `/ultrawork <task>`: Fully autonomous end-to-end execution.
- `/doctor`: Workspace health and configuration diagnostics.

---

## 📁 Structure

```
.
├── .gemini/
│   ├── agents/      # 12 Agent definitions (.md)
│   ├── hooks/       # Python logic scripts (.py)
│   ├── commands/    # Custom slash commands (.toml)
│   └── policies/    # Extension-safe deny rules
├── .oh-my-gem/      # Workspace ledger
│   └── taskboard.md
└── GEMINI.md        # Workspace instructions
```

💡 **Tip**: Keep `.oh-my-gem/taskboard.md` open in your IDE to watch the Sisyphus team update your project ledger in real-time.
