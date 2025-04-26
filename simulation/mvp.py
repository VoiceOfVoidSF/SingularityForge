import networkx as nx
import numpy as np
import plotly.graph_objects as go
from utils import scenario_chaotic_pulse

# 1. Создание графа и позиции узлов
G = nx.barabasi_albert_graph(80, 2)
pos = nx.spring_layout(G, seed=42)

# 2. Параметры времени и базовые значения
t = np.linspace(0, 10, 100)
U_mean = 0.5
I_mean = 0.3

# 3. Применение сценария с волной
G = scenario_chaotic_pulse(G, node_d=0, t=t, U_mean=U_mean, I_mean=I_mean)

# 4. Визуализация
fig = go.Figure()

# 4.1. Серый фон: все рёбра
edge_x, edge_y = [], []
for u, v in G.edges():
    x0, y0 = pos[u]
    x1, y1 = pos[v]
    edge_x.extend([x0, x1, None])
    edge_y.extend([y0, y1, None])

fig.add_trace(go.Scatter(
    x=edge_x, y=edge_y,
    mode='lines',
    line=dict(width=1, color='rgba(100,100,100,0.2)'),
    hoverinfo='none'
))

# 4.2. Цветные рёбра на основе P_t
for edge in G.edges():
    if 'P_t' not in G.edges[edge] or 'P' not in G.edges[edge]:
        continue

    final_P = G.edges[edge]['P_t'][-1]
    contrib = G.edges[edge].get('P', {}).get('contributions', {})
    delta_d = contrib.get('delta_D', 0.0)
    u_i = contrib.get('U_I', 0.0)
    n_val = contrib.get('N', 0.0)

    # Цвет: логарифмическая шкала
    scaled = np.log10(final_P + 0.01)
    scaled = max(min((scaled + 2) / 2, 1.0), 0.0)
    intensity = int(255 * scaled)
    color = f"rgba({intensity}, 0, 0, 1)"

    x0, y0 = pos[edge[0]]
    x1, y1 = pos[edge[1]]
    hover_text = f"Edge {edge}<br>P = {final_P:.3f}<br>ΔD: {delta_d:.2f}, U/I: {u_i:.2f}, N: {n_val:.2f}"

    fig.add_trace(go.Scatter(
        x=[x0, x1], y=[y0, y1],
        mode='lines',
        line=dict(color=color, width=2),
        hoverinfo='text',
        text=[hover_text]
    ))

# 4.3. Узлы
node_x, node_y = zip(*[pos[n] for n in G.nodes()])
fig.add_trace(go.Scatter(
    x=node_x, y=node_y,
    mode='markers',
    marker=dict(size=6, color='cyan'),
    hoverinfo='text',
    text=[f"Node {n}" for n in G.nodes()]
))

# 5. Оформление
fig.update_layout(
    title='Architecture of Connections: Chaotic Pulse Scenario',
    showlegend=False,
    plot_bgcolor='black',
    paper_bgcolor='black',
    font=dict(color='white'),
    xaxis=dict(showgrid=True, zeroline=False),
    yaxis=dict(showgrid=True, zeroline=False)
)

# 6. Сохранение
fig.write_html("M:/SingularityForge/simulation/mvp_output.html")
print("✅ mvp_output.html создан успешно.")