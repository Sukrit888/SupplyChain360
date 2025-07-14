
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

st.success("✅ Streamlit skeleton loaded. Add simulation, KPIs, and filters next!")
