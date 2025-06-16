from typing import Dict, Any, List
from guardian.goap import Goal

class CognitiveEngine:
    def __init__(self, memory):
        self.memory = memory

    def select_goal(self, state: Dict[str, Any]) -> Goal:
        # Deterministic logic for goal selection
        if state["health"] < 35:
            if not state["hasPotion"]:
                return Goal("Survive", {"inSafeZone": lambda v: v is True})
            else:
                return Goal("Survive", {"health": lambda v: v >= 70})
        if state["enemyNearby"] and state["health"] > 40:
            if state["treasureThreatLevel"] == "high":
                return Goal("EliminateThreat", {"enemyNearby": lambda v: v is False, "treasureThreatLevel": lambda v: v == "low"})
            else:
                return Goal("EliminateThreat", {"enemyNearby": lambda v: v is False})
        if state["stamina"] < 5:
            return Goal("PrepareForBattle", {"stamina": lambda v: v >= 10})
        if not state["enemyNearby"] and state["treasureThreatLevel"] != "low":
            return Goal("ProtectTreasure", {"treasureThreatLevel": lambda v: v == "low"})
        return Goal("Patrol", {"inSafeZone": lambda v: v is True})

    def justify_goal(self, goal: Goal, state: Dict[str, Any]) -> str:
        # Natural language justification
        if goal.name == "Survive":
            if state["health"] < 35 and not state["hasPotion"]:
                return "My health is critically low and I have no potions. I must reach a safe zone to survive."
            elif state["health"] < 35:
                return "My health is low, but I have a potion. Healing is my top priority."
        if goal.name == "EliminateThreat":
            if state["health"] > 40 and state["enemyNearby"]:
                return "I am healthy and an enemy is nearby. Eliminating the threat is my priority."
        if goal.name == "ProtectTreasure":
            return "The treasure is under threat. I must ensure its safety."
        if goal.name == "PrepareForBattle":
            return "My stamina is low. I should recover before the next fight."
        if goal.name == "Patrol":
            return "No immediate threat. I will patrol and stay alert."
        return f"I chose the goal: {goal.name} based on the current situation."

    def reflect_on_failure(self, last_plan: List[str], state: Dict[str, Any], reason: str) -> str:
        # Natural language reflection
        if "HealSelf" in last_plan and not state["hasPotion"]:
            return "I failed to heal because I had no potion. Next time, I should search for potions before engaging."
        if "AttackEnemy" in last_plan and state["health"] < 30:
            return "Attacking was too risky with low health. I should prioritize survival."
        return f"Plan failed due to: {reason}. I will adapt my strategy."
