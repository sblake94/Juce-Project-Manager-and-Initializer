/*
  ==============================================================================

    This file contains the basic framework code for a JUCE plugin editor.

  ==============================================================================
*/

#include "PluginProcessor.h"
#include "PluginEditor.h"

//==============================================================================
PluginEditor::PluginEditor (PluginProcessor& p)
    : AudioProcessorEditor (&p), audioProcessor (p)
{
    // DeSlider Horizontal Slider
    desliderSlider = std::make_unique<juce::Slider>();
    desliderSlider->setSliderStyle(juce::Slider::LinearHorizontal);
    desliderSlider->setRange(0.0, 1.0);
    desliderSlider->setValue(0.5);
    desliderSlider->setBounds(132, 90, 120, 30);
    addAndMakeVisible(*desliderSlider);
    desliderSliderAttachment = std::make_unique<juce::AudioProcessorValueTreeState::SliderAttachment>(audioProcessor.apvts, "DESLIDER", *desliderSlider);

    // Set the size of the editor
    setSize(408, 308);

    // Call createParameterLayout to initialize parameters
    createParameterLayout();



}

PluginEditor::~PluginEditor()
{
}

//==============================================================================
void PluginEditor::paint (juce::Graphics& g)
{
    // Fill background with gradient
    juce::Colour backgroundColour = juce::Colours::darkgrey;
    juce::Colour secondaryColour = backgroundColour.darker(0.2f);
    
    g.setGradientFill(juce::ColourGradient(
        backgroundColour,
        0.0f, 0.0f,
        secondaryColour,
        0.0f, static_cast<float>(getHeight()),
        false));
    g.fillAll();

    // Draw border
    g.setColour(juce::Colours::black);
    g.drawRect(getLocalBounds(), 1);

    // Draw plugin name/title
    g.setColour(juce::Colours::white);
    g.setFont(15.0f);
    g.drawText("My Awesome Plugin", getLocalBounds().withHeight(20),
               juce::Justification::centred, true);

    // Version number
    g.setFont(10.0f);
    g.drawText("v1.0.0", getLocalBounds().reduced(5).removeFromBottom(15),
               juce::Justification::bottomRight, true);

}

void PluginEditor::resized()
{
    // This is generally where you'll want to lay out the positions of any
    // subcomponents in your editor..

    // This method is where you should set the bounds of any child
    // components that your component contains. Component bounds are
    // already set in the constructor, but you can use this method
    // for dynamic layouts or resizing behavior.

    // Example of proportional layout (if you implement UI resizing):
    // auto area = getLocalBounds();
    // auto topSection = area.removeFromTop(area.getHeight() * 0.3f);
    // auto bottomSection = area;

    // Example: Dynamically position DeSlider slider
    // desliderSlider->setBounds(topSection.removeFromLeft(100).reduced(10));

}
