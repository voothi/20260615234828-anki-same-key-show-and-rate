# Anki Double-Duty Hotkey

An Anki Desktop add-on that enables keyboard shortcuts (default `1`, `2`, `3`, `4`, `h`) to perform double-duty operations during review:
1. **On the Front (Question) side of a card:** Pressing any of the configured shortcuts reveals the answer (equivalent to pressing Space or Enter).
2. **On the Back (Answer) side of a card:** Pressing a shortcut key maps to its corresponding ease rating:
   - `1` / `h`: Again (ease rating `1`)
   - `2`: Hard (ease rating `2`)
   - `3`: Good (ease rating `3`)
   - `4`: Easy (ease rating `4`)

This solves keyboard-routing limitations by hooking directly into the Qt/C++ shortcut registry system rather than injecting listeners inside the card's template HTML/JavaScript contexts.

## Compatibility

- Supported on Anki Desktop **24.x** and **25.x**.
- Compatible with Windows, macOS, and Linux.
- Note: Python add-ons do not run on AnkiDroid. For AnkiDroid, use the native keymapping options under *Settings > Reviewing > Keyboard/Gamepad shortcuts*.

## Installation

1. Copy this directory into your local Anki add-ons folder (typically `AppData\Roaming\Anki2\addons21\20260615234828-anki-double-duty-hotkey`).
2. Restart Anki.

## Configuration

You can customize the list of active double-duty keys via Anki's Add-on config manager (**Tools > Add-ons > Double-Duty Hotkey 1 > Config**).

Default configuration:
```json
{
    "hotkeys": [
        "1",
        "2",
        "3",
        "4",
        "h"
    ]
}
```

Digits in the configuration list automatically map to their respective numerical ease levels. Non-digit keys (like `"h"`) default to ease level `1` (Again) unless otherwise specified.
