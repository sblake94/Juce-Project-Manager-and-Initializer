// componentFactory.js
// Responsible for creating GUI components on the plugin canvas

export function createComponentOnCanvas(type, x, y, canvas) {
    let knob;
    if (type === 'knob') knob = createKnob(x, y);

    canvas.appendChild(knob);
    // Notify backend
    fetch('https://localhost:7296/api/Component/Create', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            type: type,
            x: x,
            y: y
        })
    }).catch(err => console.error('Component create event failed:', err));

    return knob;
}

function createKnob(x, y)
{
    const knob = document.createElement('div');
    knob.className = 'knob-icon';
    knob.style.position = 'absolute';
    knob.style.left = x + 'px';
    knob.style.top = y + 'px';
    knob.title = 'Knob';
    return knob;
}

// Additional component creation functions can be added here