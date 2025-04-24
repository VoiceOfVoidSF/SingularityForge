# Scenario 3: Chaotic Impulse

## Description
Node D generates a chaotic impulse (spike in I(t)), affecting neighbors. Wave propagates if P > 0.7, amplified in hubs.

## Parameters
- Node D I(t): Random [0.2, 0.9]
- Edge delta_D: -0.1 (mild trust drop)
- Edge U: 0.5 (average satisfaction)
- Edge I: 0.3 (base impulsivity)
- Edge N: 0.5 (average network)
- U_mean: 0.5, I_mean: 0.3
- alpha: 0.5, beta: 0.3, lambda: 0.1, T: 10

## Expected Outcome
P increases for edges near D, but supportive networks dampen the wave. Hubs amplify P by 20%.

## Example Call
```python
graph = scenario_chaotic_pulse(graph, node_d=0, t=np.linspace(0, 10, 100), U_mean=0.5, I_mean=0.3)