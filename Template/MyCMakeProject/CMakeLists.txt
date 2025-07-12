cmake_minimum_required(VERSION 3.22)

# Define project variables first
set(PROJECT_NAME "{{PROJECT_NAME}}")
set(PROJECT_VERSION "{{PROJECT_VERSION}}")
set(PLUGIN_MANUFACTURER_CODE "{{PLUGIN_MANUFACTURER_CODE}}")
set(PLUGIN_CODE "{{PLUGIN_CODE}}")
set(PRODUCT_NAME "{{PRODUCT_NAME}}")

# Now declare the project using the variables
project(${PROJECT_NAME} VERSION ${PROJECT_VERSION})

# JUCE location — change this to wherever you cloned JUCE
set(JUCE_DIR "D:/Dev/Visual Studio Projects/JUCE_8.0.8/JUCE")

# Add JUCE
add_subdirectory(${JUCE_DIR} JUCE)

# Your plugin
add_subdirectory(Source)  
