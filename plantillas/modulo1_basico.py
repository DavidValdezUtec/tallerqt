import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit

class VentanaModulo1(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Módulo 1: PyQt Básico")
        self.setGeometry(100, 100, 300, 200)

        # 1. Widget central para contenerlo todo
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # 2. Layout (Organización) - QVBoxLayout organiza en vertical
        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        # 3. Creación de Widgets
        self.label = QLabel("Ingresa tu nombre:")
        self.input_texto = QLineEdit()
        self.boton = QPushButton("Saludar")

        # 4. Añadimos los widgets al layout
        layout.addWidget(self.label)
        layout.addWidget(self.input_texto)
        layout.addWidget(self.boton)

        # 5. Signals y Slots (Interacción)
        self.boton.clicked.connect(self.al_presionar_boton)

    def al_presionar_boton(self):
        # Esta función (Slot) se ejecuta al presionar el botón (Signal)
        nombre = self.input_texto.text()
        self.label.setText(f"¡Hola {nombre}, bienvenido al curso!")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VentanaModulo1()
    ventana.show()
    sys.exit(app.exec_())