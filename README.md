# Anki Same-Key Show and Rate

[![Version](https://img.shields.io/badge/version-v1.0.0-blue)](https://github.com/voothi/20260615234828-anki-same-key-show-and-rate/releases) 
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) 

An Anki Desktop add-on that enables keyboard shortcuts (default `1`, `2`, `3`, `4`, `h`) to perform same-key show and rate operations during review, eliminating the need to hit the spacebar on every card.

## Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Compatibility](#compatibility)
- [Installation](#installation)
- [Configuration](#configuration)
- [Testing](#testing)
- [License](#license)

---

## Features

*   **Spacebar-Free Reviewing**: Pressing any configured answer shortcut when a card's question (Front) is active will instantly show the answer.
*   **Same-Key Rating**: Pressing the shortcut key again when the card's answer (Back) is active will rate the card using that key's assigned rating/action.
*   **Custom Shortcuts Compatibility**: Works with default numeric keys (`1` to `4`) as well as custom keybindings (like Vim mappings or other layouts).

[Return to Top](#table-of-contents)

## Project Structure

This project is organized following modular Python development best practices for Anki add-ons:

```text
20260615234828-anki-same-key-show-and-rate/
├── .gitattributes
├── .gitignore
├── README.md                              # Documentation
├── pytest.ini                             # Pytest configuration
├── manifest.json                          # Anki addon manifest (required at root)
├── config.json                            # Addon configuration defaults (required at root)
├── config.json.template                   # Addon configuration template (required at root)
├── meta.json                              # Local addon state metadata (required at root)
├── __init__.py                            # Entry point, imports src.main
├── src/                                   # All codebase logic
│   ├── __init__.py                        # Package initialization (empty file)
│   └── main.py                            # Core same-key show/rate hook logic
└── tests/                                 # Test suite
    └── test_main.py                       # Tests for the core logic in main.py
```

[Return to Top](#table-of-contents)

## Compatibility

*   Supported on Anki Desktop **24.x** and **25.x**.
*   Compatible with Windows, macOS, and Linux.
*   *Note:* Python add-ons do not run on AnkiDroid or AnkiMobile.

[Return to Top](#table-of-contents)

## Installation

1.  Close Anki completely.
2.  Copy this directory into your local Anki add-ons folder (typically `AppData\Roaming\Anki2\addons21\20260615234828-anki-same-key-show-and-rate`).
3.  Restart Anki.

[Return to Top](#table-of-contents)

## Configuration

You can customize the list of active same-key mappings via Anki's Add-on config manager (**Tools > Add-ons > Same-Key Show and Rate > Config**).

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

The keys of the `hotkeys` object are the triggers on the keyboard. The values represent the target shortcut/action key to run on the back side of the card (e.g., `"h"` maps to `"h"`'s default back action, while `"1"` maps to `"1"`'s default back action).

[Return to Top](#table-of-contents)

## Testing

The project includes a `pytest` suite for offline testing of shortcut registrations, state detection, and configurations.

### Running Tests

Execute `pytest` from the **project root**:

```bash
pytest
```

[Return to Top](#table-of-contents)

## License

This project is licensed under the **MIT License**.

See the [LICENSE](LICENSE) file details (or standard MIT terms).

[Return to Top](#table-of-contents)
