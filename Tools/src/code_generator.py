#!/usr/bin/env python3
"""
Code generation utilities for exporting GUI designs
"""

import json
from typing import Dict, List
from dataclasses import asdict, dataclass
from .components.component import Component
from .components.HorizontalSlider import HorizontalSlider
from .components.VerticalSlider import VerticalSlider
from .components.Knob import Knob
from .components.Button import Button
from .components.Label import Label
from .components.Toggle import Toggle
from .components.TextBox import TextBox
from .components.Meter import Meter
from .JUCECodeSections import JUCECodeSections
from .JUCECodeOutput import JUCECodeOutput 

class CodeGenerator:
    """Handles code generation in various formats"""

    def __init__(self, components: Dict[str, Component], canvas_width: int, canvas_height: int, background_color: str = "#DDDDDD"):
        self.components = components
        self.canvas_width = canvas_width
        self.canvas_height = canvas_height
        self.background_color = background_color

    def generate_juce_code(self) -> JUCECodeOutput:
        """Generate complete JUCE C++ code for editor and processor"""
        sections = JUCECodeSections()
        
        for comp in self.components.values():
            comp_name = comp.text.replace(" ", "").lower()
            if not comp_name:  # Fallback if text is empty
                comp_name = f"{comp.type}_{comp.id}"
            if isinstance(comp, HorizontalSlider):
                self._generate_juce_horizontal_slider(comp, comp_name, sections)
            elif isinstance(comp, VerticalSlider):
                self._generate_juce_vertical_slider(comp, comp_name, sections)
            elif isinstance(comp, Knob):
                self._generate_juce_knob(comp, comp_name, sections)
            elif isinstance(comp, Button):
                self._generate_juce_button(comp, comp_name, sections)
            elif isinstance(comp, Label):
                self._generate_juce_label(comp, comp_name, sections)
            elif isinstance(comp, Toggle):
                self._generate_juce_toggle(comp, comp_name, sections)
            elif isinstance(comp, TextBox):
                self._generate_juce_textbox(comp, comp_name, sections)
            elif isinstance(comp, Meter):
                self._generate_juce_meter(comp, comp_name, sections)
        

        # Add canvas size to the editor constructor code
        sections.editor_constructor_code += f"    // Set the size of the editor\n"
        sections.editor_constructor_code += f"    setSize({self.canvas_width}, {self.canvas_height});\n\n"

        # Generate paint, resized, and parameter layout methods
        sections.editor_paint_code = self._generate_editor_paint_method()
        sections.editor_resized_code = self._generate_editor_resized_method()
        sections.processor_parameter_layout_code = self._generate_parameter_layout()

        # Return structured output
        return JUCECodeOutput(JUCECodeSections(
            editor_header_declarations=sections.editor_header_declarations,
            editor_constructor_code=sections.editor_constructor_code,
            editor_paint_code=sections.editor_paint_code,
            editor_resized_code=sections.editor_resized_code,
            processor_header_declarations=sections.processor_header_declarations,
            processor_constructor_code=sections.processor_constructor_code,
            processor_parameter_layout_code=sections.processor_parameter_layout_code
        ))
    

    def _generate_juce_horizontal_slider(self, hslider: HorizontalSlider, hslider_name: str, sections: JUCECodeSections):
        """Generate JUCE horizontal slider code for all sections"""
        # Editor header declarations
        sections.editor_header_declarations += f"    std::unique_ptr<juce::Slider> {hslider_name}Slider;\n"
        sections.editor_header_declarations += f"    std::unique_ptr<juce::AudioProcessorValueTreeState::SliderAttachment> {hslider_name}SliderAttachment;\n\n"

        # Editor constructor code
        sections.editor_constructor_code += f"    // {hslider.text} Horizontal Slider\n"
        sections.editor_constructor_code += f"    {hslider_name}Slider = std::make_unique<juce::Slider>();\n"
        sections.editor_constructor_code += f"    {hslider_name}Slider->setSliderStyle(juce::Slider::LinearHorizontal);\n"
        sections.editor_constructor_code += f"    {hslider_name}Slider->setRange({hslider.min_value}, {hslider.max_value});\n"
        sections.editor_constructor_code += f"    {hslider_name}Slider->setValue({hslider.default_value});\n"
        sections.editor_constructor_code += f"    {hslider_name}Slider->setBounds({hslider.x}, {hslider.y}, {hslider.width}, {hslider.height});\n"
        sections.editor_constructor_code += f"    {hslider_name}Slider->setTextBoxStyle(juce::Slider::NoTextBox, false, 0, 0);\n"
        sections.editor_constructor_code += f"    {hslider_name}Slider->setPopupDisplayEnabled(true, true, this);\n"
        sections.editor_constructor_code += f"    addAndMakeVisible(*{hslider_name}Slider);\n"
        sections.editor_constructor_code += f"    {hslider_name}SliderAttachment = std::make_unique<juce::AudioProcessorValueTreeState::SliderAttachment>(audioProcessor.getValueTreeState(), \"{hslider_name.upper()}\", *{hslider_name}Slider);\n\n"

        # Editor paint method
        sections.editor_paint_code += f"    // {hslider.text} Horizontal Slider Paint\n"
        sections.editor_paint_code += f"    g.setColour(juce::Colours::lightgrey);\n"
        sections.editor_paint_code += f"    g.fillRect({hslider.x}, {hslider.y}, {hslider.width}, {hslider.height});\n"
        sections.editor_paint_code += f"    g.setColour(juce::Colours::black);\n"
        sections.editor_paint_code += f"    g.drawRect({hslider.x}, {hslider.y}, {hslider.width}, {hslider.height});\n\n"

        # Editor resized method
        sections.editor_resized_code += f"    // {hslider.text} Horizontal Slider Resized\n"
        sections.editor_resized_code += f"    {hslider_name}Slider->setBounds({hslider.x}, {hslider.y}, {hslider.width}, {hslider.height});\n\n"

        # Processor header declarations
        sections.processor_header_declarations += f"    // {hslider.text} parameter\n"
        sections.processor_header_declarations += f"    juce::AudioParameterFloat* {hslider_name}Parameter;\n\n"

        # Processor constructor code
        sections.processor_constructor_code += f"    // {hslider.text} Parameter\n"
        sections.processor_constructor_code += f"    {hslider_name}Parameter = dynamic_cast<juce::AudioParameterFloat*>(\n"
        sections.processor_constructor_code += f"        getValueTreeState().getParameter(\"{hslider_name.upper()}\"));\n\n"

    def _generate_juce_vertical_slider(self, vslider: VerticalSlider, vslider_name: str, sections: JUCECodeSections):
        """Generate JUCE vertical slider code for all sections"""
        # Editor header declarations
        sections.editor_header_declarations += f"    std::unique_ptr<juce::Slider> {vslider_name}Slider;\n"
        sections.editor_header_declarations += f"    std::unique_ptr<juce::AudioProcessorValueTreeState::SliderAttachment> {vslider_name}SliderAttachment;\n\n"

        # Editor constructor code
        sections.editor_constructor_code += f"    // {vslider.text} Vertical Slider\n"
        sections.editor_constructor_code += f"    {vslider_name}Slider = std::make_unique<juce::Slider>();\n"
        sections.editor_constructor_code += f"    {vslider_name}Slider->setSliderStyle(juce::Slider::LinearVertical);\n"
        sections.editor_constructor_code += f"    {vslider_name}Slider->setRange({vslider.min_value}, {vslider.max_value});\n"
        sections.editor_constructor_code += f"    {vslider_name}Slider->setValue({vslider.default_value});\n"
        sections.editor_constructor_code += f"    {vslider_name}Slider->setBounds({vslider.x}, {vslider.y}, {vslider.width}, {vslider.height});\n"
        sections.editor_constructor_code += f"    {vslider_name}Slider->setTextBoxStyle(juce::Slider::NoTextBox, false, 0, 0);\n"
        sections.editor_constructor_code += f"    {vslider_name}Slider->setPopupDisplayEnabled(true, true, this);\n"
        sections.editor_constructor_code += f"    addAndMakeVisible(*{vslider_name}Slider);\n"
        sections.editor_constructor_code += f"    {vslider_name}SliderAttachment = std::make_unique<juce::AudioProcessorValueTreeState::SliderAttachment>(audioProcessor.getValueTreeState(), \"{vslider_name.upper()}\", *{vslider_name}Slider);\n\n"

        # Editor paint method
        sections.editor_paint_code += f"    // {vslider.text} Vertical Slider Paint\n"
        sections.editor_paint_code += f"    g.setColour(juce::Colours::lightgrey);\n"
        sections.editor_paint_code += f"    g.fillRect({vslider.x}, {vslider.y}, {vslider.width}, {vslider.height});\n"
        sections.editor_paint_code += f"    g.setColour(juce::Colours::black);\n"
        sections.editor_paint_code += f"    g.drawRect({vslider.x}, {vslider.y}, {vslider.width}, {vslider.height});\n\n"

        # Editor resized method
        sections.editor_resized_code += f"    // {vslider.text} Vertical Slider Resized\n"
        sections.editor_resized_code += f"    {vslider_name}Slider->setBounds({vslider.x}, {vslider.y}, {vslider.width}, {vslider.height});\n\n"

        # Processor header declarations
        sections.processor_header_declarations += f"    // {vslider.text} parameter\n"
        sections.processor_header_declarations += f"    juce::AudioParameterFloat* {vslider_name}Parameter;\n\n"

        # Processor constructor code
        sections.processor_constructor_code += f"    // {vslider.text} Parameter\n"
        sections.processor_constructor_code += f"    {vslider_name}Parameter = dynamic_cast<juce::AudioParameterFloat*>(\n"
        sections.processor_constructor_code += f"        getValueTreeState().getParameter(\"{vslider_name.upper()}\"));\n\n"

    def _generate_juce_knob(self, knob: Knob, knob_name: str, sections: JUCECodeSections):
        """Generate JUCE knob code for all sections"""
        # Editor header declarations
        sections.editor_header_declarations += f"    std::unique_ptr<juce::Slider> {knob_name}Slider;\n"
        sections.editor_header_declarations += f"    std::unique_ptr<juce::AudioProcessorValueTreeState::SliderAttachment> {knob_name}SliderAttachment;\n\n"

        # Editor constructor code
        sections.editor_constructor_code += f"    // {knob.text} Knob\n"
        sections.editor_constructor_code += f"    {knob_name}Slider = std::make_unique<juce::Slider>();\n"
        sections.editor_constructor_code += f"    {knob_name}Slider->setSliderStyle(juce::Slider::RotaryHorizontalVerticalDrag);\n"
        sections.editor_constructor_code += f"    {knob_name}Slider->setRange({knob.min_value}, {knob.max_value});\n"
        sections.editor_constructor_code += f"    {knob_name}Slider->setValue({knob.default_value});\n"
        sections.editor_constructor_code += f"    {knob_name}Slider->setBounds({knob.x}, {knob.y}, {knob.width}, {knob.height});\n"
        sections.editor_constructor_code += f"    {knob_name}Slider->setTextBoxStyle(juce::Slider::TextBoxBelow, false, 0, 0);\n"
        sections.editor_constructor_code += f"    {knob_name}Slider->setPopupDisplayEnabled(true, true, this);\n"
        sections.editor_constructor_code += f"    addAndMakeVisible(*{knob_name}Slider);\n"
        sections.editor_constructor_code += f"    {knob_name}SliderAttachment = std::make_unique<juce::AudioProcessorValueTreeState::SliderAttachment>(audioProcessor.getValueTreeState(), \"{knob_name.upper()}\", *{knob_name}Slider);\n\n"

        # Editor paint method
        sections.editor_paint_code += f"    // {knob.text} Knob Paint\n"
        sections.editor_paint_code += f"    g.setColour(juce::Colours::lightgrey);\n"
        sections.editor_paint_code += f"    g.fillRect({knob.x}, {knob.y}, {knob.width}, {knob.height});\n"
        sections.editor_paint_code += f"    g.setColour(juce::Colours::black);\n"
        sections.editor_paint_code += f"    g.drawRect({knob.x}, {knob.y}, {knob.width}, {knob.height});\n\n"

        # Editor resized method
        sections.editor_resized_code += f"    // {knob.text} Knob Resized\n"
        sections.editor_resized_code += f"    {knob_name}Slider->setBounds({knob.x}, {knob.y}, {knob.width}, {knob.height});\n\n"

        # Processor header declarations
        sections.processor_header_declarations += f"    // {knob.text} parameter\n"
        sections.processor_header_declarations += f"    juce::AudioParameterFloat* {knob_name}Parameter;\n\n"

        # Processor constructor code
        sections.processor_constructor_code += f"    // {knob.text} Parameter\n"
        sections.processor_constructor_code += f"    {knob_name}Parameter = dynamic_cast<juce::AudioParameterFloat*>(\n"
        sections.processor_constructor_code += f"        getValueTreeState().getParameter(\"{knob_name.upper()}\"));\n\n"

    def _generate_juce_button(self, button: Button, button_name: str, sections: JUCECodeSections):
        """Generate JUCE button code for all sections"""
        # Editor header declarations
        sections.editor_header_declarations += f"    std::unique_ptr<juce::TextButton> {button_name}Button;\n"
        sections.editor_header_declarations += f"    std::unique_ptr<juce::AudioProcessorValueTreeState::ButtonAttachment> {button_name}ButtonAttachment;\n\n"

        # Editor constructor code
        sections.editor_constructor_code += f"    // {button.text} Button\n"
        sections.editor_constructor_code += f"    {button_name}Button = std::make_unique<juce::TextButton>();\n"
        sections.editor_constructor_code += f"    {button_name}Button->setButtonText(\"{button.text}\");\n"
        sections.editor_constructor_code += f"    {button_name}Button->setBounds({button.x}, {button.y}, {button.width}, {button.height});\n"
        sections.editor_constructor_code += f"    {button_name}Button->setColour(juce::TextButton::buttonColourId, juce::Colours::lightgrey);\n"
        sections.editor_constructor_code += f"    {button_name}Button->setColour(juce::TextButton::textColourOffId, juce::Colours::black);\n"
        sections.editor_constructor_code += f"    addAndMakeVisible(*{button_name}Button);\n"
        sections.editor_constructor_code += f"    {button_name}ButtonAttachment = std::make_unique<juce::AudioProcessorValueTreeState::ButtonAttachment>(audioProcessor.getValueTreeState(), \"{button_name.upper()}\", *{button_name}Button);\n\n"

        # Editor paint method
        sections.editor_paint_code += f"    // {button.text} Button Paint\n"
        sections.editor_paint_code += f"    g.setColour(juce::Colours::lightgrey);\n"
        sections.editor_paint_code += f"    g.fillRect({button.x}, {button.y}, {button.width}, {button.height});\n"
        sections.editor_paint_code += f"    g.setColour(juce::Colours::black);\n"
        sections.editor_paint_code += f"    g.drawRect({button.x}, {button.y}, {button.width}, {button.height});\n\n"

        # Editor resized method
        sections.editor_resized_code += f"    // {button.text} Button Resized\n"
        sections.editor_resized_code += f"    {button_name}Button->setBounds({button.x}, {button.y}, {button.width}, {button.height});\n\n"

        # Processor header declarations
        sections.processor_header_declarations += f"    // {button.text} parameter\n"
        sections.processor_header_declarations += f"    juce::AudioParameterBool* {button_name}Parameter;\n\n"

        # Processor constructor code
        sections.processor_constructor_code += f"    // {button.text} Parameter\n"
        sections.processor_constructor_code += f"    {button_name}Parameter = dynamic_cast<juce::AudioParameterBool*>(\n"
        sections.processor_constructor_code += f"        getValueTreeState().getParameter(\"{button_name.upper()}\"));\n\n"

    def _generate_juce_toggle(self, toggle: Toggle, toggle_name: str, sections: JUCECodeSections):
        """Generate JUCE toggle button code for all sections"""
        # Editor header declarations
        sections.editor_header_declarations += f"    std::unique_ptr<juce::ToggleButton> {toggle_name}Toggle;\n"
        sections.editor_header_declarations += f"    std::unique_ptr<juce::AudioProcessorValueTreeState::ButtonAttachment> {toggle_name}ToggleAttachment;\n\n"

        # Editor constructor code
        sections.editor_constructor_code += f"    // {toggle.text} Toggle\n"
        sections.editor_constructor_code += f"    {toggle_name}Toggle = std::make_unique<juce::ToggleButton>();\n"
        sections.editor_constructor_code += f"    {toggle_name}Toggle->setButtonText(\"{toggle.text}\");\n"
        sections.editor_constructor_code += f"    {toggle_name}Toggle->setBounds({toggle.x}, {toggle.y}, {toggle.width}, {toggle.height});\n"
        sections.editor_constructor_code += f"    {toggle_name}Toggle->setColour(juce::ToggleButton::textColourId, juce::Colours::black);\n"
        sections.editor_constructor_code += f"    addAndMakeVisible(*{toggle_name}Toggle);\n"
        sections.editor_constructor_code += f"    {toggle_name}ToggleAttachment = std::make_unique<juce::AudioProcessorValueTreeState::ButtonAttachment>(audioProcessor.getValueTreeState(), \"{toggle_name.upper()}\", *{toggle_name}Toggle);\n\n"

        # Editor paint method
        sections.editor_paint_code += f"    // {toggle.text} Toggle Paint\n"
        sections.editor_paint_code += f"    g.setColour(juce::Colours::lightgrey);\n"
        sections.editor_paint_code += f"    g.fillRect({toggle.x}, {toggle.y}, {toggle.width}, {toggle.height});\n"
        sections.editor_paint_code += f"    g.setColour(juce::Colours::black);\n"
        sections.editor_paint_code += f"    g.drawRect({toggle.x}, {toggle.y}, {toggle.width}, {toggle.height});\n\n"

        # Editor resized method
        sections.editor_resized_code += f"    // {toggle.text} Toggle Resized\n"
        sections.editor_resized_code += f"    {toggle_name}Toggle->setBounds({toggle.x}, {toggle.y}, {toggle.width}, {toggle.height});\n\n"

        # Processor header declarations
        sections.processor_header_declarations += f"    // {toggle.text} parameter\n"
        sections.processor_header_declarations += f"    juce::AudioParameterBool* {toggle_name}Parameter;\n\n"

        # Processor constructor code
        sections.processor_constructor_code += f"    // {toggle.text} Parameter\n"
        sections.processor_constructor_code += f"    {toggle_name}Parameter = dynamic_cast<juce::AudioParameterBool*>(\n"
        sections.processor_constructor_code += f"        getValueTreeState().getParameter(\"{toggle_name.upper()}\"));\n\n"


    def _generate_juce_label(self, label: Label, label_name: str, sections: JUCECodeSections):
        """Generate JUCE label code for all sections with consistent styling"""
        # Editor header declarations
        sections.editor_header_declarations += f"    std::unique_ptr<juce::Label> {label_name}Label;\n\n"

        # Editor constructor code
        sections.editor_constructor_code += f"    // {label.text} Label\n"
        sections.editor_constructor_code += f"    {label_name}Label = std::make_unique<juce::Label>();\n"
        sections.editor_constructor_code += f"    {label_name}Label->setText(\"{getattr(label, 'displayed_text', label.text)}\", juce::dontSendNotification);\n"
        sections.editor_constructor_code += f"    {label_name}Label->setJustificationType(juce::Justification::centred);\n"
        sections.editor_constructor_code += f"    {label_name}Label->setFont(juce::Font({getattr(label, 'font_size', 14.0)}.0f));\n"
        sections.editor_constructor_code += f"    {label_name}Label->setColour(juce::Label::textColourId, juce::Colours::black);\n"
        sections.editor_constructor_code += f"    {label_name}Label->setBounds({label.x}, {label.y}, {label.width}, {label.height});\n"
        sections.editor_constructor_code += f"    addAndMakeVisible(*{label_name}Label);\n\n"

        # Editor paint method
        sections.editor_paint_code += f"    // {label.text} Label Paint\n"
        sections.editor_paint_code += f"    g.setColour(juce::Colours::lightgrey);\n"
        sections.editor_paint_code += f"    g.fillRect({label.x}, {label.y}, {label.width}, {label.height});\n"
        sections.editor_paint_code += f"    g.setColour(juce::Colours::black);\n"
        sections.editor_paint_code += f"    g.drawRect({label.x}, {label.y}, {label.width}, {label.height});\n\n"

        # Editor resized method
        sections.editor_resized_code += f"    // {label.text} Label Resized\n"
        sections.editor_resized_code += f"    {label_name}Label->setBounds({label.x}, {label.y}, {label.width}, {label.height});\n\n"

        # Labels don't typically need processor parameters

    def _generate_juce_textbox(self, txtbox: TextBox, txtbox_name: str, sections: JUCECodeSections):
        """Generate JUCE text editor code for all sections with consistent styling"""
        # Editor header declarations
        sections.editor_header_declarations += f"    std::unique_ptr<juce::TextEditor> {txtbox_name}TextBox;\n\n"

        # Editor constructor code
        sections.editor_constructor_code += f"    // {txtbox.text} TextBox\n"
        sections.editor_constructor_code += f"    {txtbox_name}TextBox = std::make_unique<juce::TextEditor>();\n"
        sections.editor_constructor_code += f"    {txtbox_name}TextBox->setMultiLine(false);\n"
        sections.editor_constructor_code += f"    {txtbox_name}TextBox->setReturnKeyStartsNewLine(false);\n"
        sections.editor_constructor_code += f"    {txtbox_name}TextBox->setReadOnly(false);\n"
        sections.editor_constructor_code += f"    {txtbox_name}TextBox->setScrollbarsShown(true);\n"
        sections.editor_constructor_code += f"    {txtbox_name}TextBox->setCaretVisible(true);\n"
        sections.editor_constructor_code += f"    {txtbox_name}TextBox->setPopupMenuEnabled(true);\n"
        sections.editor_constructor_code += f"    {txtbox_name}TextBox->setText(\"{txtbox.text}\");\n"
        sections.editor_constructor_code += f"    {txtbox_name}TextBox->setFont(juce::Font({getattr(txtbox, 'font_size', 14.0)}.0f));\n"
        sections.editor_constructor_code += f"    {txtbox_name}TextBox->setColour(juce::TextEditor::backgroundColourId, juce::Colours::white);\n"
        sections.editor_constructor_code += f"    {txtbox_name}TextBox->setColour(juce::TextEditor::textColourId, juce::Colours::black);\n"
        sections.editor_constructor_code += f"    {txtbox_name}TextBox->setBounds({txtbox.x}, {txtbox.y}, {txtbox.width}, {txtbox.height});\n"
        sections.editor_constructor_code += f"    addAndMakeVisible(*{txtbox_name}TextBox);\n\n"

        # Editor paint method
        sections.editor_paint_code += f"    // {txtbox.text} TextBox Paint\n"
        sections.editor_paint_code += f"    g.setColour(juce::Colours::lightgrey);\n"
        sections.editor_paint_code += f"    g.fillRect({txtbox.x}, {txtbox.y}, {txtbox.width}, {txtbox.height});\n"
        sections.editor_paint_code += f"    g.setColour(juce::Colours::black);\n"
        sections.editor_paint_code += f"    g.drawRect({txtbox.x}, {txtbox.y}, {txtbox.width}, {txtbox.height});\n\n"

        # Editor resized method
        sections.editor_resized_code += f"    // {txtbox.text} TextBox Resized\n"
        sections.editor_resized_code += f"    {txtbox_name}TextBox->setBounds({txtbox.x}, {txtbox.y}, {txtbox.width}, {txtbox.height});\n\n"

        # TextBoxes don't typically need processor parameters

    def _generate_juce_meter(self, meter: Meter, meter_name: str, sections: JUCECodeSections):
        """Generate JUCE meter code for all sections with consistent styling"""
        # Editor header declarations
        sections.editor_header_declarations += f"    // {meter.text} Meter (custom component)\n"
        sections.editor_header_declarations += f"    juce::Rectangle<int> {meter_name}MeterBounds;\n"
        sections.editor_header_declarations += f"    float {meter_name}MeterLevel = 0.0f;\n\n"

        # Editor constructor code
        sections.editor_constructor_code += f"    // {meter.text} Meter\n"
        sections.editor_constructor_code += f"    {meter_name}MeterBounds = juce::Rectangle<int>({meter.x}, {meter.y}, {meter.width}, {meter.height});\n\n"
        # Add note about custom meter implementation
        sections.editor_constructor_code += f"    // Note: Implement custom meter drawing in paint() method\n"
        sections.editor_constructor_code += f"    // Use {meter_name}MeterBounds and {meter_name}MeterLevel\n\n"

        # Editor paint method
        sections.editor_paint_code += f"    // {meter.text} Meter Paint\n"
        sections.editor_paint_code += f"    g.setColour(juce::Colours::darkgrey);\n"
        sections.editor_paint_code += f"    g.fillRect({meter_name}MeterBounds);\n"
        sections.editor_paint_code += f"    g.setColour(juce::Colours::green);\n"
        sections.editor_paint_code += f"    auto meterHeight = static_cast<int>({meter_name}MeterLevel * {meter_name}MeterBounds.getHeight());\n"
        sections.editor_paint_code += f"    auto meterFillRect = {meter_name}MeterBounds.withTop({meter_name}MeterBounds.getBottom() - meterHeight);\n"
        sections.editor_paint_code += f"    g.fillRect(meterFillRect);\n"
        sections.editor_paint_code += f"    g.setColour(juce::Colours::white);\n"
        sections.editor_paint_code += f"    g.drawRect({meter_name}MeterBounds, 1);\n\n"

        # Editor resized method
        sections.editor_resized_code += f"    // {meter.text} Meter Resized\n"
        sections.editor_resized_code += f"    {meter_name}MeterBounds = juce::Rectangle<int>({meter.x}, {meter.y}, {meter.width}, {meter.height});\n\n"

        # Meters don't typically need processor parameters
        
    def _generate_editor_paint_method(self) -> str:
        """Generate the PluginEditor::paint method code based on components and canvas size"""
        code = ""


        if len(self.background_color) == 6:
            r = int(self.background_color[:2], 16)
            g = int(self.background_color[2:4], 16)
            b = int(self.background_color[4:], 16)
        else:
            r = g = b = 0

        # Background fill
        code += "    // Fill background with gradient\n"
        code += f"    juce::Colour backgroundColour = juce::Colour({r}, {g}, {b});\n"
        code += "    juce::Colour secondaryColour = backgroundColour.darker(0.2f);\n"
        code += "    \n"
        code += "    g.setGradientFill(juce::ColourGradient(\n"
        code += "        backgroundColour,\n"
        code += "        0.0f, 0.0f,\n"
        code += "        secondaryColour,\n"
        code += "        0.0f, static_cast<float>(getHeight()),\n"
        code += "        false));\n"
        code += "    g.fillAll();\n\n"
        
        # Draw border
        code += "    // Draw border\n"
        code += "    g.setColour(juce::Colours::black);\n"
        code += "    g.drawRect(getLocalBounds(), 1);\n\n"
        
        # Handle meter drawing and other custom components
        has_custom_drawing = False
        for comp in self.components.values():
            comp_name = comp.text.replace(" ", "").lower()
            if not comp_name:  # Fallback if text is empty
                comp_name = f"{comp.type}_{comp.id}"
                
            if comp.type == 'meter':
                has_custom_drawing = True
                code += f"    // Draw {comp.text} meter\n"
                code += f"    g.setColour(juce::Colours::green);\n"
                code += f"    auto meterHeight = static_cast<int>({comp_name}MeterLevel * {comp_name}MeterBounds.getHeight());\n"
                code += f"    auto meterFillRect = {comp_name}MeterBounds.withTop({comp_name}MeterBounds.getBottom() - meterHeight);\n"
                code += f"    g.fillRect(meterFillRect);\n"
                code += f"    \n"
                code += f"    // Meter border\n"
                code += f"    g.setColour(juce::Colours::white);\n"
                code += f"    g.drawRect({comp_name}MeterBounds, 1);\n"
                code += f"    \n"
                # Draw tick marks
                code += f"    // Draw tick marks\n"
                code += f"    g.setColour(juce::Colours::white);\n"
                code += f"    int numTicks = 5;\n" 
                code += f"    for (int i = 0; i < numTicks; ++i)\n"
                code += f"    {{\n"
                code += f"        float y = {comp_name}MeterBounds.getY() + (i * {comp_name}MeterBounds.getHeight() / (float)(numTicks - 1));\n"
                code += f"        g.drawLine({comp_name}MeterBounds.getX() - 2, y, {comp_name}MeterBounds.getX(), y, 1.0f);\n"
                code += f"        g.drawLine({comp_name}MeterBounds.getRight(), y, {comp_name}MeterBounds.getRight() + 2, y, 1.0f);\n"
                code += f"    }}\n\n"
        
        # Draw plugin name as a heading
        code += "    // Draw plugin name/title\n" 
        code += "    g.setColour(juce::Colours::white);\n"
        code += "    g.setFont(24.0f);\n"
        code += "    g.drawText(\"My Awesome Plugin\", getLocalBounds().withHeight(20),\n"
        code += "               juce::Justification::centred, true);\n\n"

        # Add placeholder for version number in bottom-right corner
        code += "    // Version number\n"
        code += "    g.setFont(10.0f);\n"
        code += "    g.drawText(\"v1.0.0\", getLocalBounds().reduced(5).removeFromBottom(15),\n"
        code += "               juce::Justification::bottomRight, true);\n"
    
        return code

    def _generate_editor_resized_method(self) -> str:
        """Generate the PluginEditor::resized method code based on components"""
        code = ""
        code += "    // This method is where you should set the bounds of any child\n"
        code += "    // components that your component contains. Component bounds are\n"
        code += "    // already set in the constructor, but you can use this method\n"
        code += "    // for dynamic layouts or resizing behavior.\n"
        
        # If there are no components, just add a comment
        if not self.components:
            code += "    // No components to resize\n"
        else:
            code += "\n    // Example of proportional layout (if you implement UI resizing):\n"
            code += "    // auto area = getLocalBounds();\n"
            code += "    // auto topSection = area.removeFromTop(area.getHeight() * 0.3f);\n"
            code += "    // auto bottomSection = area;\n"
            
            # Add example for the first component found (as demonstration)
            for comp in self.components.values():
                comp_name = comp.text.replace(" ", "").lower()
                if not comp_name:
                    comp_name = f"{comp.type}_{comp.id}"
                
                if comp.type in ['horizontalslider', 'verticalslider', 'knob']:
                    code += f"\n    // Example: Dynamically position {comp.text} slider\n"
                    code += f"    // {comp_name}Slider->setBounds(topSection.removeFromLeft(100).reduced(10));\n"
                    break
                elif comp.type == 'button':
                    code += f"\n    // Example: Dynamically position {comp.text} button\n"
                    code += f"    // {comp_name}Button->setBounds(bottomSection.removeFromLeft(100).reduced(10));\n"
                    break
        
        return code
    
    def generate_json_code(self) -> str:
        """Generate JSON representation"""
        data = {
            'canvas_size': {
                'width': self.canvas_width,
                'height': self.canvas_height
            },
            'components': [asdict(comp) for comp in self.components.values()]
        }
        return json.dumps(data, indent=2)
    
    def generate_xml_code(self) -> str:
        """Generate XML representation"""
        xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
        xml += '<gui_layout>\n'
        xml += f'  <canvas width="{self.canvas_width}" height="{self.canvas_height}"/>\n'
        xml += '  <components>\n'
        
        for comp in self.components.values():
            xml += f'    <component type="{comp.type}" id="{comp.id}">\n'
            xml += f'      <position x="{comp.x}" y="{comp.y}"/>\n'
            xml += f'      <size width="{comp.width}" height="{comp.height}"/>\n'
            xml += f'      <text>{comp.text}</text>\n'
            default_value = getattr(comp, 'default_value', None)
            if default_value is not None:
                xml += f'      <range min="{comp.min_value}" max="{comp.max_value}" default="{default_value}"/>\n'
            else:
                xml += f'      <range min="{comp.min_value}" max="{comp.max_value}"/>\n'
            xml += f'      <appearance color="{comp.color}" text_color="{comp.text_color}" font_size="{comp.font_size}"/>\n'
            xml += '    </component>\n'
        
        xml += '  </components>\n'
        xml += '</gui_layout>\n'
        return xml
    
    def _generate_parameter_layout(self) -> str:
        """Generate JUCE AudioProcessorValueTreeState parameter layout"""
        code = ""

        for comp in self.components.values():
            comp_name = comp.text.replace(" ", "").lower()
            if not comp_name:  # Fallback if text is empty
                comp_name = f"{comp.type}_{comp.id}"
                
            if comp.type in ['horizontalslider', 'verticalslider', 'knob']:
                code += f"    // {comp.text} Parameter\n"
                code += f"    parameterLayout.add(std::make_unique<juce::AudioParameterFloat>(\n"
                code += f"        \"{comp_name.upper()}\",\n"
                code += f"        \"{comp.text}\",\n"
                default_value = getattr(comp, 'default_value', comp.min_value)
                code += f"        juce::NormalisableRange<float>({comp.min_value}f, {comp.max_value}f),\n"
                code += f"        {default_value}f));\n\n"
            elif comp.type in ['button', 'toggle']:
                code += f"    // {comp.text} Parameter\n"
                code += f"    parameterLayout.add(std::make_unique<juce::AudioParameterBool>(\n"
                code += f"        \"{comp_name.upper()}\",\n"
                code += f"        \"{comp.text}\",\n"
                default_value = getattr(comp, 'default_value', False)
                code += f"        {str(bool(default_value)).lower()}));\n\n"

        return code
