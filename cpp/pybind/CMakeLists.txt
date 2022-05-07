cmake_minimum_required( VERSION 3.6 FATAL_ERROR )
set( CMAKE_VERBOSE_MAKEFILE ON )
set( CMAKE_CXX_STANDARD 17 )

if( WIN32 )
    set( EXTENSION ".pyd" )
else( WIN32 )
    set( EXTENSION ".so" )
endif( WIN32 )

project( core )
get_filename_component( PROJECT_PATH "${CMAKE_CURRENT_SOURCE_DIR}" ABSOLUTE )

file ( GLOB HEADERS
	${PROJECT_PATH}/*.hpp
)

file( GLOB SOURCES
	${PROJECT_PATH}/*.cpp
)

pybind11_add_module( ${PROJECT_NAME} ${SOURCES} ${HEADERS} )

add_dependencies( ${PROJECT_NAME} hole_filling_liepa_lib )
target_link_libraries( ${PROJECT_NAME} PRIVATE hole_filling_liepa_lib )

if ( UNIX AND NOT APPLE )
	target_link_libraries( ${PROJECT_NAME} PRIVATE stdc++fs )
endif()
