import wntr

# Crear modelo de red de agua
inp_file = r'C:\Users\RI\Downloads\EPANET-dev\example-networks\N6.inp'
wn = wntr.network.WaterNetworkModel(inp_file)


# Función recursiva para encontrar todas las conexiones desde un nodo de inicio a un nodo de destino
def find_connections_zone_to_well(node_name, dest_node_name, visited_nodes):
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
                        return visited_nodes + [other_node_name]
                    else:
                        result = find_connections_zone_to_well(other_node_name, dest_node_name, visited_nodes)
                        if result is not None:
                            return result
                        elif wn.get_node(other_node_name).tag == 'Cisterna':
                            continue
                        else:
                            visited_nodes.pop()
    return None


well_node = [node for node_name, node in wn.nodes() if node.tag == 'Pozo'][0]

# Encontrar todas las conexiones desde un nodo de zona a un nodo de pozo pasando por tanques y cisternas
for node_name in wn.node_name_list:
    node = wn.get_node(node_name)
    if node.node_type == 'Junction' and node.tag == 'Zona':
        for link_name in wn.get_links_for_node(node_name):
            link = wn.get_link(link_name)
            if link.link_type in ['Pipe', 'Pump']:
                other_node_name = link.end_node_name if link.start_node_name == node_name else link.start_node_name
                if other_node_name is not None:
                    result = find_connections_zone_to_well(other_node_name, well_node.name, [])
                    if result is not None:
                        print(' - '.join(result))


