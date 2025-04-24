## Simulation: Logic

The simulation implements the "Architecture of Connections" model, calculating the probability of destructive impulses (P) for edges in a social network graph. Key components:
- `utils.py`: Contains `calculate_P` (computes P), `generate_synthetic_data` (generates U, I, delta_D, N), and scenario functions.
- Scenarios: Three test cases (supportive network, isolated threat, chaotic pulse) in `/scenarios`.
- Tests: Validation in `/simulation/tests`.

To run:
```bash
PYTHONPATH=M:\SingularityForge pytest simulation/tests --log-file=test_log.txt --junitxml=test_report.xml
python simulation/mvp.py --scenario supportive_network