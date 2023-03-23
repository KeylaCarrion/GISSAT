
import wntr

# Cargar el archivo INP
inp_file = r'C:\Users\RI\Downloads\EPANET-dev\example-networks\N7.inp'
wn = wntr.network.WaterNetworkModel(inp_file)

listaPozos = []
listaZonas = []
listaNodos = wn.node_name_list

## Llenar la lista de Zonas
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

print(listaZonas)


