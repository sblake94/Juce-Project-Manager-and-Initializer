/*
  ==============================================================================

    DSP.cpp
    Created: 25 Jun 2025 7:32:52pm
    Author:  sam_b

  ==============================================================================
*/

#include "PluginProcessor.h"

void PluginProcessor::processDSP(juce::AudioBuffer<float>& buffer, juce::MidiBuffer&)
{
	auto numSamples = buffer.getNumSamples();
	auto* leftChannel = buffer.getWritePointer(0);
	auto* rightChannel = buffer.getWritePointer(1);
	
	for (int i = 0; i < numSamples; ++i)
	{
		
	}
}