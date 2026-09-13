# Encoder Mimic ROS 2 Workspace

This directory contains the three ROS 2 packages for the encoder mimic project.

## Packages

### 1. `encoder_data_gen`
Purpose: simulates an encoder by publishing random motor-speed values.

Functionality:
- Publishes a `std_msgs/msg/Int32` message to the `encoder_data` topic
- Emits a new value every 10 ms
- Uses a random value from 0 to 99
- Exposes the `/reset_encoder` service to reset the internal speed back to zero

Run:
```bash
ros2 launch encoder_data_gen encoder_mimic_launch.py
```

### 2. `enc_srv`
Purpose: defines the custom ROS 2 service interface used by the system.

Functionality:
- Creates the `EncoderResetService` service definition with a boolean `reset` request and boolean `success` response
- Allows the analysis node to request an encoder reset cleanly through ROS 2 service communication

Service type:
```bash
enc_srv/srv/EncoderResetService
```

### 3. `data_analysis`
Purpose: monitors encoder data and triggers resets when the signal exceeds safe limits.

Functionality:
- Subscribes to `encoder_data`
- Maintains the last 10 readings in a rolling list
- Computes a moving average
- Requests an encoder reset when the average exceeds 70
- Clears the moving-average buffer after reset

Run:
```bash
ros2 run data_analysis encoder_data_analysis_node
```

## End-to-end setup

From the workspace root:

```bash
source /opt/ros/<ros2-distro>/setup.bash
colcon build --symlink-install
source install/setup.bash
```

Then start the system:

```bash
ros2 launch encoder_data_gen encoder_mimic_launch.py
ros2 run data_analysis encoder_data_analysis_node
```

You can also trigger the reset manually:

```bash
ros2 service call /reset_encoder enc_srv/srv/EncoderResetService '{reset: true}'
```

This project is designed to demonstrate ROS 2 publisher/subscriber communication, custom service interfaces, and a simple state-reset control loop.
