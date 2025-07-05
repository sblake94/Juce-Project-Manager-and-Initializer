from dataclasses import dataclass
from src.JUCECodeSections import JUCECodeSections

@dataclass 
class JUCECodeOutput:
    """Complete JUCE code output with all sections organized"""
    editor_header_declarations: str
    editor_constructor_code: str
    editor_paint_method: str
    editor_resized_method: str
    processor_header_declarations: str
    processor_constructor_code: str

    def __init__(self, code_sections: JUCECodeSections):
        self.editor_header_declarations = code_sections.editor_header_declarations
        self.editor_constructor_code = code_sections.editor_constructor_code
        self.editor_paint_method = code_sections.editor_paint_code
        self.editor_resized_method = code_sections.editor_resized_code
        self.processor_header_declarations = code_sections.processor_header_declarations
        self.processor_constructor_code = code_sections.processor_constructor_code
    
    def get_formatted_output(self) -> str:
        """Get the complete formatted code output as a string"""
        code = "// ========================================\n"
        code += "// JUCE Audio Plugin GUI Code Generation\n"
        code += "// ========================================\n\n"
        
        code += "// ========================================\n"
        code += "// EDITOR HEADER (.h file)\n"
        code += "// Add these declarations to your PluginEditor class:\n"
        code += "// ========================================\n\n"
        code += self.editor_header_declarations
        
        code += "\n// ========================================\n"
        code += "// EDITOR CONSTRUCTOR (.cpp file)\n"
        code += "// Add this to your PluginEditor constructor:\n"
        code += "// ========================================\n\n"
        code += self.editor_constructor_code
        
        code += "\n// ========================================\n"
        code += "// EDITOR PAINT METHOD (.cpp file)\n"
        code += "// Add this code to your to your PluginEditor paint method:\n"
        code += "// ========================================\n\n"
        code += self.editor_paint_method
        
        code += "\n// ========================================\n"
        code += "// EDITOR RESIZED METHOD (.cpp file)\n"
        code += "// Add this code to your to your PluginEditor resized method:\n"
        code += "// ========================================\n\n"
        code += self.editor_resized_method
        
        code += "\n// ========================================\n"
        code += "// PROCESSOR HEADER (.h file)\n"
        code += "// Add these declarations to your PluginProcessor class:\n"
        code += "// ========================================\n\n"
        code += self.processor_header_declarations
        
        code += "\n// ========================================\n"
        code += "// PROCESSOR CONSTRUCTOR (.cpp file)\n"
        code += "// Add this to your PluginProcessor constructor:\n"
        code += "// ========================================\n\n"
        code += self.processor_constructor_code
        
        return code
    
    def get_editor_header_code(self) -> str:
        """Get only the editor header declarations"""
        return self.editor_header_declarations
    
    def get_editor_constructor_code(self) -> str:
        """Get only the editor constructor code"""
        return self.editor_constructor_code
        
    def get_processor_header_code(self) -> str:
        """Get only the processor header declarations"""
        return self.processor_header_declarations
        
    def get_processor_constructor_code(self) -> str:
        """Get only the processor constructor code"""
        return self.processor_constructor_code
           
    def get_editor_paint_code(self) -> str:
        """Get only the editor paint method code"""
        return self.editor_paint_method
    
    def get_editor_resized_code(self) -> str:
        """Get only the editor resized method code"""
        return self.editor_resized_method
