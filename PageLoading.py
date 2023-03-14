import sys
from PyQt5.QtCore import QPoint, QBasicTimer, Qt, QTimer
from PyQt5.QtGui import QColor, QPainter, QPen, QFont
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QProgressBar

# Importa la clase de la nueva ventana
from Menu import Menu


class CircularProgressBar(QProgressBar):
    def __init__(self, parent=None):
        super(CircularProgressBar, self).__init__(parent)
        self.setMinimum(0)
        self.setMaximum(100)
        self.timer = QBasicTimer()
        self.progress = 0
        self.setFixedSize(150, 150)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Make the background of the widget transparent
        painter.fillRect(self.rect(), QColor(0, 0, 0, 0))


        size = self.size()
        center = QPoint(int(size.width() / 2), int(size.height() / 2))
        radius = min(size.width(), size.height()) / 2 - 5
        progress = 360 * self.progress / 100

        # Set the color and width of the arc
        painter.setPen(QPen(QColor(75, 0, 130), 10))

        # Draw the arc
        painter.drawArc(center.x() - radius, center.y() - radius, radius * 2, radius * 2, 0, int(progress * 16))

        # Draw the percentage text
        painter.setFont(QFont("Arial", 30))
        painter.drawText(self.rect(), Qt.AlignCenter, f"{self.progress}%")

    def start(self):
        if not self.timer.isActive():
            self.timer.start(50, self)

    def stop(self):
        self.timer.stop()
        QTimer.singleShot(0, self.parent().show_next_window)

    def timerEvent(self, event):
        if self.progress >= 100:
            self.stop()
            return
        self.progress += 1
        self.update()


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Make the background of the main window transparent
        self.setAttribute(Qt.WA_TranslucentBackground)

        # Remove the frame from the main window
        self.setWindowFlags(Qt.FramelessWindowHint)

        self.initUI()

    def initUI(self):
        self.resize(300, 300)
        self.setWindowTitle('Circular Progress Bar')

        self.progress_bar = CircularProgressBar(self)
        self.progress_bar.move(50, 50)
        self.progress_bar.resize(150, 150)
        self.progress_bar.setStyleSheet("border: 4px solid white;")

        self.show()

    def start(self):
        self.progress_bar.start()

    def stop(self):
        self.progress_bar.stop()

    def update_progress(self, value):
        self.progress_bar.progress = value
        self.progress_bar.update()

    # Nueva función para mostrar la nueva ventana
    def show_next_window(self):
        self.next_window = Menu()
        self.next_window.show()
        self.hide()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.start()
    timer = QBasicTimer()
    timer.start(1000, main_window)
    sys.exit(app.exec_())
