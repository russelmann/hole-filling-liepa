cmake_minimum_required( VERSION 3.6 FATAL_ERROR )
set( CMAKE_VERBOSE_MAKEFILE ON )

set( CMAKE_CXX_STANDARD 17 )

get_filename_component( PROJECT_PATH ${CMAKE_CURRENT_SOURCE_DIR} ABSOLUTE )

project( hole_filling_liepa_lib )

file ( GLOB HEADERS
	${PROJECT_PATH}/*.hpp
)

file( GLOB SOURCES
	${PROJECT_PATH}/*.cpp
)

set ( INCLUDES
	${ROOT_DIR}/include
	${EIGEN_DIR}
)

set( SOURCES ${HEADERS} ${SOURCES} )

include_directories( ${INCLUDES} )

add_library( hole_filling_liepa_lib ${SOURCES} )
