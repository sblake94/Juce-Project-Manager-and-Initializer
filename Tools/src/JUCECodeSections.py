from dataclasses import dataclass

@dataclass
class JUCECodeSections:
    """Container for different sections of JUCE code"""
    editor_header_declarations: str = ""
    editor_constructor_code: str = ""
    editor_paint_code: str = ""
    editor_resized_code: str = ""
    processor_header_declarations: str = ""
    processor_constructor_code: str = ""
