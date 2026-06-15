# Anki Double-Duty Hotkey

An Anki Desktop add-on that enables a single keyboard shortcut (default `1`) to perform double-duty operations during review:
1. **On the Front (Question) side of a card:** Pressing the shortcut reveals the answer (equivalent to pressing Space or Enter).
2. **On the Back (Answer) side of a card:** Pressing the shortcut rates the card as **Again** (ease rating `1`, equivalent to Anki's default `1` key behavior).

This solves keyboard-routing limitations by hooking directly into the Qt/C++ shortcut registry system rather than injecting listeners inside the card's template HTML/JavaScript contexts.

## Compatibility

- Supported on Anki Desktop **24.x** and **25.x**.
- Compatible with Windows, macOS, and Linux.
- Note: Python add-ons do not run on AnkiDroid. For AnkiDroid, use the native keymapping options under *Settings > Reviewing > Keyboard/Gamepad shortcuts*.

## Installation

1. Copy this directory into your local Anki add-ons folder (typically `AppData\Roaming\Anki2\addons21\20260615234828-anki-double-duty-hotkey`).
2. Restart Anki.

## Configuration

You can customize the key shortcut and the response rating ease level via Anki's Add-on config manager (**Tools > Add-ons > Double-Duty Hotkey 1 > Config**).

Default configuration:
```json
{
    "hotkey": "1",
    "ease_level": 1
}
```

- `hotkey`: The keyboard key to use (e.g. `"1"`, `"Space"`, etc.).
- `ease_level`: The card rating to apply on the back side:
  - `1`: Again
  - `2`: Hard
  - `3`: Good
  - `4`: Easy
