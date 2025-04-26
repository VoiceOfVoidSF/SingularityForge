import networkx as nx
import numpy as np
import plotly.graph_objects as go
from utils import scenario_chaotic_pulse, calculate_P

def safe_fmt(val):
    return f"{val:.2f}" if isinstance(val, (float, int)) else str(val)

num_nodes = 80
t = np.linspace(0, 10, 100)
U_mean = 0.5
I_mean = 0.3

graph = nx.barabasi_albert_graph(num_nodes, 3)
for u, v in graph.edges():
    graph[u][v]['weight'] = 1.0

graph = scenario_chaotic_pulse(graph, node_d=0, t=t, U_mean=U_mean, I_mean=I_mean)

pos = nx.spring_layout(graph, seed=42)
for node in graph.nodes():
    graph.nodes[node]['pos'] = pos[node]

frames = []
slider_steps = []

for i, ti in enumerate(t[:-1]):
    edge_x, edge_y, hover_texts = [], [], []
    for u, v in graph.edges():
        x0, y0 = graph.nodes[u]['pos']
        x1, y1 = graph.nodes[v]['pos']
        edge_x += [x0, x1, None]
        edge_y += [y0, y1, None]

        P_t = graph[u][v].get('P_t', [0.0] * len(t))
        P_val = P_t[i] if i < len(P_t) else 0.0

        contrib = graph[u][v].get('P', {}).get('contributions', {})
        hover_text = (
            f"P = {P_val:.2f}<br>"
            f"ΔD = {safe_fmt(contrib.get('delta_D', '?'))}<br>"
            f"U/I = {safe_fmt(contrib.get('U_I', '?'))}<br>"
            f"N = {safe_fmt(contrib.get('N', '?'))}"
        )
        hover_texts.append(hover_text)

    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        mode='lines',
        line=dict(width=2, color='gray'),
        hoverinfo='text',
        text=hover_texts
    )

    node_x, node_y = zip(*[graph.nodes[n]['pos'] for n in graph.nodes()])
    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers',
        marker=dict(size=6, color='lightblue'),
        hoverinfo='text',
        text=[f"Node {n}" for n in graph.nodes()]
    )

    frame = go.Frame(data=[edge_trace, node_trace], name=str(i))
    frames.append(frame)

    slider_step = dict(
        method='animate',
        args=[[str(i)], dict(mode='immediate', frame=dict(duration=0), transition=dict(duration=0))],
        label=str(i)
    )
    slider_steps.append(slider_step)

sliders = [dict(
    active=0,
    currentvalue={"prefix": "Time step: "},
    pad={"t": 30},
    x=0.1, y=0,
    xanchor="left", yanchor="top",
    len=0.9,
    steps=slider_steps
)]

updatemenus = [dict(
    type="buttons",
    buttons=[dict(label="Play", method="animate", args=[None, dict(frame=dict(duration=100), fromcurrent=True)])],
    direction="left",
    pad={"r": 10, "t": 10},
    showactive=True,
    x=0.1, xanchor="right", y=0, yanchor="top"
)]

fig = go.Figure(
    data=frames[0].data,
    layout=go.Layout(
        title="Scenario: Chaotic Pulse (Slider Debug)",
        showlegend=False,
        hovermode='closest',
        height=700,
        margin=dict(l=20, r=20, t=60, b=100),
        sliders=sliders,
        updatemenus=updatemenus
    ),
    frames=frames
)

fig.write_html("mvp_output_slider_debug.html", include_plotlyjs='cdn', full_html=True)
print("✔ mvp_output_slider_debug.html создан.")
