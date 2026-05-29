import sys
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel
from PyQt5.QtCore import QTimer

# ---- CLASE DEL NODO ROS 2 ----
class PublisherNode(Node):
    def __init__(self):
        super().__init__('gui_publisher_node')
        self.publisher_ = self.create_publisher(Twist, '/cmd_vel', 10)

    def move_robot(self, linear_x, angular_z):
        msg = Twist()
        msg.linear.x = linear_x
        msg.angular.z = angular_z
        self.publisher_.publish(msg)

# ---- CLASE DE LA INTERFAZ PYQT ----
class VentanaModulo3(QMainWindow):
    def __init__(self, ros_node):
        super().__init__()
        self.ros_node = ros_node
        self.setWindowTitle("Módulo 2 y 3: Publicador ROS 2 (Timers)")
        self.setGeometry(100, 100, 300, 200)
        
        # Diseño básico
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        self.label = QLabel("Control de Turtlesim")
        self.btn_adelante = QPushButton("Adelante")
        self.btn_detener = QPushButton("Detener")
        
        layout.addWidget(self.label)        

        layout.addWidget(self.btn_adelante)
        layout.addWidget(self.btn_detener)

        # Conectar botones (GUI -> ROS)
        self.btn_adelante.clicked.connect(self.mover_adelante)
        self.btn_detener.clicked.connect(self.detener)

        # EL TRUCO: QTimer para el evento de ROS 2
        # Llama a `spin_once` de ROS 2 cada 10ms sin bloquear PyQt
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.spin_ros)
        self.timer.start(10) # 10 milisegundos (100 Hz)

    def mover_adelante(self):
        self.ros_node.move_robot(1.0, 0.0)

    def detener(self):
        self.ros_node.move_robot(0.0, 0.0)

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