# Dungeon Guardian

## Overview

The Sentient Guardian is an autonomous NPC agent designed to protect a dungeon using a combination of symbolic GOAP-style planning and LLM-inspired reasoning. The agent reasons, plans, adapts, and justifies its actions using a simulated internal monologue.

## Features

- **World Model**: Tracks health, stamina, potion count, treasure threat, enemy presence, and safe zone status.
- **GOAP Planning**: Symbolic planner for action selection and sequencing.
- **Cognitive Layer**: Mocked LLM/prompt engine for goal generation, justification, and reflection.
- **Execution Layer**: Simulates world state, action outcomes, interruptions, and replanning.
- **Memory**: Tracks failures and outcomes to improve future decisions.

## How It Works

1. The agent observes the world state.
2. The cognitive layer sets goals and justifies them.
3. The GOAP planner generates a plan to achieve the goal.
4. The execution layer simulates actions, updates the world, and handles interruptions.
5. The agent reflects on failures and adapts its strategy.

## Running the Simulation

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   or create venv and source venv/bin/activate
   then u can run the application byu using this.
   ```
2. **Run the main simulation:**
   ```bash
   python3 guardian/main.py
   or
   PYTHONPATH=. python3 guardian/main.py
   ```

## Scenarios

Sample scenarios are implemented in `main.py` and can be modified or extended.

## Output

Console logs show the agent's thoughts, plans, actions, and reflections.

---

For questions or to submit, see the assignment instructions.
