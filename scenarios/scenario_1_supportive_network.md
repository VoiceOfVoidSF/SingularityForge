# Scenario 1: Conflict in a Supportive Network

## Description
Nodes A and B have a conflict (high P due to falling trust and impulsivity), but are embedded in a supportive network (high N(t)).

## Parameters
- delta_D: -0.2 (trust falling)
- U: 0.4 (moderate satisfaction)
- I: 0.8 (high impulsivity)
- N: 0.7 (strong network support)
- U_mean: 0.5, I_mean: 0.3
- alpha: 0.5, beta: 0.3, lambda: 0.1, T: 10

## Expected Outcome
P should decrease over time due to high N(t), indicating network stabilization.

## Example Call
```python
graph = scenario_supportive_network(graph, node_a=0, node_b=1, t=np.linspace(0, 10, 100), U_mean=0.5, I_mean=0.3)