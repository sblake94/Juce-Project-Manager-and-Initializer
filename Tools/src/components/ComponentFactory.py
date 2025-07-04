from .component import Component
from .HorizontalSlider import HorizontalSlider
from .VerticalSlider import VerticalSlider
from .Knob import Knob
from .Button import Button
from .Toggle import Toggle
from .Label import Label
from .TextBox import TextBox
from .Meter import Meter

# Factory function to create components
def create_component(comp_type: str, comp_id: str, x: int, y: int, text: str = "") -> Component:
    """Factory function to create component instances"""
    if comp_type == 'horizontalslider':
        return HorizontalSlider(comp_id, x, y, text)
    elif comp_type == 'verticalslider':
        return VerticalSlider(comp_id, x, y, text)
    elif comp_type == 'knob':
        return Knob(comp_id, x, y, text)
    elif comp_type == 'button':
        return Button(comp_id, x, y, text)
    elif comp_type == 'toggle':
        return Toggle(comp_id, x, y, text)
    elif comp_type == 'label':
        return Label(comp_id, x, y, text)
    elif comp_type == 'textbox':
        return TextBox(comp_id, x, y, text)
    elif comp_type == 'meter':
        return Meter(comp_id, x, y, text)
    else:
        raise ValueError(f"Unknown component type: {comp_type}")
