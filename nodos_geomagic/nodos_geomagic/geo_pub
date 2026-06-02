import sys
import rclpy
from rclpy.node import Node
from omni_msgs.msg import OmniState, OmniFeedback

class GeoNode(Node):
    def __init__(self):
        super().__init__('geo_node')
        self.parameter_declarado = self.declare_parameter('modo', 'cubo')
        self.modo = self.get_parameter('modo').value
        self.subscriber = self.create_subscription(OmniState, '/phantom1/state', self.geo_callback, 10)
        self.publisher = self.create_publisher(OmniFeedback, '/phantom1/force_feedback', 10)
        self.position = [0.0, 0.0, 0.0]
        self.velocity = [0.0, 0.0, 0.0]
        self.quaternion = [0.0, 0.0, 0.0, 1.0]
        self.botones =[0,0]
    

    def geo_callback(self, msg):
        #self.get_logger().info(f'Received: {msg.pose.position.x}, {msg.pose.position.y}, {msg.pose.position.z}')
        self.position = [msg.pose.position.x/1000, msg.pose.position.y/1000, msg.pose.position.z/1000]
        self.velocity = [round(msg.velocity.x, 4), round(msg.velocity.y, 4), round(msg.velocity.z, 4)]
        self.quaternion = [msg.pose.orientation.x, msg.pose.orientation.y, msg.pose.orientation.z, msg.pose.orientation.w]
        self.botones = [msg.close_gripper, msg.locked]
        
        print(f"Position: {self.position}\n Velocity: {self.velocity}\n Quaternion: {self.quaternion}\n Botones: {self.botones}")

        # Aquí integramos la publicación de fuerzas al flujo del programa
        # Llamamos a "cubo" para calcular y devolver las fuerzas de colisión.
        if self.modo == 'cubo':
            force_x, force_y, force_z = self.cubo()
        elif self.modo == 'fuera_de_cubo':
            force_x, force_y, force_z = self.fuera_de_cubo()
        elif self.modo == 'esfera':
            force_x, force_y, force_z = self.esfera()
        elif self.modo == 'fuera_de_esfera':
            force_x, force_y, force_z = self.fuera_de_esfera()
        else:
            self.get_logger().warn(f"Modo desconocido: {self.modo}. No se aplicarán fuerzas.")
            return
        self.publish_force_feedback(force_x, force_y, force_z)

    def cubo(self): #limitar la movilidad del geoamgic dentro de los limites de un cubo de 0.1m de lado
        kp = 150.0 # rigidez del muro virtual (N/m)
        kd = 0.001 # amortiguamiento (N·s/m)
        
        l = 0.03 # mitad del lado del cubo (en metros)

        force_x, force_y, force_z = 0.0, 0.0, 0.0
        
        force_x = -kp * max(0.0, self.position[0] - l) - kp * min(0.0, self.position[0] + l)# - kd * self.velocity[0]
        force_y = -kp * max(0.0, self.position[1] - l) - kp * min(0.0, self.position[1] + l)# - kd * self.velocity[1]
        force_z = -kp * max(0.0, self.position[2] - l) - kp * min(0.0, self.position[2] + l) #- kd * self.velocity[2]
            
        return force_x, force_y, force_z
    
    def fuera_de_cubo(self):
        kp = 150.0 # rigidez del muro virtual (N/m)

        l = 0.04 # mitad del lado del cubo (en metros)
        
        force_x, force_y, force_z = 0.0, 0.0, 0.0
        
        # Verificar si estamos DENTRO del cubo
        if abs(self.position[0]) < l and abs(self.position[1]) < l and abs(self.position[2]) < l:
            
            # Encontrar a qué cara estamos más cerca para saber hacia dónde empujar
            dist_x = l - abs(self.position[0])
            dist_y = l - abs(self.position[1])
            dist_z = l - abs(self.position[2])
            
            # Empujar solo en el eje más cercano a la superficie para expulsar al robot
            if dist_x <= dist_y and dist_x <= dist_z:
                # Expulsar en X
                if self.position[0] >= 0:
                    force_x = kp * dist_x
                else:
                    force_x = -kp * dist_x
            elif dist_y <= dist_x and dist_y <= dist_z:
                # Expulsar en Y
                if self.position[1] >= 0:
                    force_y = kp * dist_y
                else:
                    force_y = -kp * dist_y
            else:
                # Expulsar en Z
                if self.position[2] >= 0:
                    force_z = kp * dist_z
                else:
                    force_z = -kp * dist_z

        return force_x, force_y, force_z
            
    def esfera(self): #limitar la movilidad del geoamgic dentro de los limites de una esfera de 0.1m de radio
        kp = 150.0 # rigidez del muro virtual (N/m)
        kd = 0.001 # amortiguamiento (N·s/m)
        
        r = 0.03 # radio de la esfera (en metros)

        force_x, force_y, force_z = 0.0, 0.0, 0.0
        
        dist = (self.position[0]**2 + self.position[1]**2 + self.position[2]**2)**0.5
        
        if dist > r:
            # Calcular la fuerza de restitución proporcional a cuánto estamos fuera de la esfera
            excess_dist = dist - r
            force_magnitude = kp * excess_dist
            
            # Calcular la dirección de la fuerza (hacia el centro de la esfera)
            dir_x = -self.position[0] / dist
            dir_y = -self.position[1] / dist
            dir_z = -self.position[2] / dist
            
            force_x = force_magnitude * dir_x
            force_y = force_magnitude * dir_y
            force_z = force_magnitude * dir_z
            
        return force_x, force_y, force_z 
            
    def fuera_de_esfera(self):
        kp = 150.0 # rigidez del muro virtual (N/m)

        r = 0.06 # radio de la esfera (en metros)
        
        force_x, force_y, force_z = 0.0, 0.0, 0.0
        
        dist = (self.position[0]**2 + self.position[1]**2 + self.position[2]**2)**0.5
        
        if dist < r:
            # Calcular la fuerza de restitución proporcional a cuánto estamos dentro de la esfera
            excess_dist = r - dist
            force_magnitude = kp * excess_dist
            
            # Calcular la dirección de la fuerza (hacia afuera del centro de la esfera)
            dir_x = self.position[0] / dist
            dir_y = self.position[1] / dist
            dir_z = self.position[2] / dist
            
            force_x = force_magnitude * dir_x
            force_y = force_magnitude * dir_y
            force_z = force_magnitude * dir_z
            
        return force_x, force_y, force_z        
            
    def publish_force_feedback(self, force_x, force_y, force_z):
        msg = OmniFeedback()
        
        # Posición
        msg.position.x = 0.0
        msg.position.y = 0.0
        msg.position.z = 0.0
        
        # Saturar la fuerza a ±3.3 N por componente
        msg.force.x = max(-3.3, min(3.3, float(force_x)))
        msg.force.y = max(-3.3, min(3.3, float(force_y)))
        msg.force.z = max(-3.3, min(3.3, float(force_z)))
        self.get_logger().info(f"Fuerza publicada: [{msg.force.x:.2f}, {msg.force.y:.2f}, {msg.force.z:.2f}]")

        self.publisher.publish(msg)
        
        
    
def main(args=None):
    rclpy.init(args=args)
    geo_node = GeoNode()
    try:
        rclpy.spin(geo_node)
    except KeyboardInterrupt:
        print('Shutting down GeoNode...')
    finally:
        # Destruir el nodo de forma segura si todavía es válido
        geo_node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()

if __name__ == '__main__':
    main()