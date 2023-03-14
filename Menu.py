from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QHBoxLayout, QSpacerItem, QSizePolicy
from PyQt5.QtGui import QIcon, QPixmap, QFont
from PyQt5.QtCore import Qt, QSize
from calcular_poblacion.CalcularPoblacion import CalculaPoblacion

class Menu(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()


    def initUI(self):

        # Configurar el layout vertical
        layout = QHBoxLayout()
        layout.setContentsMargins(30, 30, 100, 130)
        # Establecer la separación entre los elementos del layout

        # Crear el botón calcular Poblacion
        self.btnCalcular = QPushButton()
        self.btnCalcular.setIcon(QIcon(QPixmap("./resources/icon/calculadora.png")))
        self.btnCalcular.setIconSize(self.btnCalcular.size())
        self.btnCalcular.setStyleSheet("QPushButton {"
                                  "    border-radius: 8px;"
                                  "    background-color: yellow;"
                                  "    color: black;"
                                  "    padding: 8px 16px;"
                                  "    border: 2px solid #AEAE00;"
                                  "    text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.6);"
                                  "    box-shadow: 2px 2px 4px rgba(0, 0, 0, 0.6);"
                                  "}"
                                  "QPushButton:hover {"
                                  "    background-color: #ECEC06;"
                                  "    box-shadow: 2px 2px 8px rgba(0, 0, 0, 0.6);"
                                  "}"
                                  "QPushButton:pressed {"
                                  "    background-color: #FFFA00;"
                                  "    border: 2px solid #F2ED02;"
                                  "    box-shadow: none;"
                                  "}")
        self.btnCalcular.setFixedSize(95, 110)
        self.btnCalcular.clicked.connect(self.calcular)

        # Configurar la etiqueta
        labelCaulcular = QLabel('Calcular Población')
        font = QFont("Arial", 9)
        font.setWeight(QFont.Bold)
        labelCaulcular.setFont(font)

        layoutVertical = QVBoxLayout()
        layout.addItem(layoutVertical)

        # Agregar espaciadores vertical alrededor del botón y la etiqueta
        layoutVertical.addItem(QSpacerItem(10, 10, QSizePolicy.Minimum, QSizePolicy.Expanding))
        layoutVertical.addWidget(self.btnCalcular)
        layoutVertical.addItem(QSpacerItem(10, 10, QSizePolicy.Minimum, QSizePolicy.Expanding))
        layoutVertical.addWidget(labelCaulcular)
        layoutVertical.addItem(QSpacerItem(10, 10, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Agregar un espaciador vertical para separar los botones
        layout.addItem(QSpacerItem(10, 10, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Crear el botón 2
        self.button2 = QPushButton()
        self.button2.setIcon(QIcon(QPixmap("./resources/icon/bug.png")))
        self.button2.setIconSize(self.button2.size())
        self.button2.setStyleSheet("QPushButton {"
                                  "    border-radius: 8px;"
                                  "    background-color: blue;"
                                  "    color: white;"
                                  "    padding: 8px 16px;"
                                  "    border: 2px solid #00008B;"
                                  "    text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.6);"
                                  "    box-shadow: 2px 2px 4px rgba(0, 0, 0, 0.6);"
                                  "}"
                                  "QPushButton:hover {"
                                  "    background-color: #0000CD;"
                                  "    box-shadow: 2px 2px 8px rgba(0, 0, 0, 0.6);"
                                  "}"
                                  "QPushButton:pressed {"
                                  "    background-color: #000080;"
                                  "    border: 2px solid #1E90FF;"
                                  "    box-shadow: none;"
                                  "}")
        self.button2.setFixedSize(95, 110)
        self.button2.clicked.connect(self.otro)
        self.button2.setContentsMargins(30, 30, 100, 130)
        layout.addWidget(self.button2)

        # Agregar el layout vertical al widget principal
        self.setLayout(layout)
        self.setWindowTitle('GISSAT')
        self.setFixedSize(400, 300)
        self.show()

    def calcular(self):
        self.calcular = CalculaPoblacion()
        self.calcular.show()

    def otro(self):
        print("otro")

if __name__ == '__main__':
    app = QApplication([])
    window = Menu()
    app.exec_()

