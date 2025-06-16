from typing import Dict, Any, List, Callable, Optional
from guardian.actions import get_actions, Action

class Goal:
    def __init__(self, name: str, conditions: Dict[str, Callable[[Any], bool]], priority: int = 1):
        self.name = name
        self.conditions = conditions
        self.priority = priority

    def is_satisfied(self, state: Dict[str, Any]) -> bool:
        return all(cond(state.get(key)) for key, cond in self.conditions.items())

    def __str__(self):
        return self.name

# Simple forward search planner (not optimal, but sufficient for this assignment)
def plan(state: Dict[str, Any], goal: Goal, max_depth: int = 5) -> Optional[List[Action]]:
    actions = get_actions()
    path = []
    visited = set()

    def dfs(current_state, depth):
        if goal.is_satisfied(current_state):
            return []
        if depth == 0:
            return None
        state_tuple = tuple(sorted(current_state.items()))
        if state_tuple in visited:
            return None
        visited.add(state_tuple)
        for action in actions:
            if action.is_applicable(current_state):
                next_state = action.apply(current_state)
                subplan = dfs(next_state, depth - 1)
                if subplan is not None:
                    return [action] + subplan
        return None

    result = dfs(state, max_depth)
    return result
