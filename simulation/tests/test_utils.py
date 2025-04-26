import numpy as np
from simulation.utils import calculate_P

def test_calculate_P():
    t = np.linspace(0, 10, 100)
    delta_D = np.full(100, 0.1)
    U, I, N = np.full(100, 0.5), np.full(100, 0.3), np.full(100, 0.5)
    P = calculate_P(t, delta_D, U, I, N, U_mean=0.5, I_mean=0.3)
    assert 0.0 <= P <= 1.0, "P should be within [0, 1]"
    assert isinstance(P, float), "P should be a float"
    assert np.all(np.isfinite(P)), "P should be finite"



def test_calculate_P_detailed():
    t = np.linspace(0, 10, 100)
    delta_D = np.full(100, 0.1)
    U, I, N = np.full(100, 0.5), np.full(100, 0.3), np.full(100, 0.5)
    result = calculate_P(t, delta_D, U, I, N, U_mean=0.5, I_mean=0.3, detailed=True)
    assert 'P' in result and 'contributions' in result
    assert 0.0 <= result['P'] <= 1.0, "Normalized P should be between 0 and 1"
    assert 'delta_D' in result['contributions']
    assert 'U_I' in result['contributions']
    assert 'N' in result['contributions']
    assert isinstance(result['contributions']['delta_D'], float), "delta_D contribution should be a float"
    assert isinstance(result['contributions']['U_I'], float), "U_I contribution should be a float"
    assert isinstance(result['contributions']['N'], float), "N contribution should be a float"

