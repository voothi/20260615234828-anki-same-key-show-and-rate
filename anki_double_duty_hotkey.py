from aqt import mw
from aqt import gui_hooks

def get_config():
    # Get config for the current add-on package
    addon_package = __name__.split('.')[0]
    config = mw.addonManager.getConfig(addon_package)
    return config if config else {}

def register_reviewer_shortcuts(state: str, shortcuts: list):
    # Only register shortcuts when reviewing cards
    if state == "review":
        config = get_config()
        hotkey = config.get("hotkey", "1")
        ease_level = config.get("ease_level", 1)
        
        # Remove any existing binding for the configured hotkey to avoid conflicts
        for i, (key, handler) in enumerate(shortcuts):
            if key == hotkey:
                shortcuts.pop(i)
                break
                
        def on_hotkey_pressed():
            # If looking at the front side of a card (Question)
            if mw.reviewer.state == "question":
                if hasattr(mw.reviewer, "_showAnswer"):
                    mw.reviewer._showAnswer()
                elif hasattr(mw.reviewer, "showAnswer"):
                    mw.reviewer.showAnswer()
            # If looking at the back side of a card (Answer)
            elif mw.reviewer.state == "answer":
                if hasattr(mw.reviewer, "_answerCard"):
                    mw.reviewer._answerCard(ease_level)
                elif hasattr(mw.reviewer, "answerCard"):
                    mw.reviewer.answerCard(ease_level)
                    
        # Append our custom double-duty handler
        shortcuts.append((hotkey, on_hotkey_pressed))

gui_hooks.state_shortcuts_will_change.append(register_reviewer_shortcuts)
