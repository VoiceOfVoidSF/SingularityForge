# GLOSSARY.md

## Notation Conventions

| Symbol         | Meaning                                | Typical Range / Units         |
|----------------|----------------------------------------|-------------------------------|
| t              | Time                                  | 0...T (discrete)              |
| ΔD(t)          | Change in Trust                       | -0.3...+0.1 (dimensionless)   |
| U(t), Ū        | Life Satisfaction, Baseline           | 0...1 (dimensionless)         |
| I(t), Ī        | Impulsivity, Baseline                 | 0...1 (dimensionless)         |
| N(t)           | Network Influence                     | 0...1 (dimensionless)         |
| α, β, λ        | Model Coefficients                    | Positive real numbers         |
| P              | Probability of Destructive Impulse    | 0...1 (dimensionless)         |

## Formula Explanation

**P = ∫[ΔD(t) + α(U/Ū)(I/Ī) - βN(t)]e^(-λ(T-t))dt**

- ΔD(t): Change in trust dynamics
- α(U/Ū)(I/Ī): Normalized individual factors
- βN(t): Network influence (reduces risk; negative sign in formula)
- e^(-λ(T-t)): Temporal decay factor
- P is normalized and clipped to [0, 1]

_Examples from real simulations will be added as soon as MVP data is available._

_See /docs/graphs/ for visualizations of scenario dynamics._

## Scenarios

1. **Supportive Network**
   - High N(t)
   - Low ΔD(t)
   - Expected P: Decreasing

2. **Isolated Threat**
   - Low N(t)
   - Rapid ΔD(t) decrease
   - Expected P: Increasing

3. **Chaotic Pulse**
   - Fluctuating N(t)
   - Erratic ΔD(t)
   - Expected P: Unstable

## Data Format Example

CSV structure:
`time,delta_D,U,I,N,P`

Sample row:
`10, -0.15, 0.8, 0.4, 0.6, 0.32`