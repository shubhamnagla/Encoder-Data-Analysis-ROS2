/*
The Node below is used to mimic a motor speed encoder. 
It publishes a random speed value between 0 and 99 to the topic "encoder_data" every 100 milliseconds. 
The node is implemented using ROS 2 and C++17 standard.
*/
#include <cstdio>
#include <chrono>
#include <memory>

#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/int32.hpp"
#include "enc_srv/srv/encoder_reset_service.hpp"

using namespace std::chrono_literals;

class EncoderDataNode : public rclcpp::Node
{
public:
  EncoderDataNode()
  : Node("encoder_data_node"), motor_speed_(0)
  {
    service_ = this->create_service<enc_srv::srv::EncoderResetService>(
      "reset_encoder", 
      [this](const std::shared_ptr<enc_srv::srv::EncoderResetService::Request> request,
             std::shared_ptr<enc_srv::srv::EncoderResetService::Response> response) {
        (void)request; // Unused parameter
        motor_speed_ = 0; // Reset the motor speed to 0
        response->success = true; // Indicate successful reset
        RCLCPP_INFO(this->get_logger(), "Encoder reset to 0.");
      });
    publisher_ = this->create_publisher<std_msgs::msg::Int32>("encoder_data", 10);
    auto timer_callback = [this]() -> void {
      motor_speed_ = random() % 100; // Random speed between 0 and 99
      auto message = std_msgs::msg::Int32();
      message.data = motor_speed_; // Publish the random speed
      // RCLCPP_INFO(this->get_logger(), "Motor Speed: '%d'", message.data);
      publisher_->publish(message);
    };
    timer_ = this->create_wall_timer(10ms, timer_callback);
  }

private:
  rclcpp::TimerBase::SharedPtr timer_;
  rclcpp::Publisher<std_msgs::msg::Int32>::SharedPtr publisher_;
  rclcpp::Service<enc_srv::srv::EncoderResetService>::SharedPtr service_;
  int32_t motor_speed_;
};

int main(int argc, char ** argv)
{
  rclcpp::init(argc, argv);
  std::cout << "Running encoder_data_node..." << std::endl;
  rclcpp::spin(std::make_shared<EncoderDataNode>());
  try {
    rclcpp::shutdown();
  } catch (const std::exception & e) {
    RCLCPP_ERROR(rclcpp::get_logger("rclcpp"), "Exception during shutdown: %s", e.what());
  }

  std::cout << "[!] Ctrl+C detected. encoder_data_node has been shut down." << std::endl;

  return 0;
}
