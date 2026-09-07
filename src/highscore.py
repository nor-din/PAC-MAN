import json
import os
from typing import List, Dict, Any


class HighScoreManager:
    def __init__(self, filename: str = "highscores.json"):
        self.filename = filename
        self.scores: List[Dict[str, Any]] = self._load_scores()

    def _load_scores(self) -> List[Dict[str, Any]]:
        if not os.path.exists(self.filename):
            return []
        try:
            with open(self.filename, "r") as file:
                data = json.load(file)
                if isinstance(data, list):
                    return data
                return []
        except Exception as e:
            print(f"Warning: Failed to load highscores ({e}). Starting fresh.")
            return []

    def save_scores(self) -> None:
        try:
            with open(self.filename, "w") as file:
                json.dump(self.scores, file, indent=4)
        except Exception as e:
            print(f"Warning: Failed to save highscores ({e}).")

    def add_score(self, name: str, score: int) -> None:
        """
        Adds a score and keeps only the top 10.
        """
        # Clean name: alphanumeric and space only, max 10 chars
        clean_name = "".join([c for c in name if c.isalnum() or c == " "])[:10]
        if not clean_name:
            clean_name = "ANONYMOUS"

        self.scores.append({"name": clean_name, "score": score})
        # Sort descending by score
        self.scores.sort(key=lambda x: x["score"], reverse=True)
        # Keep top 10
        self.scores = self.scores[:10]
        self.save_scores()

    def get_top_scores(self) -> List[Dict[str, Any]]:
        return self.scores
