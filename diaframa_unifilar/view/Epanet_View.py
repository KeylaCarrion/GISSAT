import wntr
import matplotlib.pyplot as plt
import pandas as pd
import networkx as nx

# Create a water network model
inp_file = r'C:\Users\RI\Downloads\EPANET-dev\example-networks\N6.inp'
wn = wntr.network.WaterNetworkModel(inp_file)

print("--Conexion--")
# Obtener lista de nodos y enlaces
node_list = wn.node_name_list
link_list = wn.link_name_list

# Obtener ID del depósito
reservoir_id = [node for node in node_list if wn.get_node(node).node_type == 'Reservoir']

connected_Zone = []
# Encontrar todas las intersecciones conectadas al depósito
for reservoir_name in reservoir_id:
    connected_junctions = []
    for link_name in wn.get_links_for_node(reservoir_name):
        link = wn.get_link(link_name)
        if link.link_type == 'Pipe':
            connected_junctions.append(link.start_node_name)
            connected_junctions.append(link.end_node_name)

        if link.link_type == 'Pump':
            connected_junctions.append(link.start_node_name)
            connected_junctions.append(link.end_node_name)

    conection = []
    for conexion2 in connected_junctions:
        for link_name in wn.get_links_for_node(conexion2):
            link = wn.get_link(link_name)
            conection.append(link.start_node_name)
            conection.append(link.end_node_name)
    print(set(conection))

# Encontrar todos los tanques conectados a las intersecciones



r = wn.junction_name_list


for reservoir_name in reservoir_id:
    for reservoir in wn.get_links_for_node(reservoir_name):
        for link_name in wn.get_links_for_node(reservoir_name):
            link = wn.get_link(link_name)
        #print(f"{reservoir} connect {link.link_type}")

# Obtener ID del depósito
tank_id = [node for node in node_list if wn.get_node(node).node_type == 'Tank']

for tank_name in tank_id:
    for tank in wn.get_links_for_node(tank_name):
        for link_name in  wn.get_links_for_node(tank_name):
            link = wn.get_link(link_name)
        #print(f"{tank} connect {link.link_type}")





# Simulate hydraulics
sim = wntr.sim.EpanetSimulator(wn)
results = sim.run_sim()

# Plot results on the network

wntr.graphics.plot_network(wn)
plt.show()
