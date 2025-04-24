# Scenario 2: Isolated Threat

## Description
Nodes A and B have a high P due to low trust and weak network support.

## Parameters
- delta_D: -0.3 (severe trust drop)
- U: 0.3 (low satisfaction)
- I: 0.9 (very high impulsivity)
- N: 0.2 (weak network)
- U_mean: 0.5, I_mean: 0.3
- alpha: 0.5, beta: 0.3, lambda: 0.1, T: 10

## Expected Outcome
P remains high, indicating a need for intervention.

## Example Call
```python
graph = scenario_isolated_threat(graph, node_a=0, node_b=1, t=np.linspace(0, 10, 100), U_mean=0.5, I_mean=0.3)