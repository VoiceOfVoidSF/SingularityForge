import pytest
import numpy as np
from simulation.utils import calculate_P

def test_calculate_P():
    t = np.linspace(0, 10, 100)
    delta_D = np.full(100, 0.1)
    U, I, N = np.full(100, 0.5), np.full(100, 0.3), np.full(100, 0.5)
    P = calculate_P(t, delta_D, U, I, N, U_mean=0.5, I_mean=0.3)
    assert abs(P - 0.45) < 0.1, "P calculation off"

def test_calculate_P_detailed():
    t = np.linspace(0, 10, 100)
    delta_D = np.full(100, 0.1)
    U, I, N = np.full(100, 0.5), np.full(100, 0.3), np.full(100, 0.5)
    result = calculate_P(t, delta_D, U, I, N, U_mean=0.5, I_mean=0.3, detailed=True)
    assert 'P' in result and 'contributions' in result
    assert abs(result['P'] - 0.45) < 0.1