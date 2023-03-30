import pandas as pd
import wntr

# Cargar el archivo INP
inp_file = r'C:\Users\RI\Downloads\EPANET-dev\example-networks\N7.inp'
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
                            rebombeos_conectados.append(nodo_cisterna)

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
                    print(tub)
                if wn.get_node(tub).tag == 'Captacion':
                    print(tub)

        if wn.get_node(nodo_Tanque).tag == 'Conexion':

            tuberias_conexion = wn.get_links_for_node(nodo_Tanque)

            for conexion in tuberias_conexion:
                con = wn.get_link(conexion).start_node_name
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
                                    print("REbombeo",con9)
                                if wn.get_node(con9).tag == 'Cisterna':
                                    print("Cisterna",con9)
                                if wn.get_node(con9).tag == 'Pozo':
                                    print("Pozo",con9)
                                if wn.get_node(con9).tag == 'Captacion':
                                    print("Captacion",con9)
                                if wn.get_node(con9).tag == 'Conexion':
                                    print("conexion",con9)
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



    tanques_por_cisterna = cisternas_conectados + tanques_cisternas_conectados
    tanques_por_pozos = pozos_conectados + tanques_pozos_conectados
    cisternas_por_pozos = pozos_conectados + cisternas_pozos_conectados
    rebombeos_por_pozos = pozos_conectados + rebombeos_pozos_conectados
    pozos_por_rebombeo = pozos_conectados + zona_rebombeos_pozos + cisternas_por_pozos

    tanques_list = []
    for tanque in tanques_conectados:
        tanques_list.append(tanque)

    list_tanques = '\n'.join(tanques_list)

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
    for rebombeos in rebombeos_conectados:
        rebombeos_list.append(rebombeos)

    list_pozo_cisterna = '\n'.join(cisternas_pozos_list)
    list_rebombeo = '\n'.join(rebombeos_list)

    rebombeos_conexion_captacion = []
    for con_capta in conexion_rebombeo_captacion:
        rebombeos_conexion_captacion.append(con_capta)

    list_rebombeos_captaciones = '\n'.join(rebombeos_conexion_captacion)

    # Agregar cada elemento de la lista en una celda separada de la misma columna
    if len(tanques_list) == 0:
        filas.append(
            [list_rebombeos_captaciones, list_rebombeo, list_pozo_cisterna, list_cisternas, list_tanques, zona])

    else:
        for i, tanque in enumerate(tanques_conectados):
            if i == 0:
                filas.append(
                    [list_rebombeos_captaciones, list_rebombeo, list_pozo_cisterna, list_cisternas, tanque, zona])
            else:
                filas.append(
                    [list_rebombeos_captaciones, list_rebombeo, list_pozo_cisterna, list_cisternas, tanque, zona])
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
