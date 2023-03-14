from PyQt5.QtWidgets import QMainWindow, QToolBar, QAction, QFileDialog, QMessageBox, QVBoxLayout, QHBoxLayout, QLabel, \
    QTableWidgetItem, QPushButton, QTableView, QWidget
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QIcon, QStandardItemModel, QStandardItem
from diaframa_unifilar.controller.ControllerTanques import controllerTanques
from diaframa_unifilar.controller.ControllerPozos import controllerPozos
from diaframa_unifilar.model.ModelPozos import ModelPozos
from diaframa_unifilar.model.ModelFuentes import ModelTanque

modelo_pozos = ModelPozos(host="localhost",
                          user="root",
                          password="root",
                          database="prueba")

modelo_tanques = ModelTanque(host="localhost",
                             user="root",
                             password="root",
                             database="prueba")
controller_pozo = controllerPozos(modelo_pozos)
controller_tanques = controllerTanques(modelo_tanques)
from PyQt5 import QtWidgets, uic, QtGui, QtCore
import pandas as pd


class diagramaUnifilar(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Diagrama Unifilar")
        uic.loadUi('diagrama_unifilar.ui', self)

        toolbar = QToolBar("Diagrama Unifilar")
        toolbar.setIconSize(QSize(42, 42))
        self.addToolBar(toolbar)

        # Botones
        upload_files = QAction(QIcon("../../resources/icon/folder--plus.png"), "Agregar Archivos", self)
        upload_files.setStatusTip("Agregar Archivos")
        upload_files.triggered.connect(self.open_file)
        upload_files.setCheckable(True)
        toolbar.addAction(upload_files)

        # Botones
        relation = QAction(QIcon("../../resources/icon/application-form.png"), "Funcionamiento", self)
        relation.setStatusTip("Funcionamiento")
        relation.setCheckable(True)
        toolbar.addAction(relation)

        # Botones
        balance = QAction(QIcon("../../resources/icon/balance--arrow.png"), "Balance Volumetrico", self)
        balance.setStatusTip("Balance Volumetrico")
        balance.setCheckable(True)
        toolbar.addAction(balance)

    def open_file(self):
        self.second = tablaPozos()
        self.second.show()


class tablaPozos(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Inventario')
        self.setGeometry(200, 200, 600, 400)

        # Crear los widgets de las pestañas
        self.tab_widget = QtWidgets.QTabWidget(self)
        self.tab1 = QtWidgets.QWidget()
        self.tab2 = QtWidgets.QWidget()
        self.tab3 = QtWidgets.QWidget()
        self.tab4 = QtWidgets.QWidget()

        # Agregar las pestañas al tab widget con los nombres
        self.tab_widget.addTab(self.tab1, "Pozos")
        self.tab_widget.addTab(self.tab2, "Tanques")
        self.tab_widget.addTab(self.tab3, "Rebombeos")
        self.tab_widget.addTab(self.tab4, "Cisternas")
        self.setCentralWidget(self.tab_widget)

        # POZOS
        # Agregar dos botones en la pestaña "Tanques"
        # Crear botones
        self.btn_agregar = QtWidgets.QPushButton('Agrega Excel')
        self.btn_agregar.clicked.connect(self.upload_files)
        btn_registrar = QtWidgets.QPushButton('Registrar')

        self.modeloPozos = modelo_pozos
        self.controller = controllerPozos(self.modeloPozos)

        data = self.controller.obtnerPozos()

        self.model = QStandardItemModel(len(data), 4)

        self.model.setHorizontalHeaderLabels(['Pozos', 'Coordenada X', 'Coordenada Y','Colonia'])

        # Agregar los datos obtenidos a la tabla
        for row, record in enumerate(data):
            for column, item in enumerate(record):
                self.model.setItem(row, column, QStandardItem(str(item)))

        self.view = QTableView()
        self.view.setModel(self.model)
        self.view.setColumnWidth(0, 200)
        self.view.setColumnWidth(1, 150)
        self.view.setColumnWidth(2, 150)
        self.view.setColumnWidth(3, 150)

        # Agregar botones de editar y eliminar
        self.model.insertColumn(self.model.columnCount())
        self.model.setHeaderData(self.model.columnCount() - 1, Qt.Horizontal, 'Acciones')
        for row in range(self.model.rowCount()):
            widget_container = QWidget()
            edit_button = QPushButton('Editar', widget_container)
            edit_button.clicked.connect(lambda _, r=row: self.edit_record(r))
            delete_button = QPushButton('Eliminar', widget_container)
            delete_button.clicked.connect(lambda _, r=row: self.delete_record(r))

            # Crear un layout horizontal para los botones
            layout = QHBoxLayout()
            layout.addWidget(edit_button)
            layout.addWidget(delete_button)
            layout.setContentsMargins(0, 0, 0, 0)

            # Establecer el layout como el layout del contenedor
            widget_container.setLayout(layout)

            # Agregar el contenedor a la celda correspondiente de la tabla
            index = self.model.index(row, self.model.columnCount() - 1)
            self.view.setIndexWidget(index, widget_container)
        # Establecer el nuevo modelo en la vista de la tabla

        # Establecer el nuevo modelo en la vista de la tabla
        self.view.setModel(self.model)
        # Agregar botones y tabla a la pestaña
        layout_tab1 = QtWidgets.QVBoxLayout(self.tab1)

        # Tabla de Fuentes
        # Agregar dos botones en la pestaña "Tanques"
        # Crear botones
        self.btn_agregar2 = QtWidgets.QPushButton('Agrega Excel')
        self.btn_agregar2.clicked.connect(self.upload_files2)
        btn_registrar2 = QtWidgets.QPushButton('Registrar')

        self.modeloT = modelo_tanques
        self.controller = controllerTanques(self.modeloT)

        data = self.controller.obtenerTanques()

        self.modelP = QStandardItemModel(len(data), 4)

        self.modelP.setHorizontalHeaderLabels(['Nombre', 'X', 'Y', 'Direccion', 'Colonia'])

        # Agregar los datos obtenidos a la tabla
        for row, record in enumerate(data):
            for column, item in enumerate(record):
                self.modelP.setItem(row, column, QStandardItem(str(item)))

        self.view2 = QTableView()
        self.view2.setModel(self.modelP)
        self.view2.setColumnWidth(0, 200)
        self.view2.setColumnWidth(1, 150)
        self.view2.setColumnWidth(2, 150)
        self.view2.setColumnWidth(3, 150)

        # Agregar botones de editar y eliminar
        self.modelP.insertColumn(self.modelP.columnCount())
        self.modelP.setHeaderData(self.modelP.columnCount() - 1, Qt.Horizontal, 'Acciones')
        for row in range(self.modelP.rowCount()):
            widget_container = QWidget()
            edit_button = QPushButton('Editar', widget_container)
            edit_button.clicked.connect(lambda _, r=row: self.edit_record(r))
            delete_button = QPushButton('Eliminar', widget_container)
            delete_button.clicked.connect(lambda _, r=row: self.delete_record(r))

            # Crear un layout horizontal para los botones
            layout = QHBoxLayout()
            layout.addWidget(edit_button)
            layout.addWidget(delete_button)
            layout.setContentsMargins(0, 0, 0, 0)

            # Establecer el layout como el layout del contenedor
            widget_container.setLayout(layout)

            # Agregar el contenedor a la celda correspondiente de la tabla
            index = self.modelP.index(row, self.modelP.columnCount() - 1)
            self.view2.setIndexWidget(index, widget_container)
        # Establecer el nuevo modelo en la vista de la tabla

        # Establecer el nuevo modelo en la vista de la tabla
        self.view2.setModel(self.modelP)
        # Agregar botones y tabla a la pestaña
        layout_tab2 = QtWidgets.QVBoxLayout(self.tab2)

        layout_botones = QtWidgets.QHBoxLayout()
        layout_botones.addStretch(1)
        layout_botones.addWidget(self.btn_agregar)
        layout_botones.addWidget(btn_registrar)

        layout_botones2 = QtWidgets.QHBoxLayout()
        layout_botones2.addStretch(1)
        layout_botones2.addWidget(self.btn_agregar2)
        layout_botones2.addWidget(btn_registrar2)

        layout_tab1.addLayout(layout_botones)
        layout_tab1.addWidget(self.view)

        layout_tab2.addLayout(layout_botones2)
        layout_tab2.addWidget(self.view2)

    def upload_files(self):
        # Abrir cuadro de dialogo para seleccionar un archivo
        file = QFileDialog()
        file.setNameFilter("Archivos de excel(*.xlsx)")
        file_path, _ = file.getOpenFileName(self, "Seleccionar archivo")
        self.insert_data(file_path)

    def upload_files2(self):
        # Abrir cuadro de dialogo para seleccionar un archivo
        file = QFileDialog()
        file.setNameFilter("Archivos de excel(*.xlsx)")
        file_path, _ = file.getOpenFileName(self, "Seleccionar archivo")
        self.insert_Tanque(file_path)

    def insert_data(self, file_path):
        controller_pozo.insertPozos_excel(file_path)

    def insert_Tanque(self, file_path):
        controller_tanques.insertTanques_excel(file_path)


class MessageWidget(QtWidgets.QFrame):
    def __init__(self):
        super().__init__()
        self.setWindowModality(Qt.ApplicationModal)
        self.setWindowTitle("    ")
        self.setWindowIcon(QtGui.QIcon("../../resources/icon/message.png"))
        self.setWindowFlag(QtCore.Qt.WindowMinMaxButtonsHint, False)

        self.message_label = QtWidgets.QLabel("La carga de Archivos ha sido Exitoso", self)
        self.message_label.setAlignment(QtCore.Qt.AlignCenter)
        self.setStyleSheet("background-color: white;"
                           "QLabel{min-width: 300px;}")
        self.message_label.setFont(QtGui.QFont("Arial", 18))
        self.setFixedSize(450, 200)

        icon_label = QtWidgets.QLabel()
        icon_pixmap = QtGui.QPixmap("../../resources/icon/confirmation.png")
        icon_pixmap = icon_pixmap.scaledToHeight(50, QtCore.Qt.SmoothTransformation)
        icon_label.setPixmap(icon_pixmap)
        icon_label.setAlignment(QtCore.Qt.AlignCenter)

        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(icon_label)
        layout.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(self.message_label)


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    main_window = diagramaUnifilar()
    main_window.show()
    app.exec_()
