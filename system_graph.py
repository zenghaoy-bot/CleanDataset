from pyvis.network import Network

def construct_graph(entity_relations):

    net = Network(height="800px", width="100%", bgcolor="#ffffff", font_color="black")
    net.barnes_hut(gravity=-8000, central_gravity=0.3, spring_length=100)

    for head, rel, tail in entity_relations:
        net.add_node(head, label=head)
        net.add_node(tail, label=tail)
        net.add_edge(head, tail, title=rel) 

    net.write_html("graph.html")