import wntr
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QHBoxLayout
from PyQt5 import QtWidgets, uic
from qgis._gui import QgsMapCanvas
from PyQt5.QtGui import QColor, QFont, QIcon
from qgis.PyQt.QtWidgets import QFileDialog
import pandas
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem
import sys


class diagramaUnifilar(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Diagrama Unifilar")
        uic.loadUi('diagrama_unifilar.ui', self)

        self.canvas = QgsMapCanvas()
        self.canvas.enableAntiAliasing(True)

        # Agregar el Map canvas a la ventana principal, dentro del marco
        self.layout = QVBoxLayout(self.frame)
        self.layout.addWidget(self.canvas)

        self.btn_project_load.setIcon(QIcon("../resources/icon/i_load.png"))
        self.btn_project_load.setText("Abrir Archivo")
        self.btn_project_load.clicked.connect(self.project_load_clicked)
        self.btn_project_new.setIcon(QIcon("../resources/icon/i_load.png"))
        self.btn_project_new.setText("Conexiones")

    def project_load_clicked(self):
        self.btn_project_load.setChecked(False)

        inp_file_path, _ = QFileDialog.getOpenFileName(self, 'Open File', '.', 'All Files (*)')

        if inp_file_path is not None and inp_file_path:
            self.inp_file_path = inp_file_path

            self.txt_prj_file.setText(self.inp_file_path)
            print(self.inp_file_path)

            # Cargar el archivo INP
            inp_file = self.inp_file_path
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
                conexion_rebombeo_captacion = []

                # Rebombeo 1,2,3
                rebombeos_conectados_tanque1 = []
                rebombeos_conectados_tanque2 = []
                rebombeos_conectados_tanque3 = []

                # Rebombeo 1,2,3
                cisternas_conectados_rebombeos1 = []
                cisternas_conectados_rebombeos2 = []
                cisternas_conectados_rebombeos3 = []

                # Rebombeo 1,2,3
                rebombeos_conectados_rebombeos1 = []
                rebombeos_conectados_rebombeos2 = []
                rebombeos_conectados_rebombeos3 = []

                cisternas_pozos_conectados1 = []
                cisternas_pozos_conectados2 = []
                cisternas_pozos_conectados3 = []
                rebombeos_pozos_conectados1 = []
                rebombeos_pozos_conectados2 = []
                rebombeos_pozos_conectados3 = []

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

                                    if wn.get_node(nodo_pozo_cisterna).tag == 'Rebombeo1':
                                        rebombeos_conectados_tanque1.append(nodo_pozo_cisterna)

                                    if wn.get_node(nodo_pozo_cisterna).tag == 'Rebombeo2':
                                        rebombeos_conectados_tanque2.append(nodo_pozo_cisterna)

                                    if wn.get_node(nodo_pozo_cisterna).tag == 'Rebombeo3':
                                        print(nodo_pozo_cisterna)
                                        rebombeos_conectados_tanque3.append(nodo_pozo_cisterna)

                            if wn.get_node(nodo_cisterna).tag == 'Pozo':
                                tanques_pozos_conectados.append(nodo_cisterna)

                            if wn.get_node(nodo_cisterna).tag == 'Rebombeo1':
                                rebombeos_conectados.append(nodo_cisterna)
                                # Puede que no se enceuntre una conexion de parte de Pozo a un primer rebeombeo

                            if wn.get_node(nodo_cisterna).tag == 'Rebombeo2':
                                print("nodo_cisterna")
                            if wn.get_node(nodo_cisterna).tag == 'Rebombeo3':
                                print("nodo_cisterna")

                    if wn.get_node(nodo_Tanque).tag == 'Cisterna':
                        cisternas_conectados.append(nodo_Tanque)
                        tuberias_cisternas_pozos = wn.get_links_for_node(nodo_Tanque)
                        for tube in tuberias_cisternas_pozos:
                            t = wn.get_link(tube).start_node_name

                            if wn.get_node(t).tag == 'Pozo':
                                cisternas_pozos_conectados.append(t)
                                cpc = wn.get_links_for_node(t)

                            if wn.get_node(t).tag == 'Rebombeo1':
                                cisternas_conectados_rebombeos1.append(t)

                            if wn.get_node(t).tag == 'Rebombeo2':

                                cisternas_conectados_rebombeos2.append(t)
                                tuberias_pozos_rebombeos2 = wn.get_links_for_node(t)
                                for tpr2 in tuberias_pozos_rebombeos2:
                                    trp2 = wn.get_link(tpr2).start_node_name
                                    if wn.get_node(trp2).tag == 'Rebombeo1':
                                        cisternas_conectados_rebombeos1.append(trp2)
                                    if wn.get_node(trp2).tag == 'Rebombeo2':
                                        cisternas_conectados_rebombeos2.append(trp2)
                                    if wn.get_node(trp2).tag == 'Rebombeo3':
                                        cisternas_conectados_rebombeos3.append(trp2)
                                    print(cisternas_conectados_rebombeos3)

                            if wn.get_node(t).tag == 'Rebombeo3':
                                # Puede que no haya conexion de cisterna rebombeo pero si de rebombeo a rebombeo.
                                cisternas_conectados_rebombeos3.append(t)

                    if wn.get_node(nodo_Tanque).tag == 'Pozo':
                        pozos_conectados.append(nodo_Tanque)
                        tuberias_pozos_rebombeos = wn.get_links_for_node(nodo_Tanque)

                        for tpr in tuberias_pozos_rebombeos:

                            trp = wn.get_link(tpr).start_node_name

                            if wn.get_node(trp).tag == 'Rebombeo1':
                                rebombeos_pozos_conectados.append(trp)

                    if wn.get_node(nodo_Tanque).tag == 'Rebombeo1':

                        rebombeos_conectados.append(nodo_Tanque)
                        tuberias_rebombeos_pozos = wn.get_links_for_node(nodo_Tanque)

                        for tu in tuberias_rebombeos_pozos:
                            tub = wn.get_link(tu).start_node_name
                            if wn.get_node(tub).tag == 'Pozo':
                                rebombeos_pozos_conectados.append(tub)

                tanques_por_cisterna = cisternas_conectados + tanques_cisternas_conectados
                tanques_por_pozos = pozos_conectados + tanques_pozos_conectados
                cisternas_por_pozos = pozos_conectados + cisternas_pozos_conectados
                rebombeos_por_pozos = pozos_conectados + rebombeos_pozos_conectados
                pozos_por_rebombeo = pozos_conectados + zona_rebombeos_pozos + cisternas_por_pozos
                pozos_all = cisternas_por_pozos + rebombeos_por_pozos + pozos_conectados + zona_rebombeos_pozos

                cisternas_rebombeos1 = cisternas_conectados_rebombeos1 + rebombeos_conectados + rebombeos_conectados_tanque1
                cisternas_rebombeos2 = cisternas_conectados_rebombeos2 + rebombeos_conectados_tanque2
                cisternas_rebombeos3 = cisternas_conectados_rebombeos3 + rebombeos_conectados_tanque3

                print(rebombeos_conectados)
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

                rebombeos_list1 = []
                for rebombeos1 in cisternas_rebombeos1:
                    # print(cisternas_rebombeos)
                    rebombeos_list1.append(rebombeos1)

                rebombeos_list2 = []
                for rebombeos2 in cisternas_rebombeos2:
                    # print(cisternas_rebombeos)
                    rebombeos_list2.append(rebombeos2)

                rebombeos_list3 = []
                for rebombeos3 in cisternas_rebombeos3:
                    # print(cisternas_rebombeos)
                    rebombeos_list3.append(rebombeos3)

                list_pozo_cisterna = '\n'.join(cisternas_pozos_list)
                list_rebombeo1 = '\n'.join(rebombeos_list1)
                list_rebombeo2 = '\n'.join(rebombeos_list2)
                list_rebombeo3 = '\n'.join(rebombeos_list3)

                rebombeos_conexion_captacion = []
                for con_capta in conexion_rebombeo_captacion:
                    rebombeos_conexion_captacion.append(con_capta)

                list_rebombeos_captaciones = '\n'.join(rebombeos_conexion_captacion)

                # Agregar cada elemento de la lista en una celda separada de la misma columna
                if len(tanques_list) == 0:
                    filas.append(
                        [list_rebombeos_captaciones, list_rebombeo3, list_rebombeo2, list_rebombeo1, list_pozos_all,
                         list_cisternas,
                         '', zona])
                else:
                    for i, tanque in enumerate(tanques_conectados):
                        if i == 0:
                            filas.append(
                                ['', '', '', '', '', '', '', ''])
                        else:
                            filas.append(
                                ['', '', '', '', '', '', '', ''])

                    for j, cisterna in enumerate(tanques_por_cisterna):
                        if j == 0:
                            filas.append(
                                ['', '', '', '', '', '', '', ''])
                        else:
                            filas.append(
                                ['', '', '', '', '', '', '', ''])

                    for k, pozo in enumerate(pozos_all):
                        if k == 0:
                            filas.append(
                                ['', '', '', '', '', '', '', ''])
                        else:
                            filas.append(
                                ['', '', '', '', '', '', '', ''])

                    for m, rebombeo1 in enumerate(cisternas_rebombeos1):
                        if m == 0:
                            filas.append(
                                ['', '', '', rebombeo1, '', '', '', ''])
                        else:
                            filas.append(
                                ['', '', '', rebombeo1, '', '', '', ''])

                    for h, rebombeo2 in enumerate(cisternas_rebombeos2):
                        if h == 0:
                            filas.append(
                                ['', '', rebombeo2, '', pozo, cisterna, tanque, zona])
                        else:
                            filas.append(
                                ['', '', rebombeo2, '', pozo, cisterna, tanque, zona])

                    for f, rebombeo3 in enumerate(cisternas_rebombeos3):
                        if f == 0:
                            filas.append(
                                ['', rebombeo3, '', '', '', '', '', ''])
                        else:
                            filas.append(
                                ['', rebombeo3, '', '', '', '', '', ''])

                tablaZonas = pandas.DataFrame(filas,
                                              columns=['Captaciones', 'Rebombeos 3 ', 'Rebombeos 2', 'Rebombeos 1',
                                                       'Pozos',
                                                       'Cisternas',
                                                       'Tanque', 'Zona'])
                tablaZonas.to_excel('BalanceV.xlsx', index=False)

            # Definir función para aplicar estilo a celdas sin tanque
            def estilo_celdas_sin_tanque(valor):
                if valor == '':
                    return 'background-color: #C0C0C0'
                else:
                    return ''

            tablaZonas = tablaZonas.reset_index(drop=True)
            # Aplicar estilo a tablaZonas y guardar en un archivo Excel
            tablaZonas.style.applymap(estilo_celdas_sin_tanque).to_excel('BalanceV.xlsx', index=False)

            # Imprimir tablaZonas
            print(tablaZonas)

            # Cargar los datos del archivo Excel en un DataFrame de pandas
            df = pandas.read_excel('BalanceV.xlsx')
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


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    main_window = diagramaUnifilar()
    main_window.show()
    app.exec_()
