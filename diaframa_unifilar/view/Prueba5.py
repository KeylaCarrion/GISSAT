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

for tanque in wn.tank_name_list:
    if wn.get_node(tanque).tag == 'TanqueElevado':
        listaTanques.append(tanque)

tanques_por_cisterna = []
rebombeos_por_pozos = []
tanques_por_pozos = []
cisternas_por_pozos = []
cisternas_por_zona = {}
pozos_por_zona = {}
pozos_por_rebombeo = []
filas = []
filas_tanques = []
cisternas_rebombeos = []
# Recorrer cada zona
for zona in listaZonas:
    # Obtener lista de tanques conectados a la zona
    tuberias = wn.get_links_for_node(zona)

    tanques_conectados = []
    cisternas_conectados = []
    tanques_cisternas_conectados = []
    tanques_pozos_conectados = []
    cisternas_pozos_conectados = []
    rebombeos_pozos_conectados = []
    pozos_conectados = []
    zona_rebombeos_pozos = []
    rebombeos_conectados = []
    Captaciones_conectados = []
    conexion_rebombeo_captacion = []
    rebombeos_conectados_conexion = []
    cisternas_conectados_rebombeos = []
    rebombeos_conectados_tanque= []

    for tuberia in tuberias:
        nodo_Tanque = wn.get_link(tuberia).start_node_name

        if wn.get_node(nodo_Tanque).tag == 'TanqueElevado':
            tanques_conectados.append(nodo_Tanque)
            tuberias_tanques = wn.get_links_for_node(nodo_Tanque)
            for tuberias in tuberias_tanques:
                nodo_cisterna = wn.get_link(tuberias).start_node_name

                if wn.get_node(nodo_cisterna).tag == 'Cisterna':
                    tanques_cisternas_conectados.append(nodo_cisterna)
                    tuberias_Cisternas = wn.get_links_for_node(nodo_cisterna)
                    for tuberias_pozos_c in tuberias_Cisternas:
                        nodo_pozo_cisterna = wn.get_link(tuberias_pozos_c).start_node_name

                        if wn.get_node(nodo_pozo_cisterna).tag == 'Pozo':
                            cisternas_pozos_conectados.append(nodo_pozo_cisterna)

                        if wn.get_node(nodo_pozo_cisterna).tag == 'Rebombeo':
                            print("---",nodo_pozo_cisterna)
                            rebombeos_conectados_tanque.append(nodo_cisterna)

                        if wn.get_node(nodo_pozo_cisterna).tag == 'Conexion':
                            conexion_tuberias = wn.get_links_for_node(nodo_pozo_cisterna)
                            for con3 in conexion_tuberias:
                                link_con3 = wn.get_link(con3).start_node_name

                                if wn.get_node(link_con3).tag == 'Cisterna':
                                    print(link_con3)

                if wn.get_node(nodo_cisterna).tag == 'Pozo':
                    tanques_pozos_conectados.append(nodo_cisterna)

                if wn.get_node(nodo_cisterna).tag == 'Rebombeo':
                    rebombeos_conectados.append(nodo_cisterna)

                if wn.get_node(nodo_Tanque).tag == 'Conexion':
                    tuberias_conexion = wn.get_links_for_node(nodo_Tanque)
                    for conexion in tuberias_conexion:
                        con = wn.get_link(conexion).start_node_name

                        if wn.get_node(con).tag == 'TanqueElevado':
                            print(con)

                        if wn.get_node(con).tag == 'Cisterna':
                            cisternas_conectados.append(con)
                            print(con)

                        if wn.get_node(con).tag == 'Pozo':
                            print(con)

                        if wn.get_node(con).tag == 'Rebombeo':
                            rebombeos_conectados.append(con)

                            tuberias_pozos = wn.get_links_for_node(con)
                            for tu_pozos in tuberias_pozos:
                                con4 = wn.get_link(tu_pozos).start_node_name

                                if wn.get_node(con4).tag == 'Pozo':
                                    print("-----", con4)

                        if wn.get_node(con).tag == 'Captacion':
                            print(con)

        if wn.get_node(nodo_Tanque).tag == 'Cisterna':
            cisternas_conectados.append(nodo_Tanque)
            tuberias_cisternas_pozos = wn.get_links_for_node(nodo_Tanque)
            for tube in tuberias_cisternas_pozos:
                t = wn.get_link(tube).start_node_name

                if wn.get_node(t).tag == 'Pozo':
                    cisternas_pozos_conectados.append(t)

                if wn.get_node(t).tag == 'Rebombeo':
                    cisternas_conectados_rebombeos.append(t)

        if wn.get_node(nodo_Tanque).tag == 'Pozo':
            pozos_conectados.append(nodo_Tanque)

        if wn.get_node(nodo_Tanque).tag == 'Rebombeo':

            rebombeos_conectados.append(nodo_Tanque)
            tuberias_rebombeos_pozos = wn.get_links_for_node(nodo_Tanque)
            for tu in tuberias_rebombeos_pozos:
                tub = wn.get_link(tu).start_node_name
                if wn.get_node(tub).tag == 'Pozo':
                    rebombeos_pozos_conectados.append(tub)

                if wn.get_node(tub).tag == 'Conexion':
                    print("Conexion con rebobombeo", tub)
                if wn.get_node(tub).tag == 'Captacion':
                    print("Captacion", tub)

        if wn.get_node(nodo_Tanque).tag == 'Conexion':

            tuberias_conexion = wn.get_links_for_node(nodo_Tanque)
            # print(nodo_Tanque,"tuberias_conexion", tuberias_conexion)
            # print("  ")
            for conexion in tuberias_conexion:
                con = wn.get_link(conexion).start_node_name
                # print("conexiones", con)
                if wn.get_node(con).tag == 'Rebombeo':
                    rebombeos_conectados.append(con)
                    tube_con = wn.get_links_for_node(con)
                    for conexion2 in tube_con:
                        con2 = wn.get_link(conexion2).start_node_name

                        if wn.get_node(con2).tag == 'Pozo':
                            zona_rebombeos_pozos.append(con2)
                        if wn.get_node(con2).tag == 'Captacion':
                            conexion_rebombeo_captacion.append(con2)
                        if wn.get_node(con2).tag == 'Conexion':
                            tuberias_conexion2 = wn.get_links_for_node(con2)
                            for conexionw in tuberias_conexion2:
                                con9 = wn.get_link(conexionw).start_node_name

                                if wn.get_node(con9).tag == 'Rebombeo':
                                    print("Rebombeo", con9)
                                if wn.get_node(con9).tag == 'Cisterna':
                                    print("Cisterna", con9)
                                if wn.get_node(con9).tag == 'Pozo':
                                    print("Pozo", con9)
                                if wn.get_node(con9).tag == 'Captacion':
                                    print("Captacion", con9)
                                if wn.get_node(con9).tag == 'Conexion':
                                    print("conexion", con9)
                                    tuberias_conexion21 = wn.get_links_for_node(con2)
                                    for conexionx in tuberias_conexion21:
                                        con91 = wn.get_link(conexionw).start_node_name
                                        if wn.get_node(con91).tag == 'Rebombeo':
                                            print("REbombeo", con91)
                                        if wn.get_node(con9).tag == 'Cisterna':
                                            print("Cisterna", con91)
                                        if wn.get_node(con9).tag == 'Pozo':
                                            print("Pozo", con91)
                                        if wn.get_node(con9).tag == 'Captacion':
                                            print("Captacion", con91)
                                        if wn.get_node(con9).tag == 'Conexion':
                                            print("conexion", con91)

                if wn.get_node(con).tag == 'Conexion':

                    t2 = wn.get_links_for_node(con)
                    for c2 in t2:
                        c21 = wn.get_link(c2).start_node_name
                        if wn.get_node(c21).tag == 'Conexion':
                            conexion22= wn.get_links_for_node(c21)
                            for c3 in conexion22:
                                c23 = wn.get_link(c3).start_node_name
                                if wn.get_node(c23).tag == 'Rebombeo':
                                    print("Este es un rebombeo",c23)
                                if wn.get_node(c23).tag == 'Conexion':
                                    print("Esta es una conexion", c23)
                        if wn.get_node(c21).tag == 'Rebombeo':
                            print("hhh", c21)

    tanques_por_cisterna = cisternas_conectados + tanques_cisternas_conectados
    tanques_por_pozos = pozos_conectados + tanques_pozos_conectados
    cisternas_por_pozos = pozos_conectados + cisternas_pozos_conectados
    rebombeos_por_pozos = pozos_conectados + rebombeos_pozos_conectados
    pozos_por_rebombeo = pozos_conectados + zona_rebombeos_pozos + cisternas_por_pozos
    pozos_all = cisternas_por_pozos + rebombeos_por_pozos + pozos_conectados + zona_rebombeos_pozos
    cisternas_rebombeos = cisternas_conectados_rebombeos + rebombeos_conectados + rebombeos_conectados_tanque

    print("rebombeos conectados",rebombeos_conectados_tanque)


    tanques_list = []
    for tanque in tanques_conectados:
        tanques_list.append(tanque)

    list_tanques = '\n'.join(tanques_list)

    cisterna_list_pozos = []
    for poz in pozos_all:
        cisterna_list_pozos.append(poz)

    list_pozos_all = '\n'.join(cisterna_list_pozos)

    cisternas_list = []
    for cisternas in tanques_por_cisterna:
        cisternas_list.append(cisternas)

    list_cisternas = '\n'.join(cisternas_list)

    pozos_list = []
    for pozo in tanques_por_pozos:
        pozos_list.append(pozo)

    list_pozo = '\n'.join(pozos_list)

    cisternas_pozos_list = []
    for pozo_cisterna in pozos_por_rebombeo:
        cisternas_pozos_list.append(pozo_cisterna)

    rebombeos_list = []
    for rebombeos in cisternas_rebombeos:
        rebombeos_list.append(rebombeos)

    list_pozo_cisterna = '\n'.join(cisternas_pozos_list)
    list_rebombeo = '\n'.join(rebombeos_list)

    rebombeos_conexion_captacion = []
    for con_capta in conexion_rebombeo_captacion:
        print()
        rebombeos_conexion_captacion.append(con_capta)

    list_rebombeos_captaciones = '\n'.join(rebombeos_conexion_captacion)

    # Agregar cada elemento de la lista en una celda separada de la misma columna
    if len(tanques_list) == 0:
        filas.append(
            [list_rebombeos_captaciones, list_rebombeo, list_pozos_all, list_cisternas, '', zona])
    else:
        for i, tanque in enumerate(tanques_conectados):
            if i == 0:
                filas.append(
                    ['', '', '', '', tanque, zona])
            else:
                filas.append(
                    ['', '', '', '', tanque, zona])

        for j, cisterna in enumerate(tanques_por_cisterna):
            if j == 0:
                filas.append(
                    ['', '', '', cisterna, '', ''])
            else:
                filas.append(
                    ['', '', '', cisterna, '', ''])

        for k, pozo in enumerate(pozos_all):
            if k == 0:
                filas.append(
                    ['', '', pozo, '', '', ''])
            else:
                filas.append(
                    ['', '', pozo, '', '', ''])

        for h, rebombeo in enumerate(cisternas_rebombeos):
            if h == 0:
                filas.append(
                    ['', rebombeo, '', '', '', ''])
            else:
                filas.append(
                    ['', rebombeo, '', '', '', ''])

    tablaZonas = pd.DataFrame(filas, columns=['Captaciones', 'Rebombeos', 'Pozos', 'Cisternas', 'Tanque', 'Zona'])
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

import pandas as pd
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem
import sys

# Cargar los datos del archivo Excel en un DataFrame de pandas
df = pd.read_excel('BalanceV.xlsx')

# Crear la aplicación PyQt5
app = QApplication(sys.argv)

# Crear la ventana principal de la aplicación PyQt5
window = QMainWindow()

# Crear la tabla de PyQt5
table = QTableWidget()

# Establecer el número de filas y columnas de la tabla
table.setRowCount(len(df))
table.setColumnCount(len(df.columns))

# Establecer las etiquetas de encabezado de la tabla
table.setHorizontalHeaderLabels(df.columns)

# Agregar los datos del DataFrame a la tabla
for i, row in df.iterrows():
    for j, val in enumerate(row):
        item = QTableWidgetItem(str(val))
        table.setItem(i, j, item)

# Agregar la tabla a la ventana principal
window.setCentralWidget(table)
window.resize(800, 600)
# Mostrar la ventana principal
window.show()

# Ejecutar la aplicación PyQt5
sys.exit(app.exec_())
