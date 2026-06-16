# Same-Key Show and Rate Release Notes

## Table of Contents

- [v1.0.0](#release-notes-v100)

---

## Release Notes v1.0.0

### 🚀 Features

*   **⌨️ Spacebar-Free Card Reviewing**
    *   Pressing any configured shortcut key when a card's question (Front) is active will instantly reveal the answer, eliminating the extra keypress/spacebar action.
*   **🔗 Same-Key Card Rating**
    *   Pressing the same configured key when the card's answer (Back) is active routes the keypress to the mapped ease rating or action.
*   **🔄 Decoupled Mappings Configuration**
    *   Mappings are configured using a key-value dictionary (e.g., `{"h": "1", "j": "3"}`). This decouples physical trigger keys on the front side from logical actions/fallbacks on the back side, enabling custom key routing and robust fallbacks.
*   **⚙️ Native Configuration Interface**
    *   Configure your preferred same-key mappings directly via Anki's native Add-on configuration window (**Tools > Add-ons > Same-Key Show and Rate > Config**).
*   **🧪 Offline Verification Suite**
    *   Includes a `pytest` test suite to offline-verify shortcut registration, hook behaviors, state transitions, and configuration loading.
*   **📦 Developer Build Infrastructure**
    *   Includes a platform-independent release pipeline script (`make_release.py` and `release_pipeline.py`) that executes verification tests and packages production files into clean, timestamped `.ankiaddon` files, strictly filtering out sensitive and developmental directories.
*   **🛡️ Release Verification**
    *   [Virus scan results and check amount for verification with the archive](https://www.virustotal.com/gui/file/206a2b34ce85691ecda895b198d8970d0f273d42f3c0f0c72fdfb078a04d939b)
[Return to Top](#same-key-show-and-rate-release-notes)
