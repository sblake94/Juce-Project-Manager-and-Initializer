// selectionManager.js
// Provides unified selection/deselection logic for components on the canvas

export function deselectAll(container) {
    if (!container) return;
    const selected = container.querySelectorAll('.highlight-border');
    selected.forEach(el => {
        el.classList.remove('highlight-border');
        try { el.blur(); } catch (e) {}
    });
}

export function selectComponent(el, container) {
    if (!el) return;
    if (container) deselectAll(container);
    el.classList.add('highlight-border');
    try { el.focus(); } catch (e) {}
}
