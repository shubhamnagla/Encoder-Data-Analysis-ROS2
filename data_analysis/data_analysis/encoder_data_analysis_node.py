# this node subscribes to the encoder_data topic, 
# calculates the moving average of the last 10 values, and resets the encoder if the moving average exceeds 70.
# mimics the behavior of a motor encoder, where the encoder value is reset if the motor speed exceeds a certain threshold.

import rclpy
from rclpy.node import Node

from std_msgs.msg import Int32

from enc_srv.srv import EncoderResetService

class EncoderDataAnalysisNode(Node):

    # Function to send a request to the EncoderResetService
    def send_request(self):
        self.get_logger().info('Sending request to reset encoder...')
        future = self.cli.call_async(self.req) # Send the request asynchronously
        future.add_done_callback(self.reset_encoder_callback) # Add a callback to handle the response

    # Callback function to handle the response from the service call
    def reset_encoder_callback(self, future): 
        try:
            response = future.result() # Get the response from the service call
            if response.success:
                self.get_logger().info('Encoder reset successfully.')
            else:
                self.get_logger().error('Failed to reset encoder.')
        except Exception as e:
            self.get_logger().error(f'Service call failed: {e}')

    # Initialize the node, create a client for the EncoderResetService, and subscribe to the encoder_data topic
    def __init__(self):
        super().__init__('encoder_data_analysis_node')
        # Create a client for the EncoderResetService
        self.cli = self.create_client(EncoderResetService, 'reset_encoder')
        self.req = EncoderResetService.Request()

        # Initialize a list to store the last 10 encoder values
        self.avg_list = []
        # Create a subscription to the encoder_data topic
        self.subscription = self.create_subscription(
            Int32,
            'encoder_data',
            self.encoder_data_callback,
            10
        )
        self.subscription  # prevent unused variable warning

    # Callback function to process incoming encoder data, calculate the moving average, and reset the encoder if necessary
    def encoder_data_callback(self, msg):
        motor_speed = msg.data
        self.avg_list.append(motor_speed)
        # Calculate the moving average of the last 10 values
        if len(self.avg_list) > 10:
            self.avg_list.pop(0)  # Keep only the last 10 values

        # Calculate the moving average
        moving_average = sum(self.avg_list) / len(self.avg_list)

        # Log the received motor speed and the moving average
        self.get_logger().debug(f"Received motor speed: {motor_speed}, Moving Average of last 10 values: {moving_average:.2f}")

        # self.get_logger().info(f"Moving Average of last 10 values: {moving_average:.2f}")
        if moving_average > 70:
            self.get_logger().warn(f"Moving average {moving_average:.2f} exceeds threshold of 70. Resetting encoder.")
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
