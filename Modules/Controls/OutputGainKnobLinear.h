#pragma once

class OutputGainKnobLinear
    : public juce::Slider
{
public:
    OutputGainKnobLinear()
        : juce::Slider(juce::Slider::RotaryVerticalDrag,
                       juce::Slider::TextBoxBelow)
    {
        setRange(minValue, maxValue, stepSize);
        setValue(defaultValue);
        setSliderStyle(sliderStyle);
        setTextBoxStyle(juce::Slider::TextBoxBelow, false, 0, 0);
        setPopupDisplayEnabled(true, true, this);
    }

private:
    float minValue = 0.0f;
    float maxValue = 1.0f;
    float defaultValue = 1.0f;
    float stepSize = 0.001f;
	juce::Slider::SliderStyle sliderStyle = juce::Slider::RotaryHorizontalVerticalDrag;

};