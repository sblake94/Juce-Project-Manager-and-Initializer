cmake_minimum_required(VERSION 3.15)

project(MyPlugin VERSION 0.0.1)

# JUCE location — change this to wherever you cloned JUCE
set(JUCE_DIR "D:/Dev/Visual Studio Projects/JUCE_8.0.8/JUCE")

# Add JUCE
add_subdirectory(${JUCE_DIR} JUCE)

# Your plugin
add_subdirectory(Source)
