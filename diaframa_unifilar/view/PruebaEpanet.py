import pandas as pd
import wntr

# Cargar el archivo INP
inp_file = r'C:\Users\RI\Downloads\EPANET-dev\example-networks\N6.inp'
wn = wntr.network.WaterNetworkModel(inp_file)

# Obtener lista de nodos y lista de zonas
listaNodos = wn.node_name_list
listaZonas = []
listaTanques = []

# Llenar la lista de Zonas
for zona in listaNodos:
    if wn.get_node(zona).tag == 'Zona':
        listaZonas.append(zona)


tanques_por_cisterna = []
rebombeos_por_pozos = []
tanques_por_pozos = []
cisternas_por_pozos = []
cisternas_por_zona = {}
pozos_por_zona = {}
pozos_por_rebombeo=[]
filas = []
filas_tanques = []

# Función recursiva para obtener las conexiones de un nodo
def obtener_conexiones(nodo):
    conexiones = []
    tuberias = wn.get_links_for_node(nodo)
    for tuberia in tuberias:
        nodo_conectado = wn.get_link(tuberia).end_node_name
        tag_nodo_conectado = wn.get_node(nodo_conectado).tag
        if tag_nodo_conectado == 'TanqueElevado':
            if nodo_conectado not in conexiones:
                conexiones.append(nodo_conectado)
                conexiones += obtener_conexiones(nodo_conectado)
        elif tag_nodo_conectado == 'Cisterna':
            if nodo_conectado not in conexiones:
                conexiones.append(nodo_conectado)
                conexiones += obtener_conexiones(nodo_conectado)
        elif tag_nodo_conectado == 'Pozo':
            if nodo_conectado not in conexiones:
                conexiones.append(nodo_conectado)
                conexiones += obtener_conexiones(nodo_conectado)
        elif tag_nodo_conectado == 'Rebombeo':
            if nodo_conectado not in conexiones:
                conexiones.append(nodo_conectado)
                conexiones += obtener_conexiones(nodo_conectado)
        elif tag_nodo_conectado == 'Conexion':
            if nodo_conectado not in conexiones:
                conexiones.append(nodo_conectado)
                conexiones += obtener_conexiones(nodo_conectado)

    return conexiones


# Recorrer cada zona
for zona in listaZonas:

    tanques_conectados = []
    cisternas_conectados = []
    pozos_conectados = []
    rebombeos_conectados = []
    conexiones_conectadas = []

    # Obtener lista de nodos de la zona
    listaNodos = wn.node_name_list
    nodos_zona = []
    # Llenar la lista de Zonas
    for zona in listaNodos:
        if wn.get_node(zona).tag == 'Zona':
            nodos_zona.append(zona)

    # Recorrer cada nodo de la zona
    for nodo in nodos_zona:
        tuberias = wn.get_links_for_node(nodo)
        for tuberia in tuberias:
            t = wn.get_link(tuberia).start_node_name
            print(t)
            tag_nodo = wn.get_node(t).tag

            if tag_nodo == 'TanqueElevado':
                tanques_conectados.append(nodo)

                conexiones_conectadas += obtener_conexiones(nodo)

            elif tag_nodo == 'Cisterna':
                cisternas_conectados.append(nodo)
                conexiones_conectadas += obtener_conexiones(nodo)

            elif tag_nodo == 'Pozo':
                cisternas_conectados.append(nodo)
                conexiones_conectadas += obtener_conexiones(nodo)

            elif tag_nodo == 'Rebombeo':
                cisternas_conectados.append(nodo)
                conexiones_conectadas += obtener_conexiones(nodo)