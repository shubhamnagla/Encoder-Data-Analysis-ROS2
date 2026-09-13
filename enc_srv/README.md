# enc_srv

## Overview
`enc_srv` is the ROS 2 interface package that defines the custom service used to reset the simulated encoder.

## Main function
This package creates the service contract that allows nodes to reset the encoder safely and consistently.

## Service definition
The package defines:

```bash
srv/EncoderResetService.srv
```

The service is used to trigger encoder reset requests from the data-analysis logic to the generator node.

## Service interface
The request contains a boolean `reset` field and the response contains a boolean `success` field:

```text
bool reset
---
bool success
```

Example usage:

```bash
ros2 service call /reset_encoder enc_srv/srv/EncoderResetService '{reset: true}'
```

## Key files
- `srv/EncoderResetService.srv` — service definition
- `CMakeLists.txt` — generates the ROS interface

## Build requirements
This package is required by both the generator and the analysis node.

## Notes
`enc_srv` acts as the communication layer between the simulated encoder publisher and the control logic that decides when to reset the encoder.
