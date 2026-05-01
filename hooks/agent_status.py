import sys, json

# OMO Agent Status Hook
# Displays a professional agent banner in the Gemini CLI UI

def main():
    try:
        input_data = sys.stdin.read()
        if not input_data:
            return
        data = json.loads(input_data)
        
        # BeforeAgent hook
        # Gemini CLI sends 'agent' and 'prompt'
        agent_name = data.get("agent", "sisyphus").upper()
        
        # Map agent names to emojis for flair
        emojis = {
            "SISYPHUS": "🔱",
            "PROMETHEUS": "🔥",
            "HEPHAESTUS": "⚒️",
            "ATLAS": "🌍",
            "ORACLE": "👁️",
            "METIS": "⚖️",
            "EXPLORE": "🔍",
            "LIBRARIAN": "📚",
            "MOMUS": "🎭",
            "MULTIMODAL-LOOKER": "👁️‍🗨️"
        }
        emoji = emojis.get(agent_name, "🤖")
        
        # Use systemMessage to show a professional banner in the UI
        data["systemMessage"] = f"{emoji} Agent: **{agent_name}** is now taking the lead."
        
        # We can also keep the stderr for background logging if desired, 
        # but systemMessage is the primary UI method.
        # sys.stderr.write(f"\n[OMO]: {agent_name} active\n")
        
        print(json.dumps(data))
    except Exception:
        # On error, pass through data unchanged to avoid breaking the session
        try:
            print(input_data)
        except:
            pass
        sys.exit(0)

if __name__ == "__main__":
    main()
