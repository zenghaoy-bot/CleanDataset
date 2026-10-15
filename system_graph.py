import networkx as nx
import matplotlib.pyplot as plt

def draw_ecosystem_graph(G, title="Third-party Ecosystem Graph", save_path=None):
    pos = nx.spring_layout(G, seed=42)

    # create canvas
    plt.figure(figsize=(12,9))

    # nodes
    nx.draw_networkx_nodes(
        G, pos,
        node_size=3000,
        node_color="#b3d9ff",
        alpha=0.8
    )
    # arrows
    nx.draw_networkx_edges(
        G, pos,
        arrowstyle="->",
        arrowsize=15,
        edge_color="#555555"
    )
    # labels
    nx.draw_networkx_labels(G, pos, font_size=9)

    # relations
    edge_labels = {(u, v): d["relation"] for u, v, d in G.edges(data=True)}
    nx.draw_networkx_edge_labels(G, pos, edge_labels, font_size=8)

    plt.title(title, fontsize=14)
    plt.axis("off")
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches="tight")
    plt.show()


def add_edge(G, source, relation, target):
    G.add_edge(source, target, relation=relation)


def construct_graph(dataset):

    G = nx.DiGraph()
    for data in dataset:
        add_edge(G, *data)
    draw_ecosystem_graph(G, title="Baseline Graph (Seed only)")