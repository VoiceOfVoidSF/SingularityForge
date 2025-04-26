import numpy as np

def calculate_P(
    t: np.ndarray,
    delta_D: np.ndarray,
    U: np.ndarray,
    I: np.ndarray,
    N: np.ndarray,
    U_mean: float,
    I_mean: float,
    alpha: float = 0.5,
    beta: float = 0.3,
    lambda_: float = 0.1,
    T: float = 10,
    detailed: bool = False
) -> float | dict:
    """Calculate probability of destructive impulse P for an edge."""
    for name, arr in [('t', t), ('delta_D', delta_D), ('U', U), ('I', I), ('N', N)]:
        if not isinstance(arr, np.ndarray):
            raise TypeError(f"{name} must be a NumPy array, got {type(arr)}")
        if arr.ndim != 1:
            raise ValueError(f"{name} must be a 1D array, got shape {arr.shape}")
    length = len(t)
    for name, arr in [('delta_D', delta_D), ('U', U), ('I', I), ('N', N)]:
        if len(arr) != length:
            raise ValueError(f"Length mismatch: {name} has length {len(arr)}, but t has length {length}")
    if not isinstance(U_mean, (float, int)) or not isinstance(I_mean, (float, int)):
        raise TypeError("U_mean and I_mean must be floats")

    decay = np.exp(-lambda_ * (T - t))
    delta_D_term = delta_D
    U_I_term = alpha * (U / U_mean) * (I / I_mean)
    N_term = -beta * N  # Negative to reduce P for strong networks
    integrand = delta_D_term + U_I_term + N_term
    denominator = np.trapz(decay, t)
    P_raw = np.trapz(integrand * decay, t) / denominator if denominator else 0.0
    P = np.trapz(integrand * decay, t) / denominator if denominator != 0 else 0.0
    #P = np.clip(P, 0, 1)

    #   P_raw без жёсткой обрезки
    P_raw = np.trapz(integrand * decay, t) / denominator if denominator else 0.0

    # нормализуем к диапазону 0-1, выбрав «разумный максимум» модели
    P_max = 4.0          # подбирается опытно
    P = np.clip(P_raw / P_max, 0, 1)

    if detailed:
        return {
            'P': P,
            'P_raw' : P_raw, # сырое значение P без нормализации
            'contributions': {
                'delta_D': np.trapz(delta_D_term * decay, t) / T,
                'U_I': np.trapz(U_I_term * decay, t) / T,
                'N': np.trapz(N_term * decay, t) / T
            }
        }
    return P

def generate_synthetic_data(n_nodes, T=10):
    """Generate synthetic data for U, I, delta_D, N."""
    t = np.linspace(0, T, 100)
    U = np.random.normal(0.5, 0.1, n_nodes)
    I = np.random.gamma(2, 0.2, n_nodes)
    delta_D = np.cumsum(np.random.normal(0, 0.05, n_nodes))
    N = np.full(n_nodes, 0.5)
    return t, U, I, delta_D, N

def scenario_supportive_network(graph, node_a, node_b, t, U_mean, I_mean):
    """Scenario: Conflict with supportive network."""
    edge = graph[node_a][node_b]
    edge['delta_D'] = np.full(len(t), -0.2)
    edge['U'] = np.full(len(t), 0.4)
    edge['I'] = np.full(len(t), 0.6)  # Уменьшено для меньшей импульсивности
    edge['N'] = np.full(len(t), 0.7)
    edge['P'] = calculate_P(t, edge['delta_D'], edge['U'], edge['I'], edge['N'], U_mean, I_mean, detailed=True)
    return graph

def scenario_isolated_threat(graph, node_a, node_b, t, U_mean, I_mean):
    """Scenario: Isolated threat with low N(t)."""
    edge = graph[node_a][node_b]
    edge['delta_D'] = np.random.normal(-0.1, 0.05, len(t))
    edge['U']       = np.random.normal(0.5,  0.05, len(t))
    edge['I']       = np.random.normal(0.3,  0.08, len(t))
    edge['N']       = np.random.normal(0.5,  0.10, len(t))
    edge['P'] = calculate_P(t, edge['delta_D'], edge['U'], edge['I'], edge['N'], U_mean, I_mean, detailed=True)
    return graph

def scenario_chaotic_pulse(graph, node_d, t, U_mean, I_mean,
                           spike=0.6,                  # амплитуда импульса
                           hub_boost=1.4,              # усиление в хабах
                           threshold=0.3):             # порог волны
    # 1. генерируем всплеск импульсивности узла D
    node_spike = np.random.uniform(0.2, 0.9, len(t))
    node_spike += spike                                # смещаем вверх
    graph.nodes[node_d]['I'] = node_spike

    for nbr in graph.neighbors(node_d):
        edge = graph[node_d][nbr]

        # 2. копируем импульс узла в ребро (ключевой момент!)
        edge['I'] = node_spike.copy()                  # теперь I меняется
        edge['delta_D'] = np.full(len(t), -0.1)
        edge['U']       = np.full(len(t), 0.5)
        edge['N']       = np.full(len(t), 0.5)
    
        # 3. считаем P по полной траектории
        edge['P'] = calculate_P(t, edge['delta_D'], edge['U'],
                                edge['I'], edge['N'],
                                U_mean, I_mean, detailed=True)

        # 4. если риск выше порога — усиливаем импульс соседу
        #if edge['P']['P'] > threshold:
        #    edge['I'] += 0.2                           # «волна»
        #    edge['P'] = calculate_P(t, edge['delta_D'], edge['U'],
        #                            edge['I'], edge['N'],
        #                            U_mean, I_mean, detailed=True)

        if edge['P']['P'] > threshold:
            for nbr2 in graph.neighbors(nbr):
                if nbr2 == node_d:
                    continue                                  # назад не передаём
                sub_edge = graph[nbr][nbr2]
                if 'I' not in sub_edge:
                    # инициализируем, если это первое касание волны
                    sub_edge['delta_D'] = np.full(len(t), -0.05)
                    sub_edge['U']       = np.full(len(t), 0.5)
                    sub_edge['I']       = np.full(len(t), 0.25)   # базовая I
                    sub_edge['N']       = np.full(len(t), 0.5)
                sub_edge['I'] += 0.05                             # маленькая волна
                sub_edge['P'] = calculate_P(t, sub_edge['delta_D'],
                                            sub_edge['U'], sub_edge['I'],
                                            sub_edge['N'], U_mean, I_mean,
                                            detailed=True)
                # записываем временной ряд, если ещё не был построен
                if 'P_t' not in sub_edge:
                    sub_edge['P_t'] = [
                        calculate_P(t[:k+1],
                                    sub_edge['delta_D'][:k+1],
                                    sub_edge['U'][:k+1],
                                    sub_edge['I'][:k+1],
                                    sub_edge['N'][:k+1],
                                    U_mean, I_mean, detailed=True)['P']
                        for k in range(1, len(t))
                    ]        

        # 5. усиление в хабах
        if graph.degree[nbr] > 5:
            edge['P']['P'] *= hub_boost

        # 6. формируем временной ряд P_t
        P_t = []
        for k in range(1, len(t)):
            P_t.append(
                calculate_P(t[k:k+2],
                            edge['delta_D'][k:k+2],
                            edge['U'][k:k+2],
                            edge['I'][k:k+2],
                            edge['N'][k:k+2],
                            U_mean, I_mean, detailed=True)['P']
            )

        graph.edges[(node_d, nbr)]['P_t'] = P_t
    return graph
