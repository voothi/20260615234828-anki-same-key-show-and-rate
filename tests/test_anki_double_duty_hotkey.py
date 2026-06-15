import os
import sys
from unittest.mock import MagicMock

# Ensure parent directory is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Mock Anki imports before importing the module under test
mock_mw = MagicMock()
mock_gui_hooks = MagicMock()

sys.modules['aqt'] = MagicMock()
sys.modules['aqt'].mw = mock_mw
sys.modules['aqt.gui_hooks'] = mock_gui_hooks

# Now import the module
import anki_double_duty_hotkey

def test_get_config():
    # Setup
    mock_mw.addonManager.getConfig.return_value = {"hotkeys": {"1": "1"}}
    
    # Run
    config = anki_double_duty_hotkey.get_config()
    
    # Assert
    assert config == {"hotkeys": {"1": "1"}}
    mock_mw.addonManager.getConfig.assert_called_once()

def test_register_reviewer_shortcuts_question_state():
    # Setup
    mock_mw.addonManager.getConfig.return_value = {
        "hotkeys": {
            "1": "1",
            "h": "h"
        }
    }
    mock_mw.reviewer = MagicMock()
    
    # Define some initial shortcuts
    dummy_handler_1 = MagicMock()
    dummy_handler_h = MagicMock()
    shortcuts = [
        ("1", dummy_handler_1),
        ("h", dummy_handler_h),
        ("2", MagicMock())
    ]
    
    # Run shortcut registration
    anki_double_duty_hotkey.register_reviewer_shortcuts("review", shortcuts)
    
    # Verify shortcuts list is modified
    assert len(shortcuts) == 3
    keys = [item[0] for item in shortcuts]
    assert "1" in keys
    assert "h" in keys
    assert "2" in keys
    
    # Test Question State Behavior
    mock_mw.reviewer.state = "question"
    mock_mw.reviewer._showAnswer = MagicMock()
    
    # Find the registered custom handler for '1'
    custom_handler_1 = next(h for k, h in shortcuts if k == "1")
    custom_handler_1()
    
    # It should call _showAnswer
    mock_mw.reviewer._showAnswer.assert_called_once()
    dummy_handler_1.assert_not_called()

def test_register_reviewer_shortcuts_answer_state():
    # Setup
    mock_mw.addonManager.getConfig.return_value = {
        "hotkeys": {
            "1": "1",
            "h": "h"
        }
    }
    mock_mw.reviewer = MagicMock()
    
    dummy_handler_1 = MagicMock()
    dummy_handler_h = MagicMock()
    shortcuts = [
        ("1", dummy_handler_1),
        ("h", dummy_handler_h)
    ]
    
    # Run shortcut registration
    anki_double_duty_hotkey.register_reviewer_shortcuts("review", shortcuts)
    
    # Test Answer State Behavior for '1'
    mock_mw.reviewer.state = "answer"
    
    custom_handler_1 = next(h for k, h in shortcuts if k == "1")
    custom_handler_1()
    
    # On the back (answer) side, it should run the original handler for '1'
    dummy_handler_1.assert_called_once()

def test_register_reviewer_shortcuts_fallback():
    # Setup
    mock_mw.addonManager.getConfig.return_value = {
        "hotkeys": {
            "5": "5"
        }
    }
    mock_mw.reviewer = MagicMock()
    
    shortcuts = []
    anki_double_duty_hotkey.register_reviewer_shortcuts("review", shortcuts)
    
    mock_mw.reviewer.state = "answer"
    mock_mw.reviewer._answerCard = MagicMock()
    
    custom_handler_5 = next(h for k, h in shortcuts if k == "5")
    custom_handler_5()
    
    # It should call _answerCard(5)
    mock_mw.reviewer._answerCard.assert_called_once_with(5)

def test_register_reviewer_shortcuts_guard_when_no_reviewer():
    # Setup: reviewer is None (e.g. during startup or previewer initialization)
    mock_mw.reviewer = None
    shortcuts = [("1", MagicMock())]
    
    # Run shortcut registration
    anki_double_duty_hotkey.register_reviewer_shortcuts("review", shortcuts)
    
    # List should remain unmodified because the guard triggers
    assert len(shortcuts) == 1
