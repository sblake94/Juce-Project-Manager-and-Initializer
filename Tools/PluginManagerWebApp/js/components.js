/**
 * Component system for Audio Plugin Project Manager
 * Creates and manages UI components
 */

// Base Component class
class Component {
    constructor(id, type, x, y, width = 80, height = 30) {
        this.id = id;
        this.type = type;
        this.x = x;
        this.y = y;
        this.width = width;
        this.height = height;
        this.text = type;
        this.color = '#CCCCCC';
        this.textColor = '#000000';
        this.fontSize = 12;
        this.minValue = 0.0;
        this.maxValue = 1.0;
        this.defaultValue = 0.5;
        this.visible = true;
        this.enabled = true;
    }

    // Get component bounds
    getBounds() {
        return {
            x: this.x,
            y: this.y,
            width: this.width,
            height: this.height
        };
    }

    // Check if point is inside component
    containsPoint(x, y) {
        return Utils.pointInRect(x, y, this.x, this.y, this.width, this.height);
    }

    // Clone component
    clone() {
        return Utils.deepClone(this);
    }
}

// Specific component types
class HorizontalSlider extends Component {
    constructor(id, x, y) {
        super(id, 'horizontalslider', x, y, 120, 20);
        this.text = 'Slider';
        this.color = '#E9ECEF';
        this.sliderColor = '#0078D4';
        this.thumbColor = '#FFFFFF';
    }
}

class VerticalSlider extends Component {
    constructor(id, x, y) {
        super(id, 'verticalslider', x, y, 20, 120);
        this.text = 'Slider';
        this.color = '#E9ECEF';
        this.sliderColor = '#0078D4';
        this.thumbColor = '#FFFFFF';
    }
}

class Knob extends Component {
    constructor(id, x, y) {
        super(id, 'knob', x, y, 60, 60);
        this.text = 'Knob';
        this.color = '#F8F9FA';
        this.knobColor = '#0078D4';
        this.pointerColor = '#0078D4';
    }
}

class Button extends Component {
    constructor(id, x, y) {
        super(id, 'button', x, y, 80, 30);
        this.text = 'Button';
        this.color = '#28A745';
        this.textColor = '#FFFFFF';
        this.pressed = false;
    }
}

class Toggle extends Component {
    constructor(id, x, y) {
        super(id, 'toggle', x, y, 50, 25);
        this.text = 'Toggle';
        this.color = '#6C757D';
        this.toggledColor = '#28A745';
        this.toggled = false;
    }
}

class Label extends Component {
    constructor(id, x, y) {
        super(id, 'label', x, y, 80, 20);
        this.text = 'Label';
        this.color = 'transparent';
        this.borderColor = '#DEE2E6';
        this.alignment = 'center';
    }
}

class TextBox extends Component {
    constructor(id, x, y) {
        super(id, 'textbox', x, y, 100, 25);
        this.text = 'Text';
        this.color = '#FFFFFF';
        this.borderColor = '#0078D4';
        this.placeholder = 'Enter text...';
    }
}

class Meter extends Component {
    constructor(id, x, y) {
        super(id, 'meter', x, y, 20, 100);
        this.text = 'Meter';
        this.color = '#333333';
        this.meterColor = '#44FF44';
        this.peakColor = '#FF4444';
        this.level = 0.7;
    }
}

class ComboBox extends Component {
    constructor(id, x, y) {
        super(id, 'combobox', x, y, 120, 25);
        this.text = 'ComboBox';
        this.color = '#FFFFFF';
        this.borderColor = '#0078D4';
        this.options = ['Option 1', 'Option 2', 'Option 3'];
        this.selectedIndex = 0;
    }
}

// Component Factory
class ComponentFactory {
    static createComponent(type, id, x, y) {
        switch (type) {
            case 'horizontalslider':
                return new HorizontalSlider(id, x, y);
            case 'verticalslider':
                return new VerticalSlider(id, x, y);
            case 'knob':
                return new Knob(id, x, y);
            case 'button':
                return new Button(id, x, y);
            case 'toggle':
                return new Toggle(id, x, y);
            case 'label':
                return new Label(id, x, y);
            case 'textbox':
                return new TextBox(id, x, y);
            case 'meter':
                return new Meter(id, x, y);
            case 'combobox':
                return new ComboBox(id, x, y);
            default:
                console.warn(`Unknown component type: ${type}`);
                return new Component(id, type, x, y);
        }
    }

    static getDefaultSize(type) {
        switch (type) {
            case 'horizontalslider':
                return { width: 120, height: 20 };
            case 'verticalslider':
                return { width: 20, height: 120 };
            case 'knob':
                return { width: 60, height: 60 };
            case 'button':
                return { width: 80, height: 30 };
            case 'toggle':
                return { width: 50, height: 25 };
            case 'label':
                return { width: 80, height: 20 };
            case 'textbox':
                return { width: 100, height: 25 };
            case 'meter':
                return { width: 20, height: 100 };
            case 'combobox':
                return { width: 120, height: 25 };
            default:
                return { width: 80, height: 30 };
        }
    }

    static getSupportedTypes() {
        return [
            'horizontalslider',
            'verticalslider',
            'knob',
            'button',
            'toggle',
            'label',
            'textbox',
            'meter',
            'combobox'
        ];
    }
}

// Component Renderer
class ComponentRenderer {
    static render(ctx, component, isSelected = false) {
        if (!component.visible) return;

        ctx.save();

        // Render based on component type
        switch (component.type) {
            case 'horizontalslider':
                this.renderHorizontalSlider(ctx, component);
                break;
            case 'verticalslider':
                this.renderVerticalSlider(ctx, component);
                break;
            case 'knob':
                this.renderKnob(ctx, component);
                break;
            case 'button':
                this.renderButton(ctx, component);
                break;
            case 'toggle':
                this.renderToggle(ctx, component);
                break;
            case 'label':
                this.renderLabel(ctx, component);
                break;
            case 'textbox':
                this.renderTextBox(ctx, component);
                break;
            case 'meter':
                this.renderMeter(ctx, component);
                break;
            case 'combobox':
                this.renderComboBox(ctx, component);
                break;
            default:
                this.renderDefault(ctx, component);
        }

        // Render selection highlight
        if (isSelected) {
            this.renderSelection(ctx, component);
        }

        // Render text label if needed
        if (component.text && component.type !== 'label' && component.type !== 'textbox') {
            this.renderTextLabel(ctx, component);
        }

        ctx.restore();
    }

    // Safely normalize a value to [0, 1] based on min/max.
    // Returns 0 when range is invalid (e.g., max <= min) to avoid divide-by-zero.
    static normalizeValue(value, min, max) {
        const range = max - min;
        if (!Number.isFinite(range) || range <= 0) return 0;
        const normalized = (value - min) / range;
        if (!Number.isFinite(normalized)) return 0;
        return Math.min(Math.max(normalized, 0), 1);
    }

    static renderHorizontalSlider(ctx, comp) {
        // Background track
        ctx.fillStyle = comp.color;
        ctx.fillRect(comp.x, comp.y + comp.height/2 - 2, comp.width, 4);
        
        // Thumb
        const norm = this.normalizeValue(comp.defaultValue, comp.minValue, comp.maxValue);
        const thumbX = comp.x + norm * comp.width - 8;
        ctx.fillStyle = comp.thumbColor;
        ctx.strokeStyle = comp.sliderColor;
        ctx.lineWidth = 2;
        ctx.fillRect(thumbX, comp.y, 16, comp.height);
        ctx.strokeRect(thumbX, comp.y, 16, comp.height);
    }

    static renderVerticalSlider(ctx, comp) {
        // Background track
        ctx.fillStyle = comp.color;
        ctx.fillRect(comp.x + comp.width/2 - 2, comp.y, 4, comp.height);
        
        // Thumb
        const norm = this.normalizeValue(comp.defaultValue, comp.minValue, comp.maxValue);
        const thumbY = comp.y + comp.height - norm * comp.height - 8;
        ctx.fillStyle = comp.thumbColor;
        ctx.strokeStyle = comp.sliderColor;
        ctx.lineWidth = 2;
        ctx.fillRect(comp.x, thumbY, comp.width, 16);
        ctx.strokeRect(comp.x, thumbY, comp.width, 16);
    }

    static renderKnob(ctx, comp) {
        const centerX = comp.x + comp.width / 2;
        const centerY = comp.y + comp.height / 2;
        const radius = Math.min(comp.width, comp.height) / 2 - 2;
        
        // Outer circle
        ctx.beginPath();
        ctx.arc(centerX, centerY, radius, 0, 2 * Math.PI);
        ctx.fillStyle = comp.color;
        ctx.fill();
        ctx.strokeStyle = comp.knobColor;
        ctx.lineWidth = 2;
        ctx.stroke();
        
        // Pointer
        const norm = this.normalizeValue(comp.defaultValue, comp.minValue, comp.maxValue);
        const angle = norm * Math.PI * 1.5 - Math.PI * 0.75;
        const pointerX = centerX + Math.cos(angle) * (radius - 8);
        const pointerY = centerY + Math.sin(angle) * (radius - 8);
        
        ctx.beginPath();
        ctx.moveTo(centerX, centerY);
        ctx.lineTo(pointerX, pointerY);
        ctx.strokeStyle = comp.pointerColor;
        ctx.lineWidth = 3;
        ctx.stroke();
    }

    static renderButton(ctx, comp) {
        // Button background
        ctx.fillStyle = comp.pressed ? this.darkenColor(comp.color, 0.2) : comp.color;
        ctx.fillRect(comp.x, comp.y, comp.width, comp.height);
        
        // Button border
        ctx.strokeStyle = this.darkenColor(comp.color, 0.3);
        ctx.lineWidth = 1;
        ctx.strokeRect(comp.x, comp.y, comp.width, comp.height);
        
        // Button text
        ctx.fillStyle = comp.textColor;
        ctx.font = `${comp.fontSize}px sans-serif`;
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText(comp.text, comp.x + comp.width/2, comp.y + comp.height/2);
    }

    static renderToggle(ctx, comp) {
        // Toggle background
        ctx.fillStyle = comp.toggled ? comp.toggledColor : comp.color;
        ctx.beginPath();
        ctx.roundRect(comp.x, comp.y, comp.width, comp.height, comp.height/2);
        ctx.fill();
        
        // Toggle handle
        const handleRadius = comp.height/2 - 2;
        const handleX = comp.toggled ? comp.x + comp.width - handleRadius - 2 : comp.x + handleRadius + 2;
        const handleY = comp.y + comp.height/2;
        
        ctx.fillStyle = '#FFFFFF';
        ctx.beginPath();
        ctx.arc(handleX, handleY, handleRadius, 0, 2 * Math.PI);
        ctx.fill();
    }

    static renderLabel(ctx, comp) {
        // Label border (dashed if transparent background)
        if (comp.color === 'transparent') {
            ctx.setLineDash([5, 5]);
            ctx.strokeStyle = comp.borderColor;
            ctx.strokeRect(comp.x, comp.y, comp.width, comp.height);
            ctx.setLineDash([]);
        } else {
            ctx.fillStyle = comp.color;
            ctx.fillRect(comp.x, comp.y, comp.width, comp.height);
        }
        
        // Label text
        ctx.fillStyle = comp.textColor;
        ctx.font = `${comp.fontSize}px sans-serif`;
        ctx.textAlign = comp.alignment === 'left' ? 'left' : comp.alignment === 'right' ? 'right' : 'center';
        ctx.textBaseline = 'middle';
        
        const textX = comp.alignment === 'left' ? comp.x + 4 : 
                     comp.alignment === 'right' ? comp.x + comp.width - 4 : 
                     comp.x + comp.width/2;
        
        ctx.fillText(comp.text, textX, comp.y + comp.height/2);
    }

    static renderTextBox(ctx, comp) {
        // TextBox background
        ctx.fillStyle = comp.color;
        ctx.fillRect(comp.x, comp.y, comp.width, comp.height);
        
        // TextBox border
        ctx.strokeStyle = comp.borderColor;
        ctx.lineWidth = 1;
        ctx.strokeRect(comp.x, comp.y, comp.width, comp.height);
        
        // TextBox text
        ctx.fillStyle = comp.textColor;
        ctx.font = `${comp.fontSize}px sans-serif`;
        ctx.textAlign = 'left';
        ctx.textBaseline = 'middle';
        ctx.fillText(comp.text || comp.placeholder, comp.x + 4, comp.y + comp.height/2);
        
        // Cursor (blinking effect simulation)
        if (Date.now() % 1000 < 500) {
            ctx.beginPath();
            ctx.moveTo(comp.x + 4 + ctx.measureText(comp.text || '').width + 2, comp.y + 4);
            ctx.lineTo(comp.x + 4 + ctx.measureText(comp.text || '').width + 2, comp.y + comp.height - 4);
            ctx.strokeStyle = comp.textColor;
            ctx.stroke();
        }
    }

    static renderMeter(ctx, comp) {
        // Meter background
        ctx.fillStyle = comp.color;
        ctx.fillRect(comp.x, comp.y, comp.width, comp.height);
        
        // Meter fill
        const fillHeight = comp.height * comp.level;
        const fillY = comp.y + comp.height - fillHeight;
        
        // Gradient for meter
        const gradient = ctx.createLinearGradient(0, comp.y + comp.height, 0, comp.y);
        gradient.addColorStop(0, '#44FF44');
        gradient.addColorStop(0.6, '#FFAA44');
        gradient.addColorStop(1, '#FF4444');
        
        ctx.fillStyle = gradient;
        ctx.fillRect(comp.x + 2, fillY, comp.width - 4, fillHeight);
        
        // Meter border
        ctx.strokeStyle = '#222222';
        ctx.lineWidth = 1;
        ctx.strokeRect(comp.x, comp.y, comp.width, comp.height);
    }

    static renderComboBox(ctx, comp) {
        // ComboBox background
        ctx.fillStyle = comp.color;
        ctx.fillRect(comp.x, comp.y, comp.width, comp.height);
        
        // ComboBox border
        ctx.strokeStyle = comp.borderColor;
        ctx.lineWidth = 1;
        ctx.strokeRect(comp.x, comp.y, comp.width, comp.height);
        
        // Selected option text
        const selectedText = comp.options[comp.selectedIndex] || 'Select...';
        ctx.fillStyle = comp.textColor;
        ctx.font = `${comp.fontSize}px sans-serif`;
        ctx.textAlign = 'left';
        ctx.textBaseline = 'middle';
        ctx.fillText(selectedText, comp.x + 6, comp.y + comp.height/2);
        
        // Dropdown arrow
        ctx.fillStyle = comp.borderColor;
        ctx.font = '12px sans-serif';
        ctx.textAlign = 'center';
        ctx.fillText('▼', comp.x + comp.width - 12, comp.y + comp.height/2);
    }

    static renderDefault(ctx, comp) {
        // Default rendering for unknown components
        ctx.fillStyle = comp.color;
        ctx.fillRect(comp.x, comp.y, comp.width, comp.height);
        
        ctx.strokeStyle = '#666666';
        ctx.lineWidth = 1;
        ctx.strokeRect(comp.x, comp.y, comp.width, comp.height);
        
        // Component type text
        ctx.fillStyle = comp.textColor;
        ctx.font = `${comp.fontSize}px sans-serif`;
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText(comp.type, comp.x + comp.width/2, comp.y + comp.height/2);
    }

    static renderSelection(ctx, comp) {
        // Selection outline
        ctx.strokeStyle = '#0078D4';
        ctx.lineWidth = 2;
        ctx.setLineDash([]);
        ctx.strokeRect(comp.x - 2, comp.y - 2, comp.width + 4, comp.height + 4);
        
        // Selection handles
        const handleSize = 6;
        const handles = [
            { x: comp.x - 3, y: comp.y - 3 },
            { x: comp.x + comp.width - 3, y: comp.y - 3 },
            { x: comp.x - 3, y: comp.y + comp.height - 3 },
            { x: comp.x + comp.width - 3, y: comp.y + comp.height - 3 }
        ];
        
        ctx.fillStyle = '#0078D4';
        handles.forEach(handle => {
            ctx.fillRect(handle.x, handle.y, handleSize, handleSize);
        });
    }

    static renderTextLabel(ctx, comp) {
        if (!comp.text) return;
        
        // Text label below component
        ctx.fillStyle = comp.textColor;
        ctx.font = `${comp.fontSize}px sans-serif`;
        ctx.textAlign = 'center';
        ctx.textBaseline = 'top';
        ctx.fillText(comp.text, comp.x + comp.width/2, comp.y + comp.height + 4);
    }

    static darkenColor(color, factor) {
        // Simple color darkening
        if (color.startsWith('#')) {
            const rgb = Utils.hexToRgb(color);
            if (rgb) {
                return Utils.rgbToHex(
                    Math.floor(rgb.r * (1 - factor)),
                    Math.floor(rgb.g * (1 - factor)),
                    Math.floor(rgb.b * (1 - factor))
                );
            }
        }
        return color;
    }
}

// Export to global scope
if (typeof window !== 'undefined') {
    window.Component = Component;
    window.ComponentFactory = ComponentFactory;
    window.ComponentRenderer = ComponentRenderer;
    window.HorizontalSlider = HorizontalSlider;
    window.VerticalSlider = VerticalSlider;
    window.Knob = Knob;
    window.Button = Button;
    window.Toggle = Toggle;
    window.Label = Label;
    window.TextBox = TextBox;
    window.Meter = Meter;
    window.ComboBox = ComboBox;
}

// Node.js exports
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        Component,
        ComponentFactory,
        ComponentRenderer,
        HorizontalSlider,
        VerticalSlider,
        Knob,
        Button,
        Toggle,
        Label,
        TextBox,
        Meter,
        ComboBox
    };
}