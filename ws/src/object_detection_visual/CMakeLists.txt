cmake_minimum_required(VERSION 3.5)
project(object_detection_visual)

# Default to C99
if(NOT CMAKE_C_STANDARD)
  set(CMAKE_C_STANDARD 99)
endif()

# Default to C++14
if(NOT CMAKE_CXX_STANDARD)
  set(CMAKE_CXX_STANDARD 14)
endif()

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(visualization_msgs REQUIRED)

# Find the Gazebo Libraries used directly by the example
find_package(gz-rendering7 REQUIRED OPTIONAL_COMPONENTS ogre ogre2)
find_package(gz-sensors7 REQUIRED COMPONENTS rendering camera)

# uncomment the following section in order to fill in
# further dependencies manually.
# find_package(<dependency> REQUIRED)

if (TARGET gz-rendering6::ogre)
  add_definitions(-DWITH_OGRE)
endif()
if (TARGET gz-rendering6::ogre2)
  add_definitions(-DWITH_OGRE2)
endif()

add_executable(object_detection_visual src/object_detection_visual_node.cpp)
ament_target_dependencies(object_detection_visual rclcpp visualization_msgs gz-sensors7)

target_include_directories(object_detection_visual PUBLIC
        include
        )

install(TARGETS
  object_detection_visual
  DESTINATION lib/${PROJECT_NAME}
  )

# Install launch files.
install(DIRECTORY
  launch
  models
  rviz
  DESTINATION share/${PROJECT_NAME}/
)

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  # the following line skips the linter which checks for copyrights
  # uncomment the line when a copyright and license is not present in all source files
  #set(ament_cmake_copyright_FOUND TRUE)
  # the following line skips cpplint (only works in a git repo)
  # uncomment the line when this package is not in a git repo
  #set(ament_cmake_cpplint_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()

ament_package()
