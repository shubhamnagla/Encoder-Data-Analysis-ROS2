# enc_srv

## Overview
`enc_srv` is the ROS 2 interface package that defines the custom service used to reset the simulated encoder.

## Main function
This package creates the service contract that allows nodes to reset the encoder safely and consistently.

## Service definition
The package defines:

```bash
EncoderResetService.srv
```

The service is used to trigger encoder reset requests from the data-analysis logic to the generator node.

## Service interface
The service request is empty and the response contains a success flag.

Example usage:

```bash
ros2 service call /reset_encoder enc_srv/srv/EncoderResetService '{}'
```

## Key files
- `srv/EncoderResetService.srv` — service definition
- `CMakeLists.txt` — generates the ROS interface

## Build requirements
This package is required by both the generator and the analysis node.

## Notes
`enc_srv` acts as the communication layer between the simulated encoder publisher and the control logic that decides when to reset the encoder.
