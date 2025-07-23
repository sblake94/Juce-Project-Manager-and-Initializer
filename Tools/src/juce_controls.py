#!/usr/bin/env python3
"""
JUCE Controls System
Defines common JUCE audio plugin controls and generates corresponding C++ code
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict, field
import json

@dataclass
class JUCEControl:
    """Base class for JUCE controls"""
    name: str
    x: int
    y: int
    width: int
    height: int
    control_type: str
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'JUCEControl':
        """Create from dictionary"""
        return cls(**data)

@dataclass
class JUCESlider(JUCEControl):
    """JUCE Slider control"""
    min_value: float = 0.0
    max_value: float = 1.0
    default_value: float = 0.5
    step_size: float = 0.01
    slider_style: str = "LinearHorizontal"  # LinearHorizontal, LinearVertical, Rotary
    text_box_style: str = "TextBoxBelow"    # TextBoxBelow, TextBoxAbove, TextBoxLeft, TextBoxRight, NoTextBox
    suffix: str = ""
    parameter_id: str = ""
    
    def __post_init__(self):
        self.control_type = "slider"
        if not self.parameter_id:
            self.parameter_id = f"{self.name.lower()}_param"

@dataclass
class JUCEButton(JUCEControl):
    """JUCE Button control"""
    button_text: str = "Button"
    button_type: str = "TextButton"  # TextButton, ToggleButton, ImageButton
    toggle_state: bool = False
    parameter_id: str = ""
    
    def __post_init__(self):
        self.control_type = "button"
        if not self.parameter_id:
            self.parameter_id = f"{self.name.lower()}_param"

@dataclass
class JUCELabel(JUCEControl):
    """JUCE Label control"""
    text: str = "Label"
    font_size: float = 14.0
    justification: str = "centred"  # left, right, centred, centredLeft, centredRight, centredTop, centredBottom
    editable: bool = False
    
    def __post_init__(self):
        self.control_type = "label"

@dataclass
class JUCEComboBox(JUCEControl):
    """JUCE ComboBox control"""
    items: List[str] = field(default_factory=lambda: ["Option 1", "Option 2", "Option 3"])
    default_index: int = 0
    parameter_id: str = ""
    
    def __post_init__(self):
        self.control_type = "combobox"
        if not self.parameter_id:
            self.parameter_id = f"{self.name.lower()}_param"

class JUCEControlFactory:
    """Factory for creating JUCE controls"""
    
    @staticmethod
    def create_control(control_type: str, name: str, x: int, y: int, width: int, height: int, **kwargs) -> JUCEControl:
        """Create a JUCE control of the specified type"""
        if control_type == "slider":
            return JUCESlider(name=name, x=x, y=y, width=width, height=height, **kwargs)
        elif control_type == "button":
            return JUCEButton(name=name, x=x, y=y, width=width, height=height, **kwargs)
        elif control_type == "label":
            return JUCELabel(name=name, x=x, y=y, width=width, height=height, **kwargs)
        elif control_type == "combobox":
            return JUCEComboBox(name=name, x=x, y=y, width=width, height=height, **kwargs)
        else:
            raise ValueError(f"Unknown control type: {control_type}")
    
    @staticmethod
    def get_available_types() -> List[str]:
        """Get list of available control types"""
        return ["slider", "button", "label", "combobox"]
    
    @staticmethod
    def get_default_size(control_type: str) -> tuple[int, int]:
        """Get default width and height for control type"""
        defaults = {
            "slider": (200, 50),
            "button": (80, 30),
            "label": (100, 20),
            "combobox": (120, 25)
        }
        return defaults.get(control_type, (100, 30))

class JUCECodeGenerator:
    """Generates JUCE C++ code for controls"""
    
    def __init__(self, controls: List[JUCEControl]):
        self.controls = controls
    
    def generate_header_declarations(self) -> str:
        """Generate header file declarations for controls"""
        code = []
        code.append("    // GUI Components")
        
        for control in self.controls:
            if isinstance(control, JUCESlider):
                code.append(f"    juce::Slider {control.name}Slider;")
                code.append(f"    juce::Label {control.name}Label;")
            elif isinstance(control, JUCEButton):
                if control.button_type == "ToggleButton":
                    code.append(f"    juce::ToggleButton {control.name}Button;")
                else:
                    code.append(f"    juce::TextButton {control.name}Button;")
            elif isinstance(control, JUCELabel):
                code.append(f"    juce::Label {control.name}Label;")
            elif isinstance(control, JUCEComboBox):
                code.append(f"    juce::ComboBox {control.name}ComboBox;")
                code.append(f"    juce::Label {control.name}Label;")
        
        # Add parameter attachments for controls that need them
        params_controls = [c for c in self.controls if hasattr(c, 'parameter_id') and getattr(c, 'parameter_id', '')]
        if params_controls:
            code.append("")
            code.append("    // Parameter Attachments")
            for control in params_controls:
                if isinstance(control, JUCESlider):
                    code.append(f"    std::unique_ptr<juce::AudioProcessorValueTreeState::SliderAttachment> {control.name}Attachment;")
                elif isinstance(control, JUCEButton):
                    code.append(f"    std::unique_ptr<juce::AudioProcessorValueTreeState::ButtonAttachment> {control.name}Attachment;")
                elif isinstance(control, JUCEComboBox):
                    code.append(f"    std::unique_ptr<juce::AudioProcessorValueTreeState::ComboBoxAttachment> {control.name}Attachment;")
        
        return "\n".join(code)
    
    def generate_constructor_code(self) -> str:
        """Generate constructor initialization code"""
        code = []
        code.append("    // Initialize GUI Components")
        
        for control in self.controls:
            if isinstance(control, JUCESlider):
                code.extend(self._generate_slider_constructor(control))
            elif isinstance(control, JUCEButton):
                code.extend(self._generate_button_constructor(control))
            elif isinstance(control, JUCELabel):
                code.extend(self._generate_label_constructor(control))
            elif isinstance(control, JUCEComboBox):
                code.extend(self._generate_combobox_constructor(control))
        
        return "\n".join(code)
    
    def generate_resized_code(self) -> str:
        """Generate resized() method code for positioning"""
        code = []
        code.append("    // Position GUI Components")
        
        for control in self.controls:
            if isinstance(control, JUCESlider):
                code.append(f"    {control.name}Slider.setBounds({control.x}, {control.y}, {control.width}, {control.height});")
                # Position label above slider
                code.append(f"    {control.name}Label.setBounds({control.x}, {control.y - 25}, {control.width}, 20);")
            elif isinstance(control, JUCEButton):
                code.append(f"    {control.name}Button.setBounds({control.x}, {control.y}, {control.width}, {control.height});")
            elif isinstance(control, JUCELabel):
                code.append(f"    {control.name}Label.setBounds({control.x}, {control.y}, {control.width}, {control.height});")
            elif isinstance(control, JUCEComboBox):
                code.append(f"    {control.name}Label.setBounds({control.x}, {control.y - 25}, {control.width}, 20);")
                code.append(f"    {control.name}ComboBox.setBounds({control.x}, {control.y}, {control.width}, {control.height});")
        
        return "\n".join(code)
    
    def generate_parameter_layout(self) -> str:
        """Generate AudioProcessorValueTreeState parameter layout"""
        code = []
        params_controls = [c for c in self.controls if hasattr(c, 'parameter_id') and getattr(c, 'parameter_id', '')]
        
        if not params_controls:
            return ""
        
        code.append("    // Parameter Layout for JUCE Controls")
        code.append("    layout.add(std::make_unique<juce::AudioParameterFloat>(")
        
        for i, control in enumerate(params_controls):
            if isinstance(control, JUCESlider):
                code.append(f'        "{control.parameter_id}",')
                code.append(f'        "{control.name}",')
                code.append(f'        juce::NormalisableRange<float>({control.min_value}f, {control.max_value}f, {control.step_size}f),')
                code.append(f'        {control.default_value}f));')
            elif isinstance(control, JUCEButton) and control.button_type == "ToggleButton":
                code.append(f'        "{control.parameter_id}",')
                code.append(f'        "{control.name}",')
                code.append(f'        {str(control.toggle_state).lower()}));')
            elif isinstance(control, JUCEComboBox):
                items_str = ', '.join([f'"{item}"' for item in control.items])
                code.append(f'        "{control.parameter_id}",')
                code.append(f'        "{control.name}",')
                code.append(f'        juce::StringArray{{{items_str}}},')
                code.append(f'        {control.default_index}));')
            
            if i < len(params_controls) - 1:
                code.append("")
                code.append("    layout.add(std::make_unique<juce::AudioParameterFloat>(")
        
        return "\n".join(code)
    
    def _generate_slider_constructor(self, slider: JUCESlider) -> List[str]:
        """Generate constructor code for a slider"""
        code = []
        
        # Slider setup
        code.append(f"    {slider.name}Slider.setSliderStyle(juce::Slider::{slider.slider_style});")
        code.append(f"    {slider.name}Slider.setRange({slider.min_value}, {slider.max_value}, {slider.step_size});")
        code.append(f"    {slider.name}Slider.setValue({slider.default_value});")
        code.append(f"    {slider.name}Slider.setTextBoxStyle(juce::Slider::{slider.text_box_style}, false, 70, 20);")
        if slider.suffix:
            code.append(f"    {slider.name}Slider.setTextValueSuffix(\"{slider.suffix}\");")
        code.append(f"    addAndMakeVisible({slider.name}Slider);")
        
        # Label setup
        code.append(f"    {slider.name}Label.setText(\"{slider.name}\", juce::dontSendNotification);")
        code.append(f"    {slider.name}Label.setJustificationType(juce::Justification::centred);")
        code.append(f"    addAndMakeVisible({slider.name}Label);")
        
        # Parameter attachment
        if slider.parameter_id:
            code.append(f"    {slider.name}Attachment = std::make_unique<juce::AudioProcessorValueTreeState::SliderAttachment>(parameters, \"{slider.parameter_id}\", {slider.name}Slider);")
        
        code.append("")
        return code
    
    def _generate_button_constructor(self, button: JUCEButton) -> List[str]:
        """Generate constructor code for a button"""
        code = []
        
        code.append(f"    {button.name}Button.setButtonText(\"{button.button_text}\");")
        if button.button_type == "ToggleButton":
            code.append(f"    {button.name}Button.setToggleState({str(button.toggle_state).lower()}, juce::dontSendNotification);")
        code.append(f"    addAndMakeVisible({button.name}Button);")
        
        # Parameter attachment
        if button.parameter_id:
            code.append(f"    {button.name}Attachment = std::make_unique<juce::AudioProcessorValueTreeState::ButtonAttachment>(parameters, \"{button.parameter_id}\", {button.name}Button);")
        
        code.append("")
        return code
    
    def _generate_label_constructor(self, label: JUCELabel) -> List[str]:
        """Generate constructor code for a label"""
        code = []
        
        code.append(f"    {label.name}Label.setText(\"{label.text}\", juce::dontSendNotification);")
        code.append(f"    {label.name}Label.setJustificationType(juce::Justification::{label.justification});")
        code.append(f"    {label.name}Label.setFont(juce::Font({label.font_size}f));")
        if label.editable:
            code.append(f"    {label.name}Label.setEditable(true);")
        code.append(f"    addAndMakeVisible({label.name}Label);")
        code.append("")
        return code
    
    def _generate_combobox_constructor(self, combobox: JUCEComboBox) -> List[str]:
        """Generate constructor code for a combobox"""
        code = []
        
        # ComboBox setup
        for i, item in enumerate(combobox.items, 1):
            code.append(f"    {combobox.name}ComboBox.addItem(\"{item}\", {i});")
        code.append(f"    {combobox.name}ComboBox.setSelectedItemIndex({combobox.default_index});")
        code.append(f"    addAndMakeVisible({combobox.name}ComboBox);")
        
        # Label setup
        code.append(f"    {combobox.name}Label.setText(\"{combobox.name}\", juce::dontSendNotification);")
        code.append(f"    {combobox.name}Label.setJustificationType(juce::Justification::centred);")
        code.append(f"    addAndMakeVisible({combobox.name}Label);")
        
        # Parameter attachment
        if combobox.parameter_id:
            code.append(f"    {combobox.name}Attachment = std::make_unique<juce::AudioProcessorValueTreeState::ComboBoxAttachment>(parameters, \"{combobox.parameter_id}\", {combobox.name}ComboBox);")
        
        code.append("")
        return code

# Predefined common audio plugin controls
COMMON_AUDIO_CONTROLS = {
    "gain_slider": {
        "type": "slider",
        "name": "Gain",
        "min_value": -60.0,
        "max_value": 12.0,
        "default_value": 0.0,
        "step_size": 0.1,
        "suffix": " dB",
        "slider_style": "LinearVertical",
        "width": 60,
        "height": 120
    },
    "frequency_slider": {
        "type": "slider", 
        "name": "Frequency",
        "min_value": 20.0,
        "max_value": 20000.0,
        "default_value": 1000.0,
        "step_size": 1.0,
        "suffix": " Hz",
        "slider_style": "Rotary",
        "width": 80,
        "height": 80
    },
    "bypass_button": {
        "type": "button",
        "name": "Bypass",
        "button_text": "Bypass",
        "button_type": "ToggleButton",
        "toggle_state": False,
        "width": 80,
        "height": 30
    },
    "drive_slider": {
        "type": "slider",
        "name": "Drive", 
        "min_value": 1.0,
        "max_value": 10.0,
        "default_value": 1.0,
        "step_size": 0.1,
        "slider_style": "Rotary",
        "width": 80,
        "height": 80
    }
}
