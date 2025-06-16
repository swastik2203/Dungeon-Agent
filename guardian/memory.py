from typing import List, Dict, Any
import json

class Memory:
    def __init__(self):
        self.memories: List[Dict[str, Any]] = []

    def add(self, entry: Dict[str, Any]):
        self.memories.append(entry)

    def last(self, n=1):
        return self.memories[-n:]

    def all(self):
        return self.memories

    def save(self, filename: str):
        with open(filename, 'w') as f:
            json.dump(self.memories, f, indent=2)

    def load(self, filename: str):
        try:
            with open(filename, 'r') as f:
                self.memories = json.load(f)
        except FileNotFoundError:
            self.memories = []
