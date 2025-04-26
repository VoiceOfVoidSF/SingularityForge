import numpy as np
import networkx as nx
import pandas as pd
import plotly.graph_objects as go
from utils import scenario_chaotic_pulse
import matplotlib.pyplot as plt
# === ПАРАМЕТРЫ ===
NUM_NODES = 40          # размер сети
EDGES_PER_STEP = 2      # параметр BA‑графа
T = 10                  # длительность симуляции
STEPS = 60              # дискретизация времени
U_MEAN, I_MEAN = 0.5, 0.3

# === ВРЕМЕННАЯ ШКАЛА ===
t = np.linspace(0, T, STEPS)

# === СОЗДАНИЕ ГРАФА ===
G = nx.barabasi_albert_graph(NUM_NODES, EDGES_PER_STEP, seed=42)

# Применяем сценарий хаотичного импульса (узел 0 как patient‑zero)
G = scenario_chaotic_pulse(G, node_d=0, t=t, U_mean=U_MEAN, I_mean=I_MEAN)

# === СОХРАНЯЕМ ВРЕМЕННЫЕ РЯДЫ ДЛЯ ОДНОГО ХАБ‑РЕБРА (0‑? первый сосед) ===
for u, v in G.edges():
    if u == 0:
        edge_data = G.edges[(u, v)]
        df = pd.DataFrame({
            'time': t[:-1],              # P_t на len(t)-1 значений
            'delta_D': edge_data['delta_D'][:-1],
            'U': edge_data['U'][:-1],
            'I': edge_data['I'][:-1],
            'N': edge_data['N'][:-1],
            'P': edge_data['P_t']
        })
        df.to_csv('scenario_chaotic_pulse.csv', index=False)
        break  # один CSV достаточно
sample = list(G.edges(data=True))[:10]
print('raw P for first 10 edges:',
      [round(e[-1]['P']['P_raw'], 3) for e in sample])
# === ПОДГОТАВЛИВАЕМ ПОЗИЦИИ ДЛЯ ОТОБРАЖЕНИЯ ===
pos = nx.spring_layout(G, seed=1)

# === ГОТОВИМ КАДРЫ ДЛЯ АНИМАЦИИ ===
frames = []
for frame_idx in range(STEPS-1):
    traces = []
    # Рёбра
    for (u, v) in G.edges():
        P_val = G.edges[(u, v)]['P_t'][frame_idx] if 'P_t' in G.edges[(u, v)] else 0.0
        contrib = G.edges[(u, v)].get('P', {}).get('contributions', {})
        r,g,b,_ = [int(255*x) for x in plt.get_cmap('RdYlBu_r')(P_val)]
        color   = f"rgba({r},{g},{b},1)"# оттенки красного
        hover = (
            f"P = {P_val:.2f}<br>"
            f"ΔD = {contrib.get('delta_D', 0):.2f}<br>"
            f"U/I = {contrib.get('U_I', 0):.2f}<br>"
            f"N = {contrib.get('N', 0):.2f}"
        )
        traces.append(go.Scatter(
            x=[pos[u][0], pos[v][0]],
            y=[pos[u][1], pos[v][1]],
            mode='lines',
            line=dict(color=color, width=2),
            hoverinfo='text',
            hovertext=hover,
            showlegend=False
        ))
    # Узлы поверх линий
    node_x, node_y = zip(*[pos[n] for n in G.nodes()])
    traces.append(go.Scatter(
        x=node_x, y=node_y,
        mode='markers',
        marker=dict(size=6, color='cyan'),
        hoverinfo='text',
        text=[f'Node {n}' for n in G.nodes()],
        showlegend=False
    ))
    frames.append(go.Frame(data=traces, name=str(frame_idx)))

# === НАЧАЛЬНЫЙ КАДР ===
fig = go.Figure(frames[0].data, frames=frames)

# === СЛАЙДЕР ===
slider_steps = [
    dict(method='animate',
            args=[[str(k)], {'mode': 'immediate', 'frame': {'duration': 100, 'redraw': True}}],
            label=str(round(t[k], 2)))
    for k in range(STEPS-1)
]
sliders = [dict(steps=slider_steps,
                x=0.05, y=-0.05,
                currentvalue=dict(prefix='t = '))]

# === КНОПКА ПУСК ===
play_button = [dict(type='buttons',
                    buttons=[dict(label='Play',
                                    method='animate',
                                    args=[None, {'frame': {'duration': 150, 'redraw': True},
                                                'fromcurrent': True}])],
                    showactive=False,
                    x=0.05, y=-0.15)]

# === ОБЩИЙ LAYOUT ===
fig.update_layout(title='Chaotic Pulse ‑ Real Model (utils.py)',
                    xaxis=dict(visible=False),
                    yaxis=dict(visible=False),
                    sliders=sliders,
                    updatemenus=play_button,
                    plot_bgcolor='black',
                    paper_bgcolor='black')

# === СОХРАНЯЕМ ===
fig.write_html('mvp_final.html')
print('Готово: mvp_final.html + scenario_chaotic_pulse.csv')