#python3
import sys
import rclpy
from rclpy.node import Node
from omni_msgs.msg import OmniState

class GeoNode(Node):
    def __init__(self):
        super().__init__('geo_node')
        self.subscriber = self.create_subscription(OmniState, '/phantom1/state', self.geo_callback, 10)
        self.position = [0.0, 0.0, 0.0]
        self.velocity = [0.0, 0.0, 0.0]
        self.quaternion = [0.0, 0.0, 0.0, 1.0]
        self.botones =[0,0]
        

    def geo_callback(self, msg):
        #self.get_logger().info(f'Received: {msg.pose.position.x}, {msg.pose.position.y}, {msg.pose.position.z}')
        self.position = [msg.pose.position.x, msg.pose.position.y, msg.pose.position.z]
        self.velocity = [round(msg.velocity.x, 4), round(msg.velocity.y, 4), round(msg.velocity.z, 4)]
        self.quaternion = [msg.pose.orientation.x, msg.pose.orientation.y, msg.pose.orientation.z, msg.pose.orientation.w]
        self.botones = [msg.close_gripper, msg.locked]
        
        print(f"Position: \n x: {self.position[0]}\n y: {self.position[1]}\n z: {self.position[2]}\n \n Velocity: \n dx: {self.velocity[0]}\n dy: {self.velocity[1]}\n dz: {self.velocity[2]}\n \n Quaternion: \n x: {self.quaternion[0]}\n y: {self.quaternion[1]}\n z: {self.quaternion[2]}\n w: {self.quaternion[3]}\n Botones: {self.botones} \n")

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