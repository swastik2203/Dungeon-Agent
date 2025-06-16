from guardian.world import WorldState
from guardian.actions import get_actions
from guardian.goap import plan
from guardian.cognitive import CognitiveEngine
from guardian.memory import Memory
from tabulate import tabulate

# Scenario definitions
SCENARIO_1 = {
    "health": 20,
    "enemyNearby": True,
    "hasPotion": False,
    "treasureThreatLevel": "medium",
    "stamina": 5,
    "inSafeZone": False
}

SCENARIO_2 = {
    "health": 85,
    "enemyNearby": True,
    "hasPotion": True,
    "treasureThreatLevel": "high",
    "stamina": 15,
    "inSafeZone": False
}

SCENARIO_3 = {
    "health": 70,
    "enemyNearby": False,
    "hasPotion": True,
    "treasureThreatLevel": "low",
    "stamina": 2,
    "inSafeZone": True
}

SCENARIO_4 = {
    "health": 60,
    "enemyNearby": True,
    "hasPotion": False,
    "treasureThreatLevel": "low",
    "stamina": 10,
    "inSafeZone": False
}

SCENARIO_5 = {
    "health": 30,
    "enemyNearby": True,
    "hasPotion": True,
    "treasureThreatLevel": "high",
    "stamina": 10,
    "inSafeZone": False
}

SCENARIOS = [
    (SCENARIO_1, "Scenario 1: Low Health, No Healing Resources, Enemy Nearby"),
    (SCENARIO_2, "Scenario 2: Healthy, Treasure Under Threat, Enemy Nearby"),
    (SCENARIO_3, "Scenario 3: No Enemy Nearby, Low Stamina, Potion Available"),
    (SCENARIO_4, "Scenario 4: Out of Potions, Enemy Near, Treasure Safe"),
    (SCENARIO_5, "Scenario 5: Interrupted During Plan Execution")
]

def run_scenario(initial_state_dict, scenario_name="Scenario", interrupt_heal=False):
    print(f"\n=== {scenario_name} ===")
    state = WorldState(initial_state_dict)
    memory = Memory()
    cognitive = CognitiveEngine(memory)
    print("Initial World State:")
    print(tabulate(state.as_dict().items(), headers=["Key", "Value"]))

    # 1. Cognitive Layer: Select goal
    goal = cognitive.select_goal(state.as_dict())
    print(f"\nChosen Goal: {goal}")
    print("Justification:", cognitive.justify_goal(goal, state.as_dict()))

    # 2. Planning Layer: Plan
    plan_actions = plan(state.as_dict(), goal, max_depth=8)
    if not plan_actions:
        print("No valid plan found for this goal.")
        return
    print("\nPlanned Actions:", " -> ".join([a.name for a in plan_actions]))

    # 3. Execution Layer: Simulate
    for idx, action in enumerate(plan_actions):
        print(f"\nStep {idx+1}: {action.name}")
        # Simulate interruption for Scenario 5: Healing fails
        if interrupt_heal and action.name == "HealSelf":
            print("Action failed: Potion was stolen or spoiled!")
            state["hasPotion"] = False
            reason = "Potion was stolen or spoiled."
            reflection = cognitive.reflect_on_failure([a.name for a in plan_actions], state.as_dict(), reason)
            print("Reflection:", reflection)
            memory.add({"failure": reason, "state": state.as_dict(), "plan": [a.name for a in plan_actions]})
            break
        if not action.is_applicable(state.as_dict()):
            reason = f"Preconditions for {action.name} not met."
            print(f"Action failed: {reason}")
            reflection = cognitive.reflect_on_failure([a.name for a in plan_actions], state.as_dict(), reason)
            print("Reflection:", reflection)
            memory.add({"failure": reason, "state": state.as_dict(), "plan": [a.name for a in plan_actions]})
            break
        state.update(action.apply(state.as_dict()))
        print("World State:")
        print(tabulate(state.as_dict().items(), headers=["Key", "Value"]))
    else:
        print("\nPlan executed successfully.")

    # For Scenario 5, after interruption, replan
    if interrupt_heal:
        print("\n--- Replanning after interruption ---")
        goal = cognitive.select_goal(state.as_dict())
        print(f"New Goal: {goal}")
        print("Justification:", cognitive.justify_goal(goal, state.as_dict()))
        plan_actions = plan(state.as_dict(), goal, max_depth=8)
        if not plan_actions:
            print("No valid plan found for this goal.")
            return
        print("New Planned Actions:", " -> ".join([a.name for a in plan_actions]))
        for idx, action in enumerate(plan_actions):
            print(f"Step {idx+1}: {action.name}")
            if not action.is_applicable(state.as_dict()):
                reason = f"Preconditions for {action.name} not met."
                print(f"Action failed: {reason}")
                reflection = cognitive.reflect_on_failure([a.name for a in plan_actions], state.as_dict(), reason)
                print("Reflection:", reflection)
                memory.add({"failure": reason, "state": state.as_dict(), "plan": [a.name for a in plan_actions]})
                break
            state.update(action.apply(state.as_dict()))
            print("World State:")
            print(tabulate(state.as_dict().items(), headers=["Key", "Value"]))
        else:
            print("Plan executed successfully after replanning.")

if __name__ == "__main__":
    for i, (scenario, name) in enumerate(SCENARIOS):
        if i == 4:
            run_scenario(scenario, name, interrupt_heal=True)
        else:
            run_scenario(scenario, name)
