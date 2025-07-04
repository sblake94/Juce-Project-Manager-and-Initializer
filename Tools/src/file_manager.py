#!/usr/bin/env python3
"""
File operations for saving/loading GUI designs
"""

import json
import os
from typing import Dict, Tuple
from dataclasses import asdict
from .components.component import Component

class FileManager:
    """Handles file operations for GUI designs"""
    
    @staticmethod
    def save_design(filename: str, components: Dict[str, Component], canvas_width: int, canvas_height: int, gui_properties=None):
        """Save design to JSON file"""
        data = {
            'canvas_size': {
                'width': canvas_width,
                'height': canvas_height
            },
            'components': [asdict(comp) for comp in components.values()]
        }
        
        # Add GUI properties if provided
        if gui_properties:
            data['gui_properties'] = gui_properties.to_dict()
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
    
    @staticmethod
    def load_design(filename: str) -> Tuple[Dict[str, Component], int, int, Dict]:
        """Load design from JSON file"""
        with open(filename, 'r') as f:
            data = json.load(f)
        
        components = {}
        for comp_data in data.get('components', []):
            component = Component(**comp_data)
            components[component.id] = component
        
        canvas_size = data.get('canvas_size', {'width': 400, 'height': 300})
        gui_properties_data = data.get('gui_properties', {})
        
        return components, canvas_size['width'], canvas_size['height'], gui_properties_data
    
    @staticmethod
    def save_code(filename: str, code: str):
        """Save generated code to file"""
        with open(filename, 'w') as f:
            f.write(code)
