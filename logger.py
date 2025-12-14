import logging
import json
from datetime import datetime


state_logger = logging.getLogger("game_state")
state_logger.setLevel(logging.INFO)
event_logger = logging.getLogger("game_events")
event_logger.setLevel(logging.INFO)

state_handler = logging.FileHandler("game_state.jsonl", mode="w", encoding="utf-8")
event_handler = logging.FileHandler("game_events.jsonl", mode="w", encoding="utf-8")

formatter = logging.Formatter("%(message)s")
state_handler.setFormatter(formatter)
event_handler.setFormatter(formatter)

state_logger.addHandler(state_handler)
event_logger.addHandler(event_handler)

def log_state(entry: dict):
    """Log a game state snapshot as JSON to game_state.jsonl."""
    json_line = json.dumps(entry)
    state_logger.info(json_line)

def log_event(entry: dict):
    """Log a game event as JSON to game_events.jsonl."""
    json_line = json.dumps(entry)
    event_logger.info(json_line)