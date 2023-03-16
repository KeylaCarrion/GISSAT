import wntr

# Crear modelo de red de agua
inp_file = r'C:\Users\RI\Downloads\EPANET-dev\example-networks\N6.inp'
wn = wntr.network.WaterNetworkModel(inp_file)

print("  ")
print("Pozos")
print("  ")
pozosLista = {}
node_name = wn.node_name_list
for lik_name in node_name:

    if wn.get_node(lik_name).tag == "Pozo":
        print(lik_name)

print("  ")
print("Capataciones o fuentes")
node_name = wn.node_name_list
for lik_name in node_name:

    if wn.get_node(lik_name).tag == "Captacion" or wn.get_node(lik_name).tag == "Fuente":
        print(lik_name)

print("  ")
print("SubZonas")
node_name = wn.node_name_list
for lik_name in node_name:

    if wn.get_node(lik_name).tag == "Zona":
        print(lik_name)

print("  ")
print("pozos- links")
node_name = wn.node_name_list
for lik_name in node_name:
    node = wn.get_node(lik_name)
    if wn.get_node(lik_name).tag == "Pozo":
        for link_Pozo in wn.get_links_for_node(lik_name):
            link = wn.get_link(link_Pozo)
            if link.link_type in ['Pipe', 'Pump', 'Tank']:
                start_node = link.start_node_name
                end_node = link.end_node_name
                print(start_node, " - ", end_node)
