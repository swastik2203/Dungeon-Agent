from typing import Dict, Any, Callable

class Action:
    def __init__(self, name: str, preconditions: Dict[str, Callable[[Any], bool]], effects: Dict[str, Any], cost: int = 1):
        self.name = name
        self.preconditions = preconditions
        self.effects = effects
        self.cost = cost

    def is_applicable(self, state: Dict[str, Any]) -> bool:
        return all(cond(state.get(key)) for key, cond in self.preconditions.items())

    def apply(self, state: Dict[str, Any]) -> Dict[str, Any]:
        new_state = state.copy()
        for key, value in self.effects.items():
            if callable(value):
                new_state[key] = value(new_state.get(key))
            else:
                new_state[key] = value
        return new_state

    def __str__(self):
        return self.name

# Action definitions

def get_actions():
    actions = []

    # HealSelf
    actions.append(Action(
        name="HealSelf",
        preconditions={
            "hasPotion": lambda v: v is True,
            "health": lambda v: v < 70
        },
        effects={
            "health": lambda v: min(100, v + 50),
            "hasPotion": lambda v: False
        },
        cost=2
    ))

    # AttackEnemy
    actions.append(Action(
        name="AttackEnemy",
        preconditions={
            "enemyNearby": lambda v: v is True,
            "health": lambda v: v > 30,
            "stamina": lambda v: v >= 5
        },
        effects={
            "enemyNearby": lambda v: False,
            "stamina": lambda v: max(0, v - 5)
        },
        cost=2
    ))

    # Retreat
    actions.append(Action(
        name="Retreat",
        preconditions={
            "inSafeZone": lambda v: v is False,
            "stamina": lambda v: v >= 2
        },
        effects={
            "inSafeZone": lambda v: True,
            "stamina": lambda v: max(0, v - 2)
        },
        cost=1
    ))

    # DefendTreasure
    actions.append(Action(
        name="DefendTreasure",
        preconditions={
            "treasureThreatLevel": lambda v: v in ["medium", "high"],
            "enemyNearby": lambda v: v is False
        },
        effects={
            "treasureThreatLevel": lambda v: "low"
        },
        cost=2
    ))

    # CallBackup
    actions.append(Action(
        name="CallBackup",
        preconditions={
            "enemyNearby": lambda v: v is True
        },
        effects={
            "enemyNearby": lambda v: False
        },
        cost=3
    ))

    # SearchForPotion
    actions.append(Action(
        name="SearchForPotion",
        preconditions={
            "inSafeZone": lambda v: v is True,
            "hasPotion": lambda v: v is False
        },
        effects={
            "hasPotion": lambda v: True
        },
        cost=2
    ))

    return actions
