#!/usr/bin/env python3
"""
Code generation utilities for exporting GUI designs
"""

import json
from typing import Dict, List
from dataclasses import asdict, dataclass
from .components.component import Component
from .JUCECodeSections import JUCECodeSections
from .JUCECodeOutput import JUCECodeOutput 

class CodeGenerator:
    """Handles code generation in various formats"""
    
    def __init__(self, components: Dict[str, Component], canvas_width: int, canvas_height: int):
        self.components = components
        self.canvas_width = canvas_width
        self.canvas_height = canvas_height
    
    def generate_juce_code(self) -> JUCECodeOutput:
        """Generate complete JUCE C++ code for editor and processor"""
        sections = JUCECodeSections()
        
        for comp in self.components.values():
            comp_name = comp.text.replace(" ", "").lower()
            if not comp_name:  # Fallback if text is empty
                comp_name = f"{comp.type}_{comp.id}"
            
            if comp.type == 'horizontalslider':
                self._generate_juce_slider(comp, comp_name, 'LinearHorizontal', sections)
            elif comp.type == 'verticalslider':
                self._generate_juce_slider(comp, comp_name, 'LinearVertical', sections)
            elif comp.type == 'knob':
                self._generate_juce_slider(comp, comp_name, 'RotaryHorizontalVerticalDrag', sections)
            elif comp.type == 'button':
                self._generate_juce_button(comp, comp_name, sections)
            elif comp.type == 'label':
                self._generate_juce_label(comp, comp_name, sections)
            elif comp.type == 'toggle':
                self._generate_juce_toggle(comp, comp_name, sections)
            elif comp.type == 'textbox':
                self._generate_juce_textbox(comp, comp_name, sections)
            elif comp.type == 'meter':
                self._generate_juce_meter(comp, comp_name, sections)
        
        # Generate parameter layout
        parameter_layout = self._generate_parameter_layout()
        
        # Generate paint and resized methods
        paint_method = self._generate_editor_paint_method()
        resized_method = self._generate_editor_resized_method()
        
        # Return structured output
        return JUCECodeOutput(
            editor_header_declarations=sections.editor_header_declarations,
            editor_constructor_code=sections.editor_constructor_code,
            editor_paint_method=paint_method,
            editor_resized_method=resized_method,
            processor_header_declarations=sections.processor_header_declarations,
            processor_constructor_code=sections.processor_constructor_code,
            parameter_layout_code=parameter_layout
        )
    
    def _generate_juce_slider(self, comp: Component, comp_name: str, slider_style: str, sections: JUCECodeSections):
        """Generate JUCE slider code for all sections"""
        # Editor header declarations
        sections.editor_header_declarations += f"    std::unique_ptr<juce::Slider> {comp_name}Slider;\n"
        sections.editor_header_declarations += f"    std::unique_ptr<juce::AudioProcessorValueTreeState::SliderAttachment> {comp_name}SliderAttachment;\n\n"
        
        # Editor constructor code
        sections.editor_constructor_code += f"    // {comp.text} Slider\n"
        sections.editor_constructor_code += f"    {comp_name}Slider = std::make_unique<juce::Slider>();\n"
        sections.editor_constructor_code += f"    {comp_name}Slider->setSliderStyle(juce::Slider::{slider_style});\n"
        sections.editor_constructor_code += f"    {comp_name}Slider->setRange({comp.min_value}, {comp.max_value});\n"
        sections.editor_constructor_code += f"    {comp_name}Slider->setValue({comp.default_value});\n"
        sections.editor_constructor_code += f"    {comp_name}Slider->setBounds({comp.x}, {comp.y}, {comp.width}, {comp.height});\n"
        sections.editor_constructor_code += f"    addAndMakeVisible(*{comp_name}Slider);\n"
        sections.editor_constructor_code += f"    {comp_name}SliderAttachment = std::make_unique<juce::AudioProcessorValueTreeState::SliderAttachment>(audioProcessor.apvts, \"{comp_name.upper()}\", *{comp_name}Slider);\n\n"
        
        # Processor header declarations
        sections.processor_header_declarations += f"    // {comp.text} parameter\n"
        sections.processor_header_declarations += f"    juce::AudioParameterFloat* {comp_name}Parameter;\n\n"
        
        # Processor constructor code
        sections.processor_constructor_code += f"    // {comp.text} Parameter\n"
        sections.processor_constructor_code += f"    {comp_name}Parameter = dynamic_cast<juce::AudioParameterFloat*>(\n"
        sections.processor_constructor_code += f"        apvts.getParameter(\"{comp_name.upper()}\", nullptr));\n\n"

    def _generate_juce_button(self, comp: Component, comp_name: str, sections: JUCECodeSections):
        """Generate JUCE button code for all sections"""
        # Editor header declarations
        sections.editor_header_declarations += f"    std::unique_ptr<juce::TextButton> {comp_name}Button;\n"
        sections.editor_header_declarations += f"    std::unique_ptr<juce::AudioProcessorValueTreeState::ButtonAttachment> {comp_name}ButtonAttachment;\n\n"
        
        # Editor constructor code
        sections.editor_constructor_code += f"    // {comp.text} Button\n"
        sections.editor_constructor_code += f"    {comp_name}Button = std::make_unique<juce::TextButton>();\n"
        sections.editor_constructor_code += f"    {comp_name}Button->setButtonText(\"{comp.text}\");\n"
        sections.editor_constructor_code += f"    {comp_name}Button->setBounds({comp.x}, {comp.y}, {comp.width}, {comp.height});\n"
        sections.editor_constructor_code += f"    addAndMakeVisible(*{comp_name}Button);\n"
        sections.editor_constructor_code += f"    {comp_name}ButtonAttachment = std::make_unique<juce::AudioProcessorValueTreeState::ButtonAttachment>(audioProcessor.apvts, \"{comp_name.upper()}\", *{comp_name}Button);\n\n"
        
        # Processor header declarations
        sections.processor_header_declarations += f"    // {comp.text} parameter\n"
        sections.processor_header_declarations += f"    juce::AudioParameterBool* {comp_name}Parameter;\n\n"
        
        # Processor constructor code
        sections.processor_constructor_code += f"    // {comp.text} Parameter\n"
        sections.processor_constructor_code += f"    {comp_name}Parameter = dynamic_cast<juce::AudioParameterBool*>(\n"
        sections.processor_constructor_code += f"        apvts.getParameter(\"{comp_name.upper()}\", nullptr));\n\n"

    def _generate_juce_toggle(self, comp: Component, comp_name: str, sections: JUCECodeSections):
        """Generate JUCE toggle button code for all sections"""
        # Editor header declarations
        sections.editor_header_declarations += f"    std::unique_ptr<juce::ToggleButton> {comp_name}Toggle;\n"
        sections.editor_header_declarations += f"    std::unique_ptr<juce::AudioProcessorValueTreeState::ButtonAttachment> {comp_name}ToggleAttachment;\n\n"
        
        # Editor constructor code
        sections.editor_constructor_code += f"    // {comp.text} Toggle\n"
        sections.editor_constructor_code += f"    {comp_name}Toggle = std::make_unique<juce::ToggleButton>();\n"
        sections.editor_constructor_code += f"    {comp_name}Toggle->setButtonText(\"{comp.text}\");\n"
        sections.editor_constructor_code += f"    {comp_name}Toggle->setBounds({comp.x}, {comp.y}, {comp.width}, {comp.height});\n"
        sections.editor_constructor_code += f"    addAndMakeVisible(*{comp_name}Toggle);\n"
        sections.editor_constructor_code += f"    {comp_name}ToggleAttachment = std::make_unique<juce::AudioProcessorValueTreeState::ButtonAttachment>(audioProcessor.apvts, \"{comp_name.upper()}\", *{comp_name}Toggle);\n\n"
        
        # Processor header declarations
        sections.processor_header_declarations += f"    // {comp.text} parameter\n"
        sections.processor_header_declarations += f"    juce::AudioParameterBool* {comp_name}Parameter;\n\n"
        
        # Processor constructor code
        sections.processor_constructor_code += f"    // {comp.text} Parameter\n"
        sections.processor_constructor_code += f"    {comp_name}Parameter = dynamic_cast<juce::AudioParameterBool*>(\n"
        sections.processor_constructor_code += f"        apvts.getParameter(\"{comp_name.upper()}\", nullptr));\n\n"

    def _generate_juce_label(self, comp: Component, comp_name: str, sections: JUCECodeSections):
        """Generate JUCE label code for all sections"""
        # Editor header declarations
        sections.editor_header_declarations += f"    std::unique_ptr<juce::Label> {comp_name}Label;\n\n"
        
        # Editor constructor code
        sections.editor_constructor_code += f"    // {comp.text} Label\n"
        sections.editor_constructor_code += f"    {comp_name}Label = std::make_unique<juce::Label>();\n"
        sections.editor_constructor_code += f"    {comp_name}Label->setText(\"{comp.default_value or comp.text}\", juce::dontSendNotification);\n"
        sections.editor_constructor_code += f"    {comp_name}Label->setJustificationType(juce::Justification::centred);\n"
        sections.editor_constructor_code += f"    {comp_name}Label->setBounds({comp.x}, {comp.y}, {comp.width}, {comp.height});\n"
        sections.editor_constructor_code += f"    addAndMakeVisible(*{comp_name}Label);\n\n"
        
        # Labels don't typically need processor parameters

    def _generate_juce_textbox(self, comp: Component, comp_name: str, sections: JUCECodeSections):
        """Generate JUCE text editor code for all sections"""
        # Editor header declarations
        sections.editor_header_declarations += f"    std::unique_ptr<juce::TextEditor> {comp_name}TextBox;\n\n"
        
        # Editor constructor code
        sections.editor_constructor_code += f"    // {comp.text} TextBox\n"
        sections.editor_constructor_code += f"    {comp_name}TextBox = std::make_unique<juce::TextEditor>();\n"
        sections.editor_constructor_code += f"    {comp_name}TextBox->setMultiLine(false);\n"
        sections.editor_constructor_code += f"    {comp_name}TextBox->setReturnKeyStartsNewLine(false);\n"
        sections.editor_constructor_code += f"    {comp_name}TextBox->setReadOnly(false);\n"
        sections.editor_constructor_code += f"    {comp_name}TextBox->setScrollbarsShown(true);\n"
        sections.editor_constructor_code += f"    {comp_name}TextBox->setCaretVisible(true);\n"
        sections.editor_constructor_code += f"    {comp_name}TextBox->setPopupMenuEnabled(true);\n"
        sections.editor_constructor_code += f"    {comp_name}TextBox->setText(\"{comp.default_value or comp.text}\");\n"
        sections.editor_constructor_code += f"    {comp_name}TextBox->setBounds({comp.x}, {comp.y}, {comp.width}, {comp.height});\n"
        sections.editor_constructor_code += f"    addAndMakeVisible(*{comp_name}TextBox);\n\n"

    def _generate_juce_meter(self, comp: Component, comp_name: str, sections: JUCECodeSections):
        """Generate JUCE meter code for all sections"""
        # Editor header declarations
        sections.editor_header_declarations += f"    // {comp.text} Meter (custom component)\n"
        sections.editor_header_declarations += f"    juce::Rectangle<int> {comp_name}MeterBounds;\n"
        sections.editor_header_declarations += f"    float {comp_name}MeterLevel = 0.0f;\n\n"
        
        # Editor constructor code
        sections.editor_constructor_code += f"    // {comp.text} Meter\n"
        sections.editor_constructor_code += f"    {comp_name}MeterBounds = juce::Rectangle<int>({comp.x}, {comp.y}, {comp.width}, {comp.height});\n\n"
        
        # Add note about custom meter implementation
        sections.editor_constructor_code += f"    // Note: Implement custom meter drawing in paint() method\n"
        sections.editor_constructor_code += f"    // Use {comp_name}MeterBounds and {comp_name}MeterLevel\n\n"
        
    def _generate_editor_paint_method(self) -> str:
        """Generate the PluginEditor::paint method code based on components and canvas size"""
        code = "void PluginEditor::paint(juce::Graphics& g)\n{\n"
        
        # Background fill
        code += "    // Fill background with gradient\n"
        code += "    juce::Colour backgroundColour = juce::Colours::darkgrey;\n"
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
        code += "    g.setFont(15.0f);\n"
        code += "    g.drawText(\"My Awesome Plugin\", getLocalBounds().withHeight(20),\n"
        code += "               juce::Justification::centred, true);\n\n"

        # Add placeholder for version number in bottom-right corner
        code += "    // Version number\n"
        code += "    g.setFont(10.0f);\n"
        code += "    g.drawText(\"v1.0.0\", getLocalBounds().reduced(5).removeFromBottom(15),\n"
        code += "               juce::Justification::bottomRight, true);\n"
        
        code += "}\n"
        return code

    def _generate_editor_resized_method(self) -> str:
        """Generate the PluginEditor::resized method code based on components"""
        code = "void PluginEditor::resized()\n{\n"
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
        
        code += "}\n"
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
            xml += f'      <range min="{comp.min_value}" max="{comp.max_value}" default="{comp.default_value}"/>\n'
            xml += f'      <appearance color="{comp.color}" text_color="{comp.text_color}" font_size="{comp.font_size}"/>\n'
            xml += '    </component>\n'
        
        xml += '  </components>\n'
        xml += '</gui_layout>\n'
        return xml
    
    def _generate_parameter_layout(self) -> str:
        """Generate JUCE AudioProcessorValueTreeState parameter layout"""
        code = "// ========================================\n"
        code += "// PARAMETER LAYOUT\n"
        code += "// Add this method to your PluginProcessor class:\n"
        code += "// ========================================\n\n"
        
        code += "juce::AudioProcessorValueTreeState::ParameterLayout createParameterLayout()\n"
        code += "{\n"
        code += "    juce::AudioProcessorValueTreeState::ParameterLayout layout;\n\n"
        
        for comp in self.components.values():
            comp_name = comp.text.replace(" ", "").lower()
            if not comp_name:  # Fallback if text is empty
                comp_name = f"{comp.type}_{comp.id}"
                
            if comp.type in ['horizontalslider', 'verticalslider', 'knob']:
                code += f"    // {comp.text} Parameter\n"
                code += f"    layout.add(std::make_unique<juce::AudioParameterFloat>(\n"
                code += f"        \"{comp_name.upper()}\",\n"
                code += f"        \"{comp.text}\",\n"
                code += f"        juce::NormalisableRange<float>({comp.min_value}f, {comp.max_value}f),\n"
                code += f"        {comp.default_value}f));\n\n"
                
            elif comp.type in ['button', 'toggle']:
                code += f"    // {comp.text} Parameter\n"
                code += f"    layout.add(std::make_unique<juce::AudioParameterBool>(\n"
                code += f"        \"{comp_name.upper()}\",\n"
                code += f"        \"{comp.text}\",\n"
                code += f"        {str(comp.default_value > 0.5).lower()}));\n\n"
        
        code += "    return layout;\n"
        code += "}\n\n"
        
        code += "// Don't forget to initialize APVTS in your processor constructor:\n"
        code += "// apvts(*this, nullptr, \"Parameters\", createParameterLayout())\n"
        
        return code
