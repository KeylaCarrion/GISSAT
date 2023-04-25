from PyQt5 import QtWidgets, uic
from PyQt5.QtGui import QIcon, QPixmap, QFont
from calcular_poblacion.CalcularPoblacion import CalculaPoblacion


class Menu(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('menu_view.ui', self)
        self.show()
        self.setWindowTitle('GISSAT')

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

        self.labelCalcular.setText('Calcular Población')
        font = QFont("Arial", 9)
        font.setWeight(QFont.Bold)
        self.labelCalcular.setFont(font)
        self.btnCalcular.clicked.connect(self.calcular)


        #Boton Diagrama Unifilar
        self.btnDiagrama.setIcon(QIcon(QPixmap("./resources/icon/diagrama.png")))
        self.btnDiagrama.setIconSize(self.btnDiagrama.size())
        self.btnDiagrama.setStyleSheet("QPushButton {"
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

        self.labelDiagrama.setText('Diagrama Unifilar')
        font = QFont("Arial", 9)
        font.setWeight(QFont.Bold)
        self.labelDiagrama.setFont(font)

        self.btnBalance.setIcon(QIcon(QPixmap("./resources/icon/Balanza.png")))
        self.btnBalance.setIconSize(self.btnBalance.size())
        self.btnBalance.setStyleSheet("QPushButton {"
                                  "    border-radius: 8px;"
                                  "    background-color: red;"
                                  "    color: white;"
                                  "    padding: 8px 16px;"
                                  "    border: 2px solid #380600;"
                                  "    text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.6);"
                                  "    box-shadow: 2px 2px 4px rgba(0, 0, 0, 0.6);"
                                  "}"
                                  "QPushButton:hover {"
                                  "    background-color: #FF5D4A;"
                                  "    box-shadow: 2px 2px 8px rgba(0, 0, 0, 0.6);"
                                  "}"
                                  "QPushButton:pressed {"
                                  "    background-color: #A11201;"
                                  "    border: 2px solid #380600;"
                                  "    box-shadow: none;"
                                  "}")
        self.labelBalance.setText('Balance Volumetrico')
        font = QFont("Arial", 9)
        font.setWeight(QFont.Bold)
        self.labelBalance.setFont(font)

    def calcular(self):
        self.calcular = CalculaPoblacion()
        self.calcular.show()


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    main_window = Menu()
    main_window.show()
    app.exec_()
