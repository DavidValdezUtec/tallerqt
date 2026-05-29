import sys
import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel
from PyQt5.QtCore import QTimer

# ---- CLASE DEL NODO ROS 2 ----
class PublisherNode(Node):
    def __init__(self):
        super().__init__('gui_publisher_node')
        self.publisher_ = self.create_publisher(Int32, '/contador', 10)
        self.contador = 0

    def publicar_contador(self):
        msg = Int32()
        msg.data = self.contador
        self.publisher_.publish(msg)
        self.contador += 1
        return msg.data

# ---- CLASE DE LA INTERFAZ PYQT ----
class VentanaModulo3(QMainWindow):
    def __init__(self, ros_node):
        super().__init__()
        self.ros_node = ros_node
        self.setWindowTitle("Módulo 2 y 3: Publicador Contador (1 Hz)")
        self.setGeometry(100, 100, 300, 200)
        
        # Diseño básico
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        
        self.boton_iniciar = QPushButton("Iniciar Contador")
        self.boton_iniciar.clicked.connect(self.iniciar_timer)
        
        self.boton_pausar = QPushButton("Pausar Contador")
        self.boton_pausar.clicked.connect(self.detener_timer)
        self.boton_pausar.setEnabled(False) # Inicia deshabilitado por defecto
        
        layout.addWidget(self.boton_iniciar)
        layout.addWidget(self.boton_pausar)
        
        central_widget.setLayout(layout)

        self.label = QLabel("Contador: 0")
        self.label.setStyleSheet("font-size: 24px; font-weight: bold; color: green;")
        
        layout.addWidget(self.label)    
        #Timer para procesar eventos de ROS 2 sin bloquear la GUI
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.spin_ros)
        self.timer.start(10) # 100 ms = 0.1 segundo
        
        #Timer para publicar cada segundo
        self.timer_publicador = QTimer(self)
        self.timer_publicador.timeout.connect(self.ciclo_publicacion)  

    def iniciar_timer(self):
        # Inicia el timer de publicación
        self.timer_publicador.start(1000) # 1000 ms = 1 segundo
        self.boton_iniciar.setEnabled(False)
        self.boton_pausar.setEnabled(True)

    def detener_timer(self):
        # Detiene el timer de publicación
        self.timer_publicador.stop()
        self.boton_iniciar.setEnabled(True)
        self.boton_pausar.setEnabled(False)

    def ciclo_publicacion(self):
        # 1. Hacemos que ROS publique el dato
        nuevo_valor = self.ros_node.publicar_contador()
        # 2. Actualizamos la interfaz gráfica para reflejar el cambio
        self.label.setText(f"Contador: {nuevo_valor}")

    def spin_ros(self):
        # Permite a ROS 2 procesar callbacks rápidamente y se sale
        rclpy.spin_once(self.ros_node, timeout_sec=0.01)

if __name__ == "__main__":
    rclpy.init(args=sys.argv)
    ros_node = PublisherNode()
    
    app = QApplication(sys.argv)
    ventana = VentanaModulo3(ros_node)
    ventana.show()
    
    app.exec_() # Bloquea aquí hasta cerrar la ventana
    
    # Limpiar ROS al salir
    ros_node.destroy_node()
    rclpy.shutdown()