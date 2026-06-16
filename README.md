# Anki Same-Key Show and Rate

[![Version](https://img.shields.io/badge/version-v1.0.0-blue)](https://github.com/voothi/20260615234828-anki-same-key-show-and-rate/releases) 
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) 
[![AnkiWeb](https://img.shields.io/badge/AnkiWeb-290816457-blue)](https://ankiweb.net/shared/info/290816457)

An Anki Desktop add-on that enables keyboard shortcuts (default `1`, `2`, `3`, `4`, `h`) to perform same-key show and rate operations during review, eliminating the need to hit the spacebar on every card.

## Table of Contents

- [Features](#features)
- [How It Works](#how-it-works)
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

## How It Works

The add-on automates the review loop using the following state transitions:

1. **Card Question (Front Side / Unrevealed):**
   * When a new card is presented, Anki is in the `"question"` state.
   * Pressing any of your configured trigger keys (e.g., `3` or `j`) intercepts the keypress and triggers the **Show Answer** (flip) action (`showAnswer()`), revealing the back side of the card.
2. **Card Answer (Back Side / Revealed):**
   * Once the answer is shown, Anki enters the `"answer"` state.
   * Pressing the same key (e.g., `3` or `j`) routes to the mapped target action:
     * If the target has an existing shortcut registered in Anki, it triggers that shortcut's action (e.g., running the custom handler for rating 3/Good).
     * If there is no handler, it falls back to directly answering/rating the card (`answerCard(ease)`) using the configured rating index.
   * Rating the card automatically loads the next card's question, restarting the loop at Step 1.

[Return to Top](#table-of-contents)

## Project Structure

This project is organized following modular Python development best practices for Anki add-ons:

```text
20260615234828-anki-same-key-show-and-rate/
├── .gitattributes
├── .gitignore
├── LICENSE                                # Project license
├── README.md                              # Documentation
├── release-notes.md                       # Version release notes
├── pytest.ini                             # Pytest configuration
├── manifest.json                          # Anki addon manifest (required at root)
├── config.json                            # Addon configuration defaults (required at root)
├── config.json.template                   # Addon configuration template (required at root)
├── meta.json                              # Local addon state metadata (required at root)
├── __init__.py                            # Entry point, imports src.main
├── scripts/                               # Developer build and deployment tools
│   ├── make_release.py                    # Release compilation entry point
│   ├── make_deploy.py                     # Local addon deployment utility
│   └── packaging/                         # Subdirectory containing internal build pipelines
│       ├── packaging.ini                  # Release configurations and exclusions
│       ├── release_pipeline.py            # Orchestrator
│       ├── create_addon_zip.py            # Zips addon and writes checksums
│       ├── setup_local_vendor.py          # Prepares local wheels
│       └── build_all_vendors.py           # Prepares platform wheels
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

### Why Key-Value Mappings instead of a Simple List?

If the configuration used a simple list of keys (e.g., `["1", "2", "3", "4", "h"]`), it would assume that the key pressed on the front must trigger itself on the back. While this works for standard keys, it breaks down for more advanced layouts:

1. **Custom Key Routing:** If a user reviews using a custom layout (e.g., mapping `h` to Again, `j` to Good, and `e` to Easy in Anki's settings), they can configure `{"h": "1", "j": "3", "e": "4"}`. Tap `h` to flip the card, and tap it again to route directly to rating `1` (Again).
2. **Decoupling Triggers from Actions:** A dictionary decoupling allows any physical key on the keyboard to map to any logical rating or handler on the back side of the card, regardless of whether that key natively performs a rating in Anki.
3. **Robust Fallbacks:** If a target key does not have an original handler registered, the mapping tells the add-on which ease rating to fallback to (e.g., routing `h` to rate `1`).

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
