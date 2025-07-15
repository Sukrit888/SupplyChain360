import streamlit as st
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import random

st.set_page_config(page_title="SupplyChain360", layout="wide")
st.title("🌍 SupplyChain360 Dashboard")
st.markdown("Visualize and optimize your global supply chain operations in real-time.")

st.sidebar.header("🔧 Controls")
show_graph = st.sidebar.checkbox("Show Supply Chain Network", value=True)
opt_mode = st.sidebar.radio("Optimize for", ["Cost", "Time"], index=0)
inject_delay = st.sidebar.checkbox("Inject Random Delays", value=False)

nodes_df = pd.read_csv("data/global_supply_chain_nodes.csv")
edges_df = pd.read_csv("data/global_supply_chain_edges.csv")

G = nx.DiGraph()
for _, row in nodes_df.iterrows():
    G.add_node(row["node_id"], label=row["name"], type=row["type"], location=row["location"])
for _, row in edges_df.iterrows():
    G.add_edge(
        row["source"], row["target"],
        distance=row["distance_km"],
        time=row["avg_time_hr"],
        cost=row["cost_usd"]
    )

if show_graph:
    st.subheader("🗺️ Global Supply Chain Network")
    pos = nx.spring_layout(G, seed=42)
    node_colors = {
        "Supplier": "skyblue",
        "Factory": "orange",
        "Warehouse": "green",
        "Retailer": "salmon"
    }
    colors = [node_colors[G.nodes[n]["type"]] for n in G.nodes]

    fig, ax = plt.subplots(figsize=(10, 6))
    nx.draw_networkx_nodes(G, pos, node_color=colors, node_size=1000, edgecolors='black')
    nx.draw_networkx_labels(G, pos, labels={n: G.nodes[n]["label"] for n in G.nodes}, font_size=8)
    nx.draw_networkx_edges(G, pos, edge_color='gray', arrows=True, arrowsize=20)
    nx.draw_networkx_edge_labels(
        G, pos,
        edge_labels={(u, v): f"{d['distance']} km" for u, v, d in G.edges(data=True)},
        font_size=7
    )
    ax.set_title("Supply Chain Flow Map")
    ax.axis("off")
    st.pyplot(fig)

st.subheader("🚚 Shipment Path Simulation")

suppliers = nodes_df[nodes_df["type"] == "Supplier"]["node_id"].tolist()
retailers = nodes_df[nodes_df["type"] == "Retailer"]["node_id"].tolist()

col1, col2 = st.columns(2)
with col1:
    source_node = st.selectbox("Select Supplier", suppliers, index=0)
with col2:
    target_node = st.selectbox("Select Retailer", retailers, index=0)

best_path = []
best_cost = 0
best_time = 0
delays_included = False

try:
    all_paths = list(nx.all_simple_paths(G, source=source_node, target=target_node))
    if not all_paths:
        st.warning("No shipment path found between the selected nodes.")
    else:
        def calculate_metrics(path):
            total_cost = 0
            total_time = 0
            for i in range(len(path) - 1):
                edge_data = G.get_edge_data(path[i], path[i + 1])
                delay = random.randint(1, 5) if inject_delay else 0
                total_cost += edge_data["cost"]
                total_time += edge_data["time"] + delay
            return total_cost, total_time

    
        if opt_mode == "Cost":
            best_path = min(all_paths, key=lambda p: calculate_metrics(p)[0])
        else:
            best_path = min(all_paths, key=lambda p: calculate_metrics(p)[1])

        best_cost, best_time = calculate_metrics(best_path)
        delays_included = inject_delay

        st.success(f"📍 Best Path: {' → '.join(best_path)}")
        st.info(f"💰 Total Cost: ${best_cost} | ⏱️ Total Time: {best_time} hrs")
        if inject_delay:
            st.warning("⚠️ Random delays injected into time calculation.")

except nx.NetworkXNoPath:
    st.error("❌ No available shipment route between selected nodes.")

st.subheader("📊 KPI Dashboard")

if "simulation_history" not in st.session_state:
    st.session_state.simulation_history = []

if best_path:
    st.session_state.simulation_history.append({
        "source": source_node,
        "target": target_node,
        "path": best_path,
        "cost": best_cost,
        "time": best_time,
        "delayed": delays_included
    })

history = st.session_state.simulation_history
if history:
    avg_cost = sum(h["cost"] for h in history) / len(history)
    avg_time = sum(h["time"] for h in history) / len(history)
    most_efficient = min(history, key=lambda h: h["cost"])
    delay_count = sum(1 for h in history if h["delayed"])

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("📦 Total Simulations", len(history))
    col2.metric("💰 Avg. Cost", f"${avg_cost:.2f}")
    col3.metric("⏱️ Avg. Time", f"{avg_time:.1f} hrs")
    col4.metric("⚠️ Delayed Shipments", delay_count)

    st.success(
        f"🥇 Most Efficient Path: {most_efficient['source']} → {most_efficient['target']} "
        f"via {' → '.join(most_efficient['path'])}"
    )
else:
    st.info("No simulations yet. Run a shipment to generate KPIs.")
