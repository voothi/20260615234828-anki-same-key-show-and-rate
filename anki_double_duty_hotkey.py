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
        if not getattr(mw, "reviewer", None):
            return
        config = get_config()
        hotkey_mappings = config.get("hotkeys", {
            "1": "1",
            "2": "2",
            "3": "3",
            "4": "4",
            "h": "h"
        })
        
        # Extract the original handlers for the target keys before we modify shortcuts
        original_handlers = {}
        for key, handler in shortcuts:
            original_handlers[key] = handler

        def create_callback(trigger, target):
            def callback():
                if not getattr(mw, "reviewer", None):
                    return
                # If looking at the front side of a card (Question)
                if mw.reviewer.state == "question":
                    if hasattr(mw.reviewer, "_showAnswer"):
                        mw.reviewer._showAnswer()
                    elif hasattr(mw.reviewer, "showAnswer"):
                        mw.reviewer.showAnswer()
                # If looking at the back side of a card (Answer)
                elif mw.reviewer.state == "answer":
                    # Run target key's original handler if it exists
                    if target in original_handlers:
                        original_handlers[target]()
                    # Fallback: if target is a digit, map directly to corresponding ease rating
                    elif target.isdigit():
                        ease = int(target)
                        if hasattr(mw.reviewer, "_answerCard"):
                            mw.reviewer._answerCard(ease)
                        elif hasattr(mw.reviewer, "answerCard"):
                            mw.reviewer.answerCard(ease)
            return callback

        for trigger, target in hotkey_mappings.items():
            # Remove any existing binding for the configured trigger key to avoid conflicts
            shortcuts[:] = [(k, h) for (k, h) in shortcuts if k != trigger]
            
            # Append our custom double-duty handler
            shortcuts.append((trigger, create_callback(trigger, target)))

gui_hooks.state_shortcuts_will_change.append(register_reviewer_shortcuts)
