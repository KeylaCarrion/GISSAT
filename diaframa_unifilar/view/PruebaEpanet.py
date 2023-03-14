import wntr
import matplotlib.pyplot as plt

# Create a water network model
inp_file = r'C:\Users\RI\Downloads\EPANET-dev\example-networks\N5.inp'
wn = wntr.network.WaterNetworkModel(inp_file)

print("--Conexion--")
# Obtener lista de nodos y enlaces
node_list = wn.node_name_list
link_list = wn.link_name_list

# Obtener ID del depósito
reservoir_id = [node for node in node_list if wn.get_node(node).node_type == 'Reservoir']

connected_Zone = []
connected_junctions = []

# Encontrar todas las intersecciones conectadas al depósito
connected_Zone = []
# Encontrar todas las intersecciones conectadas al depósito
for reservoir_name in reservoir_id:
    connected_junctions = []
    for link_name in wn.get_links_for_node(reservoir_name):
        link = wn.get_link(link_name)
        if link.link_type == 'Junction':
            connected_junctions.append(link.start_node_name)
            connected_junctions.append(link.end_node_name)

        if link.link_type == 'Pump':
            connected_junctions.append(link.start_node_name)
            connected_junctions.append(link.end_node_name)

            l = link.end_node_name
            for linkT in wn.get_links_for_node(l):
                linkTan = wn.get_link(linkT)

                if linkTan.link_type == 'Pump':
                    connected_Zone.append(link.start_node_name)
                    connected_Zone.append(link.end_node_name)

    #print(connected_junctions)
    print(connected_junctions)

