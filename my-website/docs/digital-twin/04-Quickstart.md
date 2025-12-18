---
sidebar_position: 4
---

# Quickstart for Digital Twin Module

This guide provides the basic steps to set up a local environment suitable for understanding and experimenting with the concepts presented in the Digital Twin book module.

## Prerequisites

- Ubuntu 22.04 (or a containerized environment with it)
- A complete ROS 2 Humble Hawksbill desktop installation.
- Unity Hub and a Unity Editor (2021.LTS or newer).
- Basic familiarity with Linux command line and ROS 2 concepts.

## Environment Setup

### 1. Install ROS 2 Humble & Gazebo Fortress

If you have not already, follow the official ROS 2 documentation to install the `ros-humble-desktop` package. This will include Gazebo Fortress.

```bash
# Ensure your system is up to date
sudo apt update && sudo apt upgrade

# Follow official ROS 2 Humble installation guide
# ...

# Install the ROS 2 Gazebo integration packages
sudo apt install ros-humble-ros-gz
```

### 2. Install Unity Hub and Editor

1.  Download and install Unity Hub for Linux from the official Unity website.
2.  Using Unity Hub, install a **Unity 2021.LTS** (or newer) editor. Ensure you include Linux build support.

### 3. Set up a ROS 2 Workspace

1.  Create a new ROS 2 workspace to work in.
    ```bash
    mkdir -p ~/digital_twin_ws/src
    cd ~/digital_twin_ws
    ```

2.  Source your ROS 2 and Gazebo environments. It's recommended to add these to your `.bashrc` file.      
    ```bash
    source /opt/ros/humble/setup.bash
    source /usr/share/gazebosim/setup.sh
    ```

## Conceptual Workflow Verification

This module is conceptual, so there is no single project to run. However, you can verify your setup by running the tools independently.

1.  **Run Gazebo:**
    ```bash
    gz sim -v 4 shapes.sdf
    ```
    This should open a Gazebo window with several simple shapes, confirming your Gazebo installation is working.

2.  **Run a ROS 2 Node:**
    ```bash
    ros2 run demo_nodes_cpp talker
    ```
    In another terminal, run `ros2 run demo_nodes_cpp listener` to confirm your ROS 2 installation is working.

3.  **Run Unity:**
    - Open Unity Hub, create a new 3D project, and confirm the editor loads correctly.
