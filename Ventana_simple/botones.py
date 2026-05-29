from PyQt5.QtCore import Qt, QTimer, QSize
from PyQt5.QtGui import QPixmap, QImage, QTransform
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap, QIcon, QPainter, QColor
from PyQt5.QtSvg import QSvgRenderer
from PyQt5 import QtCore


class Ventana(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ventana simple")
        self.setGeometry(100, 100, 400, 300)
        self.label = QLabel("¡Hola, PyQt5!", self)#; self.label.setFrameStyle(QFrame.Panel | QFrame.Raised)
        self.layout = QVBoxLayout()
        
        container = QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)
        self.boton = QPushButton("Presioname", self)
        
        self.layout.addWidget(self.label)        
        self.layout.addWidget(self.boton)
        
        
if __name__ == "__main__":
    app = QApplication([])
    ventana = Ventana()
    ventana.show()
    app.exec_(app.exec_())