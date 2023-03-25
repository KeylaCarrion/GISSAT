import wntr
import pandas as pd
import openpyxl
from openpyxl import Workbook
from openpyxl.styles import Border, Side

# Cargar el archivo INP
inp_file = r'C:\Users\RI\Downloads\EPANET-dev\example-networks\N6.inp'
wn = wntr.network.WaterNetworkModel(inp_file)

# crear un nuevo libro de trabajo de Excel con openpyxl
wb = Workbook()

# seleccionar la hoja activa (por defecto)
ws = wb.active

# Obtener lista de nodos y lista de zonas
listaNodos = wn.node_name_list
listaZonas = []

# Llenar la lista de Zonas
for zona in listaNodos:
    if wn.get_node(zona).tag == 'Zona':
        listaZonas.append(zona)

# Crear tabla de resultados
tablaZonas = pd.DataFrame(columns=['Zonas', 'Tanques', 'Cisternas', 'Pozos', 'Rebombeos', 'Captaciones'])
tanques_por_zona = {}
cisternas_por_zona = {}
pozos_por_zona = {}
filas = []
filas_tanques = []
# Recorrer cada zona
for zona in listaZonas:
    # Obtener lista de tanques en la zona

    # Obtener lista de tanques conectados a la zona
    tuberias = wn.get_links_for_node(zona)
    tanques_conectados = []
    cisternas_conectados = []
    pozos_conectados = []
    rebombeos_conectados = []
    for tuberia in tuberias:
        nodo_Tanque = wn.get_link(tuberia).start_node_name
        if wn.get_node(nodo_Tanque).tag == 'TanqueElevado':
            tanques_conectados.append(nodo_Tanque)

        if wn.get_node(nodo_Tanque).tag == 'Cisterna':
            cisternas_conectados.append(nodo_Tanque)

        if wn.get_node(nodo_Tanque).tag == 'Pozo':
            pozos_conectados.append(nodo_Tanque)

        if wn.get_node(nodo_Tanque).tag == 'Rebombeo':
            rebombeos_conectados.append(nodo_Tanque)

    tanques_list = []

    for tanque in tanques_conectados:
        tanques_list.append(tanque)

    list_tanques = ','.join(tanques_list)

    cisternas_str = '\n'.join(cisternas_conectados)
    pozos_str = '\n'.join(pozos_conectados)
    rebombeos_str = '\n'.join(rebombeos_conectados)

    # Agregar cada elemento de la lista en una celda separada de la misma columna
    if len(tanques_list) == 0:
        # Si no hay tanques conectados, agregar una fila con la zona y sin tanques
        filas.append([zona, list_tanques, cisternas_str, pozos_str, rebombeos_str])
    else:
        for i, tanque in enumerate(tanques_conectados):
            if i == 0:
                # La primera fila para una zona tendrá el nombre de la zona
                filas.append([zona, tanque, '', '', '', ''])
            else:
                # Las filas siguientes para la misma zona solo tendrán el nombre del tanque
                filas.append([zona, tanque, '', '', '', ''])

    tablaZonas = pd.DataFrame(filas, columns=['Zona', 'Tanque', 'Cisternas', 'Pozos', 'Rebombeos', 'Captaciones'])

    tablaZonas.to_excel('BalanceV.xlsx', index=False)


# Definir función para aplicar estilo a celdas sin tanque
def estilo_celdas_sin_tanque(valor):
    if valor == '':

        return 'background-color: #C0C0C0'
    else:
        return ''


# Aplicar estilo a tablaZonas y guardar en un archivo Excel
tablaZonas.style.applymap(estilo_celdas_sin_tanque).to_excel('BalanceV.xlsx', index=False)

# Imprimir tablaZonas
print(tablaZonas)
print(tanques_por_zona)
