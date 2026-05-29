import sys
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget
from PyQt5.QtCore import QThread, pyqtSignal

# ---- CLASE HILO PARA ROS 2 ----
class ROS2Thread(QThread):
    # Definimos una 'PyQt Signal' personalizada que enviará un string.
    # Es VITAL usar esto para enviar datos desde el hilo ROS a la GUI
    nuevo_mensaje = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.node = None

    def run(self):
        """Este método arranca al llamar a thread.start()"""
        rclpy.init()
        self.node = Node('gui_subscriber_node')
        self.sub = self.node.create_subscription(
            String,
            '/chatter',
            self.callback_mensaje,
            10
        )
        # Hacemos spin aquí. Bloquea ESTE hilo, NO la GUI.
        rclpy.spin(self.node)

    def callback_mensaje(self, msg):
        # NO TOCAR LA GUI DIRECTAMENTE AQUÍ (ej. label.setText(msg.data))
        # En su lugar, emitimos nuestra señal. Qt se encarga del hilo con seguridad.
        self.nuevo_mensaje.emit(msg.data)
        
    def stop(self):
        if self.node:
            self.node.destroy_node()
        rclpy.shutdown()

# ---- CLASE DE LA INTERFAZ PYQT ----
class VentanaModulo4(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Módulo 4: Suscriptor y Hilos Seguros")
        self.setGeometry(100, 100, 300, 150)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        self.label = QLabel("Esperando mensajes de ROS 2...")
        self.label.setStyleSheet("font-size: 14px; font-weight: bold; color: blue;")
        layout.addWidget(self.label)

        # Inicializar y arrancar el hilo de ROS 2
        self.ros_thread = ROS2Thread()
        # Conectamos la señal que creamos a la función de la GUI
        self.ros_thread.nuevo_mensaje.connect(self.actualizar_label)
        self.ros_thread.start() # Empieza a correr run()

    def actualizar_label(self, texto):
        # Esta ejecución transcurre a salvo en el hilo principal
        self.label.setText(f"Recibido desde tópico: {texto}")

    def closeEvent(self, event):
        # Sobrescribimos el evento de cerrar ventana para matar el hilo de ROS
        self.ros_thread.stop()
        self.ros_thread.wait() # Espera a que termine limpiamente
        super().closeEvent(event)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VentanaModulo4()
    ventana.show()
    sys.exit(app.exec_())