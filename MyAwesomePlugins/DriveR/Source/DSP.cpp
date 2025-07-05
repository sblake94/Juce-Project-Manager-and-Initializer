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
		// Steps:
		// 1: Split out the audio into middle and side components
		double mid = (leftChannel[i] + rightChannel[i]) * 0.5f;
		double side = (leftChannel[i] - rightChannel[i]) * 0.5f;

		// 2: Split the high and low frequencies of the side channel
		double highSide = side; // Placeholder for high frequencies
		double lowSide = side;  // Placeholder for low frequencies
	
		// 3: Apply upward compression to the high frequencies of the side channel
		// Placeholder for upward compression logic
		// This could involve applying a gain factor or a specific compression algorithm
		double compressedHighSide = highSide * 1.2; // Example gain factor for upward compression
		double compressedLowSide = lowSide * 0.8; // Example gain factor for downward compression
			
		// 4: Apply downward compression to the low frequencies of the side channel
		// Placeholder for downward compression logic
		// This could involve applying a gain factor or a specific compression algorithm
		double processedHighSide = compressedHighSide; // Placeholder for processed high side
		double processedLowSide = compressedLowSide; // Placeholder for processed low side
	
		// 5: Recombine the processed side channel with the middle channel
		leftChannel[i] = mid + processedHighSide; // Left channel gets mid + processed high side
		rightChannel[i] = mid - processedLowSide; // Right channel gets mid - processed low side

		// 6: Apply Output Gain to the left and right channels


	}
}