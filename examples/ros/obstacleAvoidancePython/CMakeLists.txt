project(obstacleAvoidancePython)

cmake_minimum_required(VERSION 2.8.3)

find_package(catkin REQUIRED COMPONENTS
  roscpp
  sensor_msgs
  geometry_msgs
)

catkin_package()
include_directories(${catkin_INCLUDE_DIRS})
install(PROGRAMS obstacleAvoidancePython.py DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION})
