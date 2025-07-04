# this class is responsible for taking the generated code and writing it to the appropriate files
from src.JUCECodeOutput import JUCECodeOutput
from src.JUCECodeSections import JUCECodeSections

class CodeWriter:
    def __init__(self):
        # Initialize the CodeWriter
        self.editor_header_file = "PluginEditor.h"
        self.editor_cpp_file = "PluginEditor.cpp"
        self.processor_header_file = "PluginProcessor.h"
        self.processor_cpp_file = "PluginProcessor.cpp"

        self.editor_header_genmarker = "// [GENERATED_EDITOR_H_MARKER]"
        self.editor_cppctor_genmarker = "// [GENERATED_EDITOR_CPP_CTOR_MARKER]"
        self.header_cpppaint_gen_paintmarker = "// [GENERATED_EDITOR_CPP_PAINT_MARKER]"
        self.header_cppresized_gen_resizedmarker = "// [GENERATED_EDITOR_CPP_RESIZED_MARKER]"
        self.processor_header_genmarker = "// [GENERATED_PROCESSOR_H_MARKER]"
        self.processor_cppctor_genmarker = "// [GENERATED_PROCESSOR_CPP_MARKER]"
        return

    def write_code(self, code: JUCECodeOutput, output_dir: str = ""):
        if not self._check_files_exist(output_dir):
            raise FileNotFoundError("Required code files do not exist in the output directory.")
        
        self._write_to_plugin_editor_h(code.get_editor_header_code())
        self._write_to_plugin_editor_ctor(code.get_editor_constructor_code())
        self._write_to_plugin_editor_paint(code.get_editor_paint_code())
        self._write_to_plugin_editor_resized(code.get_editor_resized_code())
        self._write_to_plugin_processor_h(code.get_processor_header_code())
        self._write_to_plugin_processor_ctor(code.get_processor_constructor_code())

    def _check_files_exist(self, output_dir: str) -> bool:
        """Check if the required JUCE code files exist in the output directory."""
        if output_dir:
            self.editor_header_file = f"{output_dir}/{self.editor_header_file}"
            self.editor_cpp_file = f"{output_dir}/{self.editor_cpp_file}"
            self.processor_header_file = f"{output_dir}/{self.processor_header_file}"
            self.processor_cpp_file = f"{output_dir}/{self.processor_cpp_file}"
        try:
            with open(self.editor_header_file, 'r') as f:
                pass
            with open(self.editor_cpp_file, 'r') as f:
                pass
            with open(self.processor_header_file, 'r') as f:
                pass
            with open(self.processor_cpp_file, 'r') as f:
                pass
            return True
        except FileNotFoundError:
            return False
        pass

    def _write_to_plugin_editor_h(self, content: str):
        with open(self.editor_header_genmarker, 'r+') as f:
            lines = f.readlines()
            f.seek(0)
            for line in lines:
                if self.editor_header_genmarker in line:
                    f.write(content + "\n")
                else:
                    f.write(line)
            f.truncate()

    def _write_to_plugin_editor_ctor(self, content: str):
        with open(self.editor_cpp_file, 'r+') as f:
            lines = f.readlines()
            f.seek(0)
            for line in lines:
                if self.editor_cppctor_genmarker in line:
                    f.write(content + "\n")
                else:
                    f.write(line)
            f.truncate()

    def _write_to_plugin_editor_paint(self, content: str):
        with open(self.editor_cpp_file, 'r+') as f:
            lines = f.readlines()
            f.seek(0)
            for line in lines:
                if self.header_cpppaint_gen_paintmarker in line:
                    f.write(content + "\n")
                else:
                    f.write(line)
            f.truncate()

    def _write_to_plugin_editor_resized(self, content: str):
        with open(self.editor_cpp_file, 'r+') as f:
            lines = f.readlines()
            f.seek(0)
            for line in lines:
                if self.header_cppresized_gen_resizedmarker in line:
                    f.write(content + "\n")
                else:
                    f.write(line)
            f.truncate()

    def _write_to_plugin_processor_h(self, content: str):
        with open(self.processor_header_file, 'r+') as f:
            lines = f.readlines()
            f.seek(0)
            for line in lines:
                if self.editor_header_genmarker in line:
                    f.write(content + "\n")
                else:
                    f.write(line)
            f.truncate()

    def _write_to_plugin_processor_ctor(self, content: str):
        with open(self.processor_cpp_file, 'r+') as f:
            lines = f.readlines()
            f.seek(0)
            for line in lines:
                if self.processor_cppctor_genmarker in line:
                    f.write(content + "\n")
                else:
                    f.write(line)
            f.truncate()
    

if __name__ == "__main__":
    # Example usage
    code_writer = CodeWriter()
    juce_output = JUCECodeOutput(JUCECodeSections(),)
    
    # Assuming JUCECodeOutput has methods to generate code sections
    juce_output.get_editor_header_code()
    juce_output.get_editor_constructor_code()
    juce_output.get_editor_paint_code()
    juce_output.get_editor_resized_code()
    juce_output.get_processor_header_code()
    juce_output.get_processor_constructor_code()

    try:
        code_writer.write_code(juce_output, output_dir="path/to/your/juce/project")
        print("JUCE code written successfully.")
    except FileNotFoundError as e:
        print(f"Error: {e}")