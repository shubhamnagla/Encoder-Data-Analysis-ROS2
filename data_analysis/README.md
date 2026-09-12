# data_analysis

## Overview
`data_analysis` is the ROS 2 analysis package that watches the simulated encoder data stream and triggers a reset when the motor-speed average exceeds a threshold.

## Main function
The package contains the node `encoder_data_analysis_node`.

### Behavior
- Subscribes to the `encoder_data` topic
- Stores the most recent 10 encoder values
- Computes a moving average across those values
- Resets the encoder if the average exceeds 70
- Clears the recorded values after a reset

## Key files
- `data_analysis/encoder_data_analysis_node.py` — main analysis logic
- `setup.py` — Python package configuration and console entry point

## How to run
From the workspace root:

```bash
source /opt/ros/<ros2-distro>/setup.bash
colcon build --symlink-install
source install/setup.bash
ros2 run data_analysis encoder_data_analysis_node
```

## Interaction with the rest of the system
- Reads data from `encoder_data`
- Calls the service `/reset_encoder`
- Uses `enc_srv/srv/EncoderResetService` to trigger reset behavior in the generator node

## Notes
This package demonstrates using a rolling-window average to detect abnormal speed conditions and respond by communicating with another node via a ROS 2 service.
