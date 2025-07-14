
import streamlit as st
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

st.set_page_config(page_title="SupplyChain360", layout="wide")

st.title("🌍 SupplyChain360 Dashboard")
st.markdown("Visualize and optimize your global supply chain operations in real-time.")

# Sidebar
st.sidebar.header("🔧 Controls")
show_graph = st.sidebar.checkbox("Show Supply Chain Network", value=True)

# Load data
nodes_df = pd.read_csv("data/global_supply_chain_nodes.csv")
edges_df = pd.read_csv("data/global_supply_chain_edges.csv")

# Build graph
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

# Show Graph
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

# Shipment Simulation
st.subheader("🚚 Shipment Path Simulation")

# --- Filter source and target nodes ---
suppliers = nodes_df[nodes_df["type"] == "Supplier"]["node_id"].tolist()
retailers = nodes_df[nodes_df["type"] == "Retailer"]["node_id"].tolist()

col1, col2 = st.columns(2)
with col1:
    source_node = st.selectbox("Select Supplier", suppliers, index=0)
with col2:
    target_node = st.selectbox("Select Retailer", retailers, index=0)

# --- Find all paths ---
try:
    all_paths = list(nx.all_simple_paths(G, source=source_node, target=target_node))
    if not all_paths:
        st.warning("No shipment path found between the selected nodes.")
    else:
        # Evaluate all paths and pick the best (shortest by cost)
        def calculate_metrics(path):
            total_cost = 0
            total_time = 0
            for i in range(len(path) - 1):
                edge_data = G.get_edge_data(path[i], path[i+1])
                total_cost += edge_data["cost"]
                total_time += edge_data["time"]
            return total_cost, total_time

        best_path = min(all_paths, key=lambda p: calculate_metrics(p)[0])
        best_cost, best_time = calculate_metrics(best_path)

        st.success(f"📍 Best Path: {' → '.join(best_path)}")
        st.info(f"💰 Total Cost: ${best_cost} | ⏱️ Total Time: {best_time} hrs")

except nx.NetworkXNoPath:
    st.error("❌ No available shipment route between selected nodes.")


# --- KPI Dashboard ---
st.subheader("📊 KPI Dashboard")

# Initialize session state for simulations
if "simulation_history" not in st.session_state:
    st.session_state.simulation_history = []

# Record the current simulation
if best_path:
    st.session_state.simulation_history.append({
        "source": source_node,
        "target": target_node,
        "path": best_path,
        "cost": best_cost,
        "time": best_time
    })

# Display KPIs
history = st.session_state.simulation_history
if history:
    avg_cost = sum(h["cost"] for h in history) / len(history)
    avg_time = sum(h["time"] for h in history) / len(history)
    most_efficient = min(history, key=lambda h: h["cost"])

    col1, col2, col3 = st.columns(3)
    col1.metric("📦 Total Simulations", len(history))
    col2.metric("💰 Avg. Cost", f"${avg_cost:.2f}")
    col3.metric("⏱️ Avg. Time", f"{avg_time:.1f} hrs")

    st.success(f"🥇 Most Efficient Path: {most_efficient['source']} → {most_efficient['target']} via {' → '.join(most_efficient['path'])}")
else:
    st.info("No simulations yet. Run a shipment to generate KPIs.")
