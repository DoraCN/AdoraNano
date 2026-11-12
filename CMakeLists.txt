cmake_minimum_required(VERSION 3.16)
project(adora_nano_description)

find_package(ament_cmake REQUIRED)

install(DIRECTORY urdf meshes launch config
        DESTINATION share/${PROJECT_NAME})
install(FILES README.md
        DESTINATION share/${PROJECT_NAME})

ament_package()
