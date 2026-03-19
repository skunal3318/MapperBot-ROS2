cmake_minimum_required(VERSION 3.8)
project(diff_robot)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(robot_state_publisher REQUIRED)
find_package(gazebo_ros REQUIRED)
find_package(controller_manager REQUIRED)
find_package(diff_drive_controller REQUIRED)
find_package(nav_msgs REQUIRED)
find_package(nav2_msgs REQUIRED)
find_package(geometry_msgs REQUIRED)

install(
  DIRECTORY launch
  DESTINATION share/${PROJECT_NAME}/
)




add_executable(pose_publisher src/odom_pose.cpp)
ament_target_dependencies(pose_publisher rclcpp nav_msgs geometry_msgs)

add_executable(vel_publisher src/vel_publisher.cpp)
ament_target_dependencies(vel_publisher rclcpp geometry_msgs)



if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  set(ament_cmake_copyright_FOUND TRUE)
  set(ament_cmake_cpplint_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()

install(TARGETS
  pose_publisher
  vel_publisher
  DESTINATION lib/${PROJECT_NAME})

ament_package()
