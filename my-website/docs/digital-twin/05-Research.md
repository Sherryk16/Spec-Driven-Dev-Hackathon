---
sidebar_position: 5
---

# Research & Decisions for Digital Twin Module

This document records the decisions made for key technical clarifications during the planning phase of the
 Digital Twin book module (`003-digital-twin-module-2`).

---

## 1. Gazebo Version Selection

- **Need**: Determine the correct version of Gazebo to use for a book targeting the ROS 2 Humble Hawksbill
 LTS release.
- **Decision**: Gazebo Fortress.
- **Rationale**:
  - The official ROS 2 documentation and Gazebo documentation explicitly state that ROS 2 Humble is officially paired with and supported by Gazebo Fortress.
  - The `ros_gz` integration packages available through `apt` for Humble are built and tested against Fortress, ensuring maximum compatibility and stability.
- **Alternatives Considered**:
  - **Gazebo Classic (`gazebo-11`)**: While it can be used with ROS 2, it is the older version of Gazebo and is not the default for Humble. It would require a different set of bridge packages (`ros1_bridge`) and is not the forward-looking choice.
  - **Newer Gazebo Versions (e.g., Harmonic)**: Using versions newer than Fortress with Humble would require building the `ros_gz` packages from source, which adds complexity that is unnecessary for the educational goals of this book module.

---

## 2. Unity Version and URDF Importer

- **Need**: Select a suitable Unity version and a standard method for importing URDF robot models.        
- **Decision**:
  - **Unity Version**: A recent Long-Term Support (LTS) version, specifically **2021.LTS** or newer.      
  - **URDF Importer**: The official **Unity Robotics Hub URDF Importer** package.
- **Rationale**:
  - Unity's official robotics packages are tested and supported on Unity 2020.x and newer. Using a recent LTS version ensures stability and access to the latest features of both the engine and the robotics packages.
  - The Unity Robotics Hub provides the standard, best-practice tools for ROS integration. The `URDF-Importer` is the official tool for this purpose and is designed to work with the `ROS-TCP-Connector`.
- **Alternatives Considered**:
  - **Custom Importer**: Building a custom URDF parser would be a significant and unnecessary effort, reinventing a solved problem.
  - **Older Unity Versions**: Using older versions might introduce compatibility issues with the latest ROS 2 integration packages and miss out on performance or feature improvements.

---

## 3. ROS 2 Integration Strategy

- **Need**: Define the standard method for passing data between the simulation environments (Gazebo, Unity) and ROS 2.
- **Decision**:
  - **Gazebo**: Use the `ros_gz_bridge` package.
  - **Unity**: Use the `ROS-TCP-Connector` package.
- **Rationale**:
  - **Gazebo**: `ros_gz_bridge` is the official and standard tool for connecting Gazebo Fortress with ROS 2 Humble. It provides a direct, configurable bridge to translate Gazebo Transport messages to ROS 2 messages (and vice-versa) for topics, services, and other primitives. This is the most direct and efficient integration method.
  - **Unity**: The `ROS-TCP-Connector`, part of the Unity Robotics Hub, is the official and recommended method for connecting a Unity simulation to a ROS 2 network. It establishes a TCP connection and handles message serialization/deserialization between Unity's C# environment and the ROS 2 ecosystem.
- **Alternatives Considered**:
  - **Custom Sockets/Middleware**: Creating a custom communication layer would be highly complex and error-prone. The existing official tools are robust and well-documented.
  - **File-based Exchange**: Using files to exchange data would be extremely slow and not representative of real-time robotics systems.
