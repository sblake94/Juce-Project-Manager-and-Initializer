# Audio Plugin GUI Designer (UIGenerator)

A powerful drag-and-drop visual interface designer for creating audio plugin GUIs. Design your plugin's user interface visually and export production-ready code for popular audio frameworks.

![Audio Plugin GUI Designer](screenshot.png)

## 🎯 Overview

The Audio Plugin GUI Designer is a desktop application built with Python and Tkinter that allows audio plugin developers to:

- **Visually design** plugin interfaces with drag-and-drop components
- **Export code** in multiple formats (JUCE C++, XML, JSON)
- **Save and load** design projects for iterative development
- **Customize properties** of all UI elements in real-time

## 🚀 Features

### Visual Design Canvas
- **400x300px default canvas** representing your plugin window
- **Real-time component rendering** with accurate visual representations
- **Drag-and-drop positioning** with snap-to-bounds functionality
- **Visual selection indicators** for active components

### Component Library
- **Slider** - Horizontal parameter controls with customizable ranges
- **Knob** - Rotary controls with visual pointer indicators
- **Button** - Standard push buttons for triggers and toggles
- **Toggle Switch** - On/off controls with visual state indication
- **Label** - Text displays for parameter names and values
- **TextBox** - Input fields for user text entry
- **Meter** - Level indicators for audio visualization

### Properties Panel
- **Position & Size**: Precise X/Y coordinates and width/height control
- **Text Content**: Customizable labels and display text
- **Value Ranges**: Min/max values and default settings for controls
- **Visual Styling**: Background colors, text colors, and font sizes
- **Real-time Updates**: Changes reflect immediately on the canvas

### Code Export System
- **JUCE C++**: Ready-to-use component initialization code
- **Generic XML**: Universal layout description format
- **JSON**: Data exchange and backup format
- **Copy to Clipboard**: Quick code integration workflow

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.8 or higher
- tkinter (usually included with Python)

### Running the Application
```bash
# Navigate to the Tools directory
cd "d:\Dev\Visual Studio Projects\AudioPlugins\MyAwesomePluginCompany\Tools"

# Run the GUI Designer
python UIGenerator.py
```

## 📖 Usage Guide

### Getting Started
1. **Launch the application** - Run `UIGenerator.py`
2. **Add components** - Click buttons in the left toolbox panel
3. **Position elements** - Drag components around the canvas
4. **Customize properties** - Select components to edit in the right panel
5. **Export your design** - Use File → Export Code when ready

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

## 💻 Code Export Examples

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

## 🎨 Design Best Practices

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

## 🔧 Keyboard Shortcuts

- `Ctrl+N` - New design
- `Ctrl+O` - Open design file
- `Ctrl+S` - Save current design
- `Ctrl+Shift+S` - Save As new file
- `Right-click` - Context menu (Delete, Duplicate, Properties)
- `Double-click` - Quick properties access

## 📁 File Formats

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

## 🛡️ Error Handling

The application includes robust error handling for:
- **File I/O operations** - Graceful handling of file access issues
- **Invalid property values** - Automatic validation and correction
- **Component positioning** - Boundary checking and snap-to-canvas
- **Code generation** - Safe string formatting and escaping

## 🔮 Future Enhancements

- **Custom component templates** - Create reusable component groups
- **Grid snapping and alignment tools** - Precise positioning aids
- **Multiple export targets** - VST3, AU, AAX framework support
- **Theme system** - Custom color schemes and styling
- **Undo/Redo functionality** - Full edit history management
- **Component grouping** - Organize related elements

## 🤝 Contributing

This tool is part of the MyAwesomePluginCompany audio development toolkit. Contributions and feature requests are welcome!

## 📜 License

Part of the MyAwesomePluginCompany audio plugin development suite.

---

**Built for audio developers, by audio developers** 🎵