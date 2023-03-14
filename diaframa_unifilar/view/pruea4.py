import wntr

# Crear modelo de red de agua
inp_file = r'C:\Users\RI\Downloads\EPANET-dev\example-networks\N6.inp'
wn = wntr.network.WaterNetworkModel(inp_file)


# Función recursiva para encontrar todas las conexiones desde un nodo de inicio a un nodo de destino
def find_connections(node_name, dest_node_name, visited_nodes):
    visited_nodes.append(node_name)
    for link_name in wn.get_links_for_node(node_name):
        link = wn.get_link(link_name)
        if link.link_type in ['Pipe', 'Pump', 'Tank', 'Reservoir', 'Junction']:
            other_node_name = link.end_node_name if link.start_node_name == node_name else link.start_node_name
            if other_node_name is not None:
                if other_node_name not in visited_nodes:
                    if link.tag is not None and "Interconexion" in link.tag:
                        continue
                    if other_node_name == dest_node_name:
                        print(f"{wn.get_node(node_name).name} - {wn.get_node(other_node_name).name}")
                    else:
                        print(f"{wn.get_node(node_name).name} - {wn.get_node(other_node_name).name}")
                        if wn.get_node(other_node_name).tag == 'Zona':
                            continue
                        find_connections(other_node_name, dest_node_name, visited_nodes)
                        print("---------")


# Encontrar todas las conexiones desde un nodo de depósito a un nodo de zona
for node_name in wn.node_name_list:
    node = wn.get_node(node_name)
    if node.node_type == 'Reservoir':
        for link_name in wn.get_links_for_node(node_name):
            link = wn.get_link(link_name)
            if link.link_type in ['Pipe', 'Pump', 'Tank']:
                other_node_name = link.end_node_name if link.start_node_name == node_name else link.start_node_name
                if other_node_name is not None and wn.get_node(other_node_name).tag == 'Zona':
                    print(f"{wn.get_node(node_name).name} - {wn.get_node(other_node_name).name}")
                    find_connections(other_node_name, node_name, [])

    elif node.node_type in ['Tank', 'Junction']:
        tanques_conectados = [n for n in wn.get_links_for_node(node_name) if wn.get_link(n).link_type == 'Tank']
        if len(tanques_conectados) == 1:
            tanque_name = wn.get_link(tanques_conectados[0]).start_node_name if wn.get_link(
                tanques_conectados[0]).end_node_name == node_name else None



