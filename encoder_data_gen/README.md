# encoder_data_gen

## Overview
`encoder_data_gen` is the ROS 2 package responsible for simulating encoder output data. It publishes a stream of integer values that mimic motor-speed readings.

## Main function
The package contains a node named `encoder_data_node`.

### Behavior
- Publishes random speed values to the `encoder_data` topic
- Uses `std_msgs/msg/Int32` as the topic message type
- Sends a new value every 100 milliseconds
- Random values range from 0 to 99
- Provides the `reset_encoder` service to reset the internal speed to zero

## Key files
- `src/encoder_data_node.cpp` — Node implementation
- `launch/encoder_mimic_launch.py` — Launch file to start the generator

## How to run
From the workspace root:

```bash
source /opt/ros/<ros2-distro>/setup.bash
colcon build --symlink-install
source install/setup.bash
ros2 launch encoder_data_gen encoder_mimic_launch.py
```

This starts the encoder generator in the foreground. The node publishes on `encoder_data`; per-message publishing logs are disabled by default.

## Service
The node exposes:

```bash
/reset_encoder
```

This service uses the custom type `enc_srv/srv/EncoderResetService` from the `enc_srv` package. Its request contains `reset` and its response contains `success`.

Call it manually with:

```bash
ros2 service call /reset_encoder enc_srv/srv/EncoderResetService '{reset: true}'
```

## Notes
The node is built for simple simulation and testing in a ROS 2 ecosystem and acts as the data source for the analysis package.
