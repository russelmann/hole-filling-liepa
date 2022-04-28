cmake_minimum_required( VERSION 3.6 FATAL_ERROR )
set( CMAKE_VERBOSE_MAKEFILE ON )

set( CMAKE_CXX_STANDARD 17 )

if( WIN32 )
    set( EXTENSION ".pyd" )
else( WIN32 )
    set( EXTENSION ".so" )
endif( WIN32 )

# set( CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${ROOT_DIR}/module )

project( core )
get_filename_component( PROJECT_PATH "${CMAKE_CURRENT_SOURCE_DIR}" ABSOLUTE )

file ( GLOB HEADERS
	${PROJECT_PATH}/*.hpp
)

file( GLOB SOURCES
	${PROJECT_PATH}/*.cpp
)

set ( INCLUDES
	${ROOT_DIR}/include
	${EIGEN3_INCLUDE_DIR}
)

set( SOURCES ${HEADERS} ${SOURCES})

include_directories(${INCLUDES})

pybind11_add_module( ${PROJECT_NAME} ${SOURCES} )

# set_target_properties( ${PROJECT_NAME} PROPERTIES DEBUG_POSTFIX d )
# set_target_properties( ${PROJECT_NAME} PROPERTIES LIBRARY_OUTPUT_DIRECTORY_DEBUG   ${ROOT_DIR}/../module/hole_filling_liepa/ )
# set_target_properties( ${PROJECT_NAME} PROPERTIES LIBRARY_OUTPUT_DIRECTORY_RELEASE ${ROOT_DIR}/../module/hole_filling_liepa/ )

add_dependencies( ${PROJECT_NAME} hole_filling_liepa_lib )
target_link_libraries( ${PROJECT_NAME} PRIVATE hole_filling_liepa_lib )

if ( UNIX AND NOT APPLE )
	target_link_libraries( ${PROJECT_NAME} PRIVATE stdc++fs )
endif()
