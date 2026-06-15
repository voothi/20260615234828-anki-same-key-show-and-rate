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
        hotkeys = config.get("hotkeys", ["1", "2", "3", "4", "h"])
        
        ease_map = {
            "1": 1,
            "2": 2,
            "3": 3,
            "4": 4,
            "h": 1
        }
        
        def create_callback(ease):
            def callback():
                # If looking at the front side of a card (Question)
                if mw.reviewer.state == "question":
                    if hasattr(mw.reviewer, "_showAnswer"):
                        mw.reviewer._showAnswer()
                    elif hasattr(mw.reviewer, "showAnswer"):
                        mw.reviewer.showAnswer()
                # If looking at the back side of a card (Answer)
                elif mw.reviewer.state == "answer":
                    if hasattr(mw.reviewer, "_answerCard"):
                        mw.reviewer._answerCard(ease)
                    elif hasattr(mw.reviewer, "answerCard"):
                        mw.reviewer.answerCard(ease)
            return callback

        for hotkey in hotkeys:
            # Remove any existing binding for the configured hotkey to avoid conflicts
            shortcuts[:] = [(k, h) for (k, h) in shortcuts if k != hotkey]
            
            # Determine target ease rating
            ease = ease_map.get(hotkey, 1)
            if hotkey.isdigit():
                ease = int(hotkey)
                
            # Append our custom double-duty handler
            shortcuts.append((hotkey, create_callback(ease)))

gui_hooks.state_shortcuts_will_change.append(register_reviewer_shortcuts)
