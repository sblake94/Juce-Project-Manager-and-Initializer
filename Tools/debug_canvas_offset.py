#!/usr/bin/env python3
"""
Debug script to determine the actual canvas size offset
"""

# Simulate the values you're seeing
expected_canvas_size = (400, 200)  # What you want (based on your message mentioning 204)
generated_juce_size = (404, 204)   # What you're seeing in the generated code

# Calculate the actual offset
actual_width_offset = generated_juce_size[0] - expected_canvas_size[0]
actual_height_offset = generated_juce_size[1] - expected_canvas_size[1]

print("Canvas Size Debug Information")
print("=" * 40)
print(f"Expected canvas size: {expected_canvas_size[0]} x {expected_canvas_size[1]}")
print(f"Generated JUCE size: {generated_juce_size[0]} x {generated_juce_size[1]}")
print(f"Actual offset: {actual_width_offset}px width, {actual_height_offset}px height")
print()

# Test different border scenarios
print("Testing different border/padding scenarios:")
print(f"If border=2 (4px total): Canvas widget would be {expected_canvas_size[0] + 4} x {expected_canvas_size[1] + 4}")
print(f"If border=3 (6px total): Canvas widget would be {expected_canvas_size[0] + 6} x {expected_canvas_size[1] + 6}")
print(f"If border=4 (8px total): Canvas widget would be {expected_canvas_size[0] + 8} x {expected_canvas_size[1] + 8}")
print()

# Determine what border size would create this offset
border_per_side = actual_width_offset // 2
print(f"Calculated border per side: {border_per_side}px")
print(f"Total border/padding: {actual_width_offset}px")
