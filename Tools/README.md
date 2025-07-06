

# Audio Plugin Project Manager

This is a personal tool for initializing, managing, and visually designing audio plugin projects. It lets you create new JUCE-based plugin projects from templates, then design your plugin's user interface visually and export code for audio frameworks.



## Overview

The Audio Plugin Project Manager is a Python/Tkinter application for:

- Creating new plugin projects from a JUCE/CMake template
- Visually designing plugin interfaces with drag-and-drop components
- Exporting code in multiple formats (JUCE C++, XML, JSON)
- Saving and loading design projects
- Customizing properties of all UI elements in real-time



## Features


### Project Initialization
- Project wizard to start new plugin projects from a template with your chosen name and location
- Automated setup: copies template, renames files, and prepares CMake/JUCE structure
- Guided workflow: prompts you to run CMake and launches the UI Designer automatically


### Visual Design Canvas
- 400x300px default canvas representing your plugin window
- Real-time component rendering
- Drag-and-drop positioning with snap-to-bounds
- Visual selection indicators for active components


### Component Library
- Slider - Horizontal parameter controls with customizable ranges
- Knob - Rotary controls with visual pointer indicators
- Button - Standard push buttons for triggers and toggles
- Toggle Switch - On/off controls with visual state indication
- Label - Text displays for parameter names and values
- TextBox - Input fields for user text entry
- Meter - Level indicators for audio visualization


### Properties Panel
- Position & Size: X/Y coordinates and width/height control
- Text Content: Customizable labels and display text
- Value Ranges: Min/max values and default settings for controls
- Visual Styling: Background colors, text colors, and font sizes
- Real-time Updates: Changes reflect immediately on the canvas


### Code Export System
- JUCE C++: Component initialization code
- Generic XML: Universal layout description format
- JSON: Data exchange and backup format
- Copy to Clipboard: Quick code integration workflow



## Installation & Setup


### Prerequisites
- Python 3.8 or higher
- tkinter (usually included with Python)


### Running the Application
```bash
# Navigate to the Tools directory
cd "d:\Dev\Visual Studio Projects\AudioPlugins\MyAwesomePluginCompany\Tools"

# Launch the Project Manager
python app_project_initializer.py
```

This opens the Project Manager wizard. Use it to create a new plugin project from the template. After project creation and running CMake, the UI Designer will launch for your new project.


## Usage Guide



### Getting Started
1. Launch the Project Manager: Run `app_project_initializer.py`
2. Create a new project: Enter your project name and select a location
3. Run CMake: Follow the prompt to generate your build files
4. Design your UI: The UI Designer will launch for your new project
5. Add components: Click buttons in the left toolbox panel
6. Position elements: Drag components around the canvas
7. Customize properties: Select components to edit in the right panel
8. Export your design: Use File → Export Code when ready

### Component Workflow
1. **Select a component type** from the toolbox (Slider, Knob, Button, etc.)
2. **Click to add** - Component appears in the center of the canvas
3. **Drag to position** - Move components to desired locations
4. **Select and customize** - Click a component to edit its properties
5. **Fine-tune settings** - Use the properties panel for precise control

### Property Editing
- **Text**: Change labels and display names
- **Position**: Set exact X/Y coordinates
- **Size**: Adjust width and height dimensions
- **Value Range**: Set min/max values for controls (sliders, knobs)
- **Default Value**: Set initial parameter values
- **Colors**: Choose background and text colors
- **Font Size**: Adjust text sizing (8-24pt range)

### File Operations
- **New**: Clear the canvas for a fresh design
- **Open**: Load previously saved design files (.json)
- **Save**: Store your current design
- **Save As**: Create new design file copies
- **Export Code**: Generate code in various formats

bypassButton.setBounds(200, 100, 80, 30);


## Code Export Examples

### JUCE C++ Output
```cpp
// JUCE Component Layout
// Add this to your AudioProcessorEditor constructor

// Volume Slider
volumeSlider.setSliderStyle(juce::Slider::LinearHorizontal);
volumeSlider.setRange(0.0, 1.0);
volumeSlider.setValue(0.5);
volumeSlider.setBounds(50, 100, 120, 30);
addAndMakeVisible(volumeSlider);

// Bypass Button
bypassButton.setButtonText("Bypass");
bypassButton.setBounds(200, 100, 80, 30);
addAndMakeVisible(bypassButton);
```

### XML Layout
```xml
<?xml version="1.0" encoding="UTF-8"?>
<gui_layout>
  <canvas width="400" height="300"/>
  <components>
    <component type="slider" id="uuid-here">
      <position x="50" y="100"/>
      <size width="120" height="30"/>
      <text>Volume</text>
      <range min="0.0" max="1.0" default="0.5"/>
    </component>
  </components>
</gui_layout>
```


## Design Best Practices

### Layout Guidelines
- **Group related controls** - Place similar parameters near each other
- **Maintain consistent spacing** - Use the properties panel for precise alignment
- **Consider plugin size constraints** - Most hosts prefer compact interfaces
- **Test different resolutions** - Ensure readability at various sizes

### Component Selection
- **Sliders** - Best for continuous parameters (volume, frequency)
- **Knobs** - Space-efficient for multiple parameters
- **Buttons** - Ideal for on/off functions and triggers
- **Labels** - Essential for parameter identification
- **Meters** - Great for real-time audio feedback


## Keyboard Shortcuts

- `Ctrl+N` - New design
- `Ctrl+O` - Open design file
- `Ctrl+S` - Save current design
- `Ctrl+Shift+S` - Save As new file
- `Right-click` - Context menu (Delete, Duplicate, Properties)
- `Double-click` - Quick properties access


## File Formats

### Design Files (.json)
- **Native format** for saving/loading designs
- **Human-readable** JSON structure
- **Version control friendly** for team collaboration
- **Includes all component properties** and canvas settings

### Export Formats
- **.cpp/.h** - JUCE C++ header and implementation files
- **.xml** - Generic XML layout description
- **.json** - Raw component data for custom parsers
- **.txt** - Plain text for documentation


## Error Handling

The application includes robust error handling for:
- **File I/O operations** - Graceful handling of file access issues
- **Invalid property values** - Automatic validation and correction
- **Component positioning** - Boundary checking and snap-to-canvas
- **Code generation** - Safe string formatting and escaping


## Future Enhancements

- **Custom component templates** - Create reusable component groups
- **Grid snapping and alignment tools** - Precise positioning aids
- **Multiple export targets** - VST3, AU, AAX framework support
- **Theme system** - Custom color schemes and styling
- **Undo/Redo functionality** - Full edit history management
- **Component grouping** - Organize related elements
