# SPDX-License-Identifier: BSD-3-Clause
# SPDX-FileCopyrightText: Czech Technical University in Prague

cmake_minimum_required(VERSION 3.10.2)
project(zyxel_gs1200_snmp_agent)

find_package(catkin REQUIRED)

catkin_python_setup()

catkin_package()

catkin_install_python(PROGRAMS
  nodes/print_stats
  nodes/snmp_agent
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)

if (CATKIN_ENABLE_TESTING)
  find_package(roslint REQUIRED)

  roslint_custom(catkin_lint "-W2" .)

  # Run roslint on Python sources
  file(GLOB_RECURSE python_files src/*.py nodes/*)
  roslint_python("${python_files}")

  roslint_add_test()
  
  # catkin_add_nosetests(test)
endif()
