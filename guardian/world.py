from typing import Dict, Any

class WorldState:
    def __init__(self, state: Dict[str, Any]):
        self.state = state.copy()

    def update(self, updates: Dict[str, Any]):
        self.state.update(updates)

    def __getitem__(self, key):
        return self.state[key]

    def __setitem__(self, key, value):
        self.state[key] = value

    def as_dict(self):
        return self.state.copy()

    def __str__(self):
        lines = [f"{k}: {v}" for k, v in self.state.items()]
        return "\n".join(lines)

# Example world state keys:
# health, stamina, hasPotion, treasureThreatLevel, enemyNearby, inSafeZone
