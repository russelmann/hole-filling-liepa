cmake_minimum_required( VERSION 3.6 FATAL_ERROR )
set( CMAKE_VERBOSE_MAKEFILE ON )
set( CMAKE_CXX_STANDARD 17 )

get_filename_component( ROOT_DIR ${CMAKE_CURRENT_SOURCE_DIR} ABSOLUTE )

#if( DEFINED $ENV{pythonLocation} )
#	set( Python3_ROOT_DIR "$ENV{pythonLocation}" )
#else()
#	set( Python3_ROOT_DIR "${Python3_LIBRARY_DIRS}/.." )
#endif()

#find_package( Python3 COMPONENTS Interpreter Development REQUIRED )

#set( pybind11_DIR "${Python3_ROOT_DIR}/Lib/site-packages/pybind11/share/cmake/pybind11" )
#set( Eigen3_DIR "${Python3_ROOT_DIR}/Library/share/eigen3/cmake" )

# if( MSVC )
# 	set_property(GLOBAL PROPERTY USE_FOLDERS ON)
# endif()

find_package( Eigen3 REQUIRED )
find_package( pybind11 CONFIG REQUIRED )

project( hole-filling-liepa )

add_subdirectory( ${ROOT_DIR}/lib "${CMAKE_CURRENT_BINARY_DIR}/lib" )
add_subdirectory( ${ROOT_DIR}/pybind "${CMAKE_CURRENT_BINARY_DIR}/pybind" )
