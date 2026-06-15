# Anki Double-Duty Hotkey

An Anki Desktop add-on that enables keyboard shortcuts (default `1`, `2`, `3`, `4`, `h`) to perform double-duty operations during review:
1. **On the Front (Question) side of a card:** Pressing any of the configured shortcuts reveals the answer (equivalent to pressing Space or Enter).
2. **On the Back (Answer) side of a card:** Pressing a shortcut key maps to its corresponding target shortcut handler (or ease level):
   - `1` maps to `"1"` (Again)
   - `2` maps to `"2"` (Hard)
   - `3` maps to `"3"` (Good)
   - `4` maps to `"4"` (Easy)
   - `h` maps to `"h"` (its own original handler on the back, or ease rating 1 if none exists)

This solves keyboard-routing limitations by hooking directly into the Qt/C++ shortcut registry system rather than injecting listeners inside the card's template HTML/JavaScript contexts.

## Compatibility

- Supported on Anki Desktop **24.x** and **25.x**.
- Compatible with Windows, macOS, and Linux.
- Note: Python add-ons do not run on AnkiDroid. For AnkiDroid, use the native keymapping options under *Settings > Reviewing > Keyboard/Gamepad shortcuts*.

## Installation

1. Copy this directory into your local Anki add-ons folder (typically `AppData\Roaming\Anki2\addons21\20260615234828-anki-double-duty-hotkey`).
2. Restart Anki.

## Configuration

You can customize the list of active double-duty keys and what they route to via Anki's Add-on config manager (**Tools > Add-ons > Double-Duty Hotkey 1 > Config**).

Default configuration:
```json
{
    "hotkeys": {
        "1": "1",
        "2": "2",
        "3": "3",
        "4": "4",
        "h": "h"
    }
}
```

The keys of the `hotkeys` object are the triggers on the keyboard. The values represent the target shortcut/action key to run on the back side of the card (e.g. `"h"` maps to `"h"`'s default back action, while `"1"` maps to `"1"`'s default back action).
