FROM osrf/ros:humble-desktop

# Avoid interactive prompts
ENV DEBIAN_FRONTEND=noninteractive

# Install dependencies
RUN apt update && apt install -y \
    ros-humble-nav2-bringup \
    ros-humble-slam-toolbox \
    ros-humble-gazebo-ros-pkgs \
    ros-humble-ros2-control \
    ros-humble-ros2-controllers \
    ros-humble-controller-manager \
    python3-colcon-common-extensions \
    && rm -rf /var/lib/apt/lists/*

# Create workspace
WORKDIR /ros2_ws

# Copy your project
COPY . /ros2_ws/src/diff_robot

# Build workspace
RUN /bin/bash -c "source /opt/ros/humble/setup.bash && colcon build"

# Source ROS automatically
RUN echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc
RUN echo "source /ros2_ws/install/setup.bash" >> ~/.bashrc

# Default command
CMD ["bash"]