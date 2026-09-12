# this node subscribes to the encoder_data topic, 
# calculates the moving average of the last 10 values, and resets the encoder if the moving average exceeds 70.
# mimics the behavior of a motor encoder, where the encoder value is reset if the motor speed exceeds a certain threshold.

import rclpy
from rclpy.node import Node

from std_msgs.msg import Int32

from enc_srv.srv import EncoderResetService

class EncoderDataAnalysisNode(Node):
    def encoder_reset_client(self):
        self.cli = self.create_client(EncoderResetService, 'reset_encoder')
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Service not available, waiting again...')
        self.req = EncoderResetService.Request()

    def send_request(self):
        self.get_logger().info('Sending request to reset encoder...')
        return self.cli.call_async(self.req)

    def __init__(self):
        super().__init__('encoder_data_analysis_node')
        self.avg_list = []
        self.subscription = self.create_subscription(
            Int32,
            'encoder_data',
            self.encoder_data_callback,
            10
        )
        self.subscription  # prevent unused variable warning

    def encoder_data_callback(self, msg):
        motor_speed = msg.data
        self.avg_list.append(motor_speed)
        if len(self.avg_list) > 10:
            self.avg_list.pop(0)  # Keep only the last 10 valuesS
        for i in range(len(self.avg_list)):
            moving_average = sum(self.avg_list) / 10
            # self.get_logger().info(f"Moving Average of last 10 values: {moving_average:.2f}")
        if moving_average > 70:
            self.get_logger().warn(f"Moving average {moving_average:.2f} exceeds threshold of 70. Resetting encoder.")
            self.encoder_reset_client()
            self.send_request()
            self.avg_list.clear()  # Clear the list after reset

def main():
    rclpy.init()
    node = EncoderDataAnalysisNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info("\n[!] Program interrupted by user. Cleaning up and exiting safely.")
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()

if __name__ == '__main__':
    main()
