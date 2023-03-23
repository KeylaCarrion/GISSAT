import pandas as pd
import wntr
import numpy as np

# Crear modelo de red de agua
inp_file = r'C:\Users\RI\Downloads\EPANET-dev\example-networks\N6.inp'
wn = wntr.network.WaterNetworkModel(inp_file)

listaPozos = []
listaZonas = []
listaNodos = wn.node_name_list

for zona in listaNodos:
    if wn.get_node(zona).tag == 'Zona':
        listaZonas.append(zona)
    else:
        listaZonas.append(None)

# Llenar la lista de Pozos
for pozo in listaNodos:
    if wn.get_node(pozo).tag == 'Pozo':
        listaPozos.append(pozo)
    else:
        listaPozos.append(None)



def find_connections(node_name, dest_node_name, visited_nodes):
    visited_nodes.append(node_name)
    connections = []
    for link_name in wn.get_links_for_node(node_name):
        link = wn.get_link(link_name)
        if link.link_type in ['Pipe', 'Pump', 'Tank', 'Reservoir', 'Junction']:
            other_node_name = link.end_node_name if link.start_node_name == node_name else link.start_node_name
            if other_node_name is not None:
                if other_node_name not in visited_nodes:
                    if link.tag is not None and "Interconexion" in link.tag:
                        continue
                    if other_node_name == dest_node_name:
                        connections.append(f"{node_name} - {other_node_name}")
                    else:
                        connections.append(f"{node_name} - {other_node_name}")
                        if wn.get_node(other_node_name).tag == 'Zona':
                            continue
                        connections += find_connections(other_node_name, dest_node_name, visited_nodes)
    return connections


# Crear lista de conexiones
connections = []
for node_name in wn.node_name_list:
    node = wn.get_node(node_name)
    if node.node_type == 'Reservoir':
        for link_name in wn.get_links_for_node(node_name):
            link = wn.get_link(link_name)
            if link.link_type in ['Pipe', 'Pump', 'Tank']:
                other_node_name = link.end_node_name if link.start_node_name == node_name else link.start_node_name
                if other_node_name is not None and wn.get_node(other_node_name).tag == 'Zona':
                    connections.append([node_name, other_node_name])
                    connections += find_connections(other_node_name, node_name, [])
    elif node.node_type in ['Tank', 'Junction']:
        tanques_conectados = [n for n in wn.get_links_for_node(node_name) if wn.get_link(n).link_type == 'Tank']
        if len(tanques_conectados) == 1:
            tanque_name = wn.get_link(tanques_conectados[0]).start_node_name if wn.get_link(
                tanques_conectados[0]).end_node_name == node_name else wn.get_link(tanques_conectados[0]).end_node_name
            if wn.get_node(tanque_name).tag == 'Zona':
                connections.append([node_name, tanque_name])
                connections += find_connections(tanque_name, node_name, [])
        elif len(tanques_conectados) > 1:
            for i, tanque_link_name in enumerate(tanques_conectados):
                tanque_name = wn.get_link(tanque_link_name).start_node_name if wn.get_link(
                    tanque_link_name).end_node_name == node_name else wn.get_link(tanque_link_name).end_node_name
                if i == 0:
                    connections.append([node_name, tanque_name])
                    connections += find_connections(tanque_name, node_name, [])
                else:
                    connections.append([tanque_name, wn.get_link(tanques_conectados[i - 1]).start_node])
                    connections += find_connections(tanque_name, wn.get_link(tanques_conectados[i - 1]).start_node)

print(connections)
df = pd.DataFrame(
    columns=['Macrozonas', 'Captaciones', 'Rebombeos', 'Rebombeo', 'Rebombeo2', 'Pozos', 'Rebombeo-Cisterna', 'Tanque',
             'Subzonas'])
#df['Subzonas'] = listaZonas
df['Pozos'] = listaPozos




print(df)
df = df.dropna(subset=['Pozos'])

df.to_excel('Balance Volumetrico.xlsx', index=False)
