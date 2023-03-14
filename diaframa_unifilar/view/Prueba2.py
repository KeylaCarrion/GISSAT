import wntr


# Create a water network model
inp_file = r'C:\Users\RI\Downloads\EPANET-dev\example-networks\N6.inp'
wn = wntr.network.WaterNetworkModel(inp_file)

print("--Conexion--")
# Obtener lista de nodos y enlaces
node_list = wn.node_name_list
link_list = wn.link_name_list

# Obtener ID del depósito
reservoir_id = [node for node in node_list if wn.get_node(node).node_type == 'Reservoir']

connected_junctions = []

print("Pozo a conexiones")
# Encontrar todas las intersecciones conectadas al depósito
for reservoir_name in reservoir_id:
    node = wn.get_node(reservoir_name)
    tag = node.tag
    for link_name in wn.get_links_for_node(reservoir_name):
        link = wn.get_link(link_name)
        if link.link_type == 'Pump' and node.tag != 'Interconexion':

                connected_junctions.append(link.start_node_name)
                connection_Start = link.start_node_name
                connected_junctions.append(link.end_node_name)
                connection_end = link.end_node_name
                print(f"{connection_Start} con {connection_end}")


                for link_name in wn.get_links_for_node(connection_end):
                    link = wn.get_link(link_name)
                    print(f"-{link.start_node_name} con {link.end_node_name}")

        if link.link_type == 'Pipe' and node.tag != 'Interconexion':

                connected_junctions.append(link.start_node_name)
                connection_Start = link.start_node_name
                connected_junctions.append(link.end_node_name)
                connection_end = link.end_node_name
                print(f"-{connection_Start} con {connection_end}")
                print("------",connection_end)

                for link_name in wn.get_links_for_node(connection_end):
                    link = wn.get_link(link_name)
                    print(f"-{link.start_node_name} con {link.end_node_name}")








print("Funciones")


