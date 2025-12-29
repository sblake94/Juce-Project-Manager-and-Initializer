/**
 * Main Application Controller
 * Audio Plugin Project Manager Web App
 */

class AudioPluginApp {
    constructor() {
        this.currentProject = null;
        this.canvas = null;
        this.components = new Map();
        this.selectedComponent = null;
        this.guiProperties = {
            width: 400,
            height: 300,
            backgroundColor: '#DDDDDD',
            pluginName: 'My Audio Plugin',
            pluginManufacturer: 'MyCompany'
        };
        
        this.isDragging = false;
        this.dragOffset = { x: 0, y: 0 };
        this.showGrid = true;
        this.zoomLevel = 1.0;
        
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.initializeCanvas();
        this.initializeTabs();
        this.initializeModals();
        this.loadDefaultProject();
        this.updateStatus('Ready - Add components from the toolbox');
    }

    setupEventListeners() {
        // Header controls
        document.getElementById('newProjectBtn').addEventListener('click', () => this.showNewProjectModal());
        document.getElementById('openProjectBtn').addEventListener('click', () => this.openProject());
        document.getElementById('saveProjectBtn').addEventListener('click', () => this.saveProject());
        document.getElementById('exportCodeBtn').addEventListener('click', () => this.showExportModal());

        // Canvas controls
        document.getElementById('toggleGridBtn').addEventListener('click', () => this.toggleGrid());
        document.getElementById('clearCanvasBtn').addEventListener('click', () => this.clearCanvas());

        // GUI Properties
        document.getElementById('canvasWidth').addEventListener('input', (e) => this.updateCanvasSize());
        document.getElementById('canvasHeight').addEventListener('input', (e) => this.updateCanvasSize());
        document.getElementById('backgroundColor').addEventListener('input', (e) => this.updateBackgroundColor());

        // Component toolbox - UI Components
        document.querySelectorAll('#ui-components .component-item').forEach(item => {
            item.addEventListener('click', (e) => this.onComponentSelected(e.target.closest('.component-item')));
            item.addEventListener('dragstart', (e) => this.onComponentDragStart(e));
            item.addEventListener('dragend', (e) => this.onComponentDragEnd(e));
            item.draggable = true;
        });

        // Keyboard shortcuts
        document.addEventListener('keydown', (e) => this.handleKeyboard(e));

        // Window resize
        window.addEventListener('resize', () => this.handleResize());

        // Mouse tracking
        document.addEventListener('mousemove', (e) => this.updateMouseCoords(e));

        // Project manager
        document.getElementById('createProjectBtn').addEventListener('click', () => this.createProject());
        document.getElementById('addReplacementBtn').addEventListener('click', () => this.addCMakeReplacement());
    }

    initializeCanvas() {
        this.canvas = document.getElementById('designCanvas');
        this.ctx = this.canvas.getContext('2d');
        this.canvasOverlay = document.getElementById('canvasOverlay');
        
        // Canvas event listeners
        this.canvas.addEventListener('click', (e) => this.onCanvasClick(e));
        this.canvas.addEventListener('mousedown', (e) => this.onCanvasMouseDown(e));
        this.canvas.addEventListener('mousemove', (e) => this.onCanvasMouseMove(e));
        this.canvas.addEventListener('mouseup', (e) => this.onCanvasMouseUp(e));
        this.canvas.addEventListener('contextmenu', (e) => this.onCanvasContextMenu(e));
        
        // Drag and drop
        this.canvas.addEventListener('dragover', (e) => this.onCanvasDragOver(e));
        this.canvas.addEventListener('drop', (e) => this.onCanvasDrop(e));
        
        this.drawCanvas();
    }

    initializeTabs() {
        // Handle tab switching
        document.querySelectorAll('.tab-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const tabId = e.target.dataset.tab;
                const container = e.target.closest('.left-panel, .right-panel');
                
                // Update tab buttons
                container.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
                e.target.classList.add('active');
                
                // Update tab content
                container.querySelectorAll('.tab-content').forEach(content => {
                    content.classList.remove('active');
                });
                container.querySelector(`#${tabId}`).classList.add('active');
            });
        });
    }

    initializeModals() {
        // Modal close handlers
        document.querySelectorAll('.modal .close').forEach(closeBtn => {
            closeBtn.addEventListener('click', (e) => {
                e.target.closest('.modal').classList.remove('show');
            });
        });

        // Modal background click to close
        document.querySelectorAll('.modal').forEach(modal => {
            modal.addEventListener('click', (e) => {
                if (e.target === modal) {
                    modal.classList.remove('show');
                }
            });
        });

        // New project modal
        document.querySelector('#newProjectModal .confirm-btn').addEventListener('click', () => {
            this.newProject();
            document.getElementById('newProjectModal').classList.remove('show');
        });

        document.querySelector('#newProjectModal .cancel-btn').addEventListener('click', () => {
            document.getElementById('newProjectModal').classList.remove('show');
        });

        // Export modal
        document.getElementById('downloadExportBtn').addEventListener('click', () => this.downloadExport());
        document.querySelector('#exportModal .cancel-btn').addEventListener('click', () => {
            document.getElementById('exportModal').classList.remove('show');
        });

        // Export format change
        document.querySelectorAll('input[name="exportFormat"]').forEach(radio => {
            radio.addEventListener('change', () => this.updateExportOutput());
        });
    }

    loadDefaultProject() {
        // Load default/empty project
        this.components.clear();
        this.juceControls = [];
        this.selectedComponent = null;
        this.updateCanvasFromGUIProperties();
        this.drawCanvas();
    }

    onComponentSelected(componentItem) {
        const componentType = componentItem.dataset.type;
        this.addComponent(componentType);
    }

    onComponentDragStart(e) {
        const componentItem = e.target.closest('.component-item');
        const componentType = componentItem.dataset.type;
        
        e.dataTransfer.setData('text/plain', componentType);
        e.dataTransfer.effectAllowed = 'copy';
        
        // Add dragging class to the component item
        componentItem.classList.add('dragging');
        
        // Store reference for cleanup
        this.currentDragElement = componentItem;
        
        // Create custom drag image
        const dragImage = componentItem.cloneNode(true);
        dragImage.style.transform = 'rotate(3deg)';
        dragImage.style.opacity = '0.8';
        dragImage.style.pointerEvents = 'none';
        e.dataTransfer.setDragImage(dragImage, 40, 20);
        
        this.updateStatus(`Dragging ${componentType} component`);
    }

    onCanvasDragOver(e) {
        e.preventDefault();
        e.dataTransfer.dropEffect = 'copy';
        
        const canvasContainer = this.canvas.parentElement;
        canvasContainer.classList.add('drag-over');
        
        // Update mouse coordinates during drag
        this.updateMouseCoords(e);
    }

    onCanvasDrop(e) {
        e.preventDefault();
        
        const canvasContainer = this.canvas.parentElement;
        canvasContainer.classList.remove('drag-over');
        
        const componentType = e.dataTransfer.getData('text/plain');
        
        if (!componentType) {
            this.updateStatus('Invalid drop - no component type data');
            return;
        }
        
        // Calculate drop position relative to canvas
        const rect = this.canvas.getBoundingClientRect();
        const x = Math.max(0, Math.min(this.guiProperties.width - 50, 
            (e.clientX - rect.left) / this.zoomLevel));
        const y = Math.max(0, Math.min(this.guiProperties.height - 30, 
            (e.clientY - rect.top) / this.zoomLevel));
        
        // Add component at drop position
        this.addComponentAtPosition(componentType, x, y);
        
        // Cleanup is handled by dragend event
    }

    addComponent(type, x = null, y = null) {
        if (x === null) x = Math.random() * (this.guiProperties.width - 100);
        if (y === null) y = Math.random() * (this.guiProperties.height - 50);
        
        this.addComponentAtPosition(type, x, y);
    }

    addComponentAtPosition(type, x, y) {
        const id = `comp_${Date.now()}_${Math.random().toString(36).slice(2, 11)}`;
        const component = ComponentFactory.createComponent(type, id, Math.round(x), Math.round(y));
        
        this.components.set(id, component);
        this.drawCanvas();
        this.updateStatus(`Added ${type} component`);
        
        // Auto-select the new component
        this.selectComponent(id);
    }

    selectComponent(componentId) {
        this.selectedComponent = componentId;
        const component = this.components.get(componentId);
        
        if (component) {
            this.updateStatus(`Selected: ${component.type} - ${component.text || componentId}`);
            // Update properties panel
            if (window.PropertiesManager) {
                PropertiesManager.updateComponentProperties(component);
            }
        }
        
        this.drawCanvas();
    }

    onCanvasClick(e) {
        const rect = this.canvas.getBoundingClientRect();
        const x = (e.clientX - rect.left) / this.zoomLevel;
        const y = (e.clientY - rect.top) / this.zoomLevel;
        
        // Check if clicking on a component
        let clickedComponent = null;
        for (const [id, component] of this.components.entries()) {
            if (x >= component.x && x <= component.x + component.width &&
                y >= component.y && y <= component.y + component.height) {
                clickedComponent = id;
                break;
            }
        }
        
        if (clickedComponent) {
            this.selectComponent(clickedComponent);
        } else {
            this.selectedComponent = null;
            this.updateStatus('No component selected');
            this.drawCanvas();
        }
    }

    onCanvasMouseDown(e) {
        if (this.selectedComponent) {
            const rect = this.canvas.getBoundingClientRect();
            const x = (e.clientX - rect.left) / this.zoomLevel;
            const y = (e.clientY - rect.top) / this.zoomLevel;
            const component = this.components.get(this.selectedComponent);
            
            if (component && x >= component.x && x <= component.x + component.width &&
                y >= component.y && y <= component.y + component.height) {
                this.isDragging = true;
                this.dragOffset = {
                    x: x - component.x,
                    y: y - component.y
                };
                this.canvas.style.cursor = 'grabbing';
            }
        }
    }

    onCanvasMouseMove(e) {
        if (this.isDragging && this.selectedComponent) {
            const rect = this.canvas.getBoundingClientRect();
            const x = (e.clientX - rect.left) / this.zoomLevel;
            const y = (e.clientY - rect.top) / this.zoomLevel;
            const component = this.components.get(this.selectedComponent);
            
            if (component) {
                component.x = Math.max(0, Math.min(this.guiProperties.width - component.width, 
                    x - this.dragOffset.x));
                component.y = Math.max(0, Math.min(this.guiProperties.height - component.height, 
                    y - this.dragOffset.y));
                
                this.drawCanvas();
                
                // Update properties panel if available
                if (window.PropertiesManager) {
                    PropertiesManager.updateComponentProperties(component);
                }
            }
        }
    }

    onCanvasMouseUp(e) {
        if (this.isDragging) {
            this.isDragging = false;
            this.canvas.style.cursor = 'default';
        }
    }

    onCanvasContextMenu(e) {
        e.preventDefault();
        // TODO: Show context menu
    }

    drawCanvas() {
        // Clear canvas
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
        
        // Set background color
        this.ctx.fillStyle = this.guiProperties.backgroundColor;
        this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);
        
        // Draw grid if enabled
        if (this.showGrid) {
            this.drawGrid();
        }
        
        // Draw components
        for (const [id, component] of this.components.entries()) {
            this.drawComponent(component, id === this.selectedComponent);
        }
    }

    drawGrid() {
        const gridSize = 10;
        this.ctx.strokeStyle = 'rgba(0, 0, 0, 0.1)';
        this.ctx.lineWidth = 0.5;
        
        // Vertical lines
        for (let x = 0; x <= this.canvas.width; x += gridSize) {
            this.ctx.beginPath();
            this.ctx.moveTo(x, 0);
            this.ctx.lineTo(x, this.canvas.height);
            this.ctx.stroke();
        }
        
        // Horizontal lines
        for (let y = 0; y <= this.canvas.height; y += gridSize) {
            this.ctx.beginPath();
            this.ctx.moveTo(0, y);
            this.ctx.lineTo(this.canvas.width, y);
            this.ctx.stroke();
        }
    }

    drawComponent(component, isSelected) {
        // Use the ComponentRenderer if available
        if (window.ComponentRenderer) {
            ComponentRenderer.render(this.ctx, component, isSelected);
        } else {
            // Fallback rendering
            this.ctx.fillStyle = component.color || '#CCCCCC';
            this.ctx.fillRect(component.x, component.y, component.width, component.height);
            
            if (isSelected) {
                this.ctx.strokeStyle = '#0078D4';
                this.ctx.lineWidth = 2;
                this.ctx.strokeRect(component.x - 1, component.y - 1, 
                    component.width + 2, component.height + 2);
            }
            
            // Draw label
            if (component.text) {
                this.ctx.fillStyle = component.textColor || '#000000';
                this.ctx.font = `${component.fontSize || 12}px sans-serif`;
                this.ctx.textAlign = 'center';
                this.ctx.fillText(component.text, 
                    component.x + component.width / 2, 
                    component.y + component.height + 15);
            }
        }
    }

    toggleGrid() {
        this.showGrid = !this.showGrid;
        document.getElementById('toggleGridBtn').textContent = 
            this.showGrid ? 'Hide Grid' : 'Show Grid';
        this.drawCanvas();
    }

    clearCanvas() {
        if (this.components.size > 0) {
            if (confirm('Clear all components from the canvas?')) {
                this.components.clear();
                this.selectedComponent = null;
                this.drawCanvas();
                this.updateStatus('Canvas cleared');
                
                // Update properties panel
                if (window.PropertiesManager) {
                    PropertiesManager.clearProperties();
                }
            }
        }
    }

    updateCanvasSize() {
        const width = parseInt(document.getElementById('canvasWidth').value);
        const height = parseInt(document.getElementById('canvasHeight').value);
        
        if (width && height && width >= 200 && height >= 150) {
            this.guiProperties.width = width;
            this.guiProperties.height = height;
            this.updateCanvasFromGUIProperties();
        }
    }

    updateBackgroundColor() {
        const color = document.getElementById('backgroundColor').value;
        this.guiProperties.backgroundColor = color;
        this.drawCanvas();
    }

    updateCanvasFromGUIProperties() {
        this.canvas.width = this.guiProperties.width;
        this.canvas.height = this.guiProperties.height;
        document.getElementById('canvasSizeText').textContent = 
            `${this.guiProperties.width} x ${this.guiProperties.height}`;
        this.drawCanvas();
    }

    showNewProjectModal() {
        document.getElementById('newProjectModal').classList.add('show');
    }

    showExportModal() {
        document.getElementById('exportModal').classList.add('show');
        this.updateExportOutput();
    }

    newProject() {
        this.components.clear();
        this.selectedComponent = null;
        this.currentProject = null;
        this.drawCanvas();
        this.updateStatus('New project created');
        
        // Reset GUI properties to defaults
        this.guiProperties = {
            width: 400,
            height: 300,
            backgroundColor: '#DDDDDD',
            pluginName: 'My Audio Plugin',
            pluginManufacturer: 'MyCompany'
        };
        
        document.getElementById('canvasWidth').value = this.guiProperties.width;
        document.getElementById('canvasHeight').value = this.guiProperties.height;
        document.getElementById('backgroundColor').value = this.guiProperties.backgroundColor;
        
        this.updateCanvasFromGUIProperties();
    }

    openProject() {
        // TODO: Implement file opening
        this.updateStatus('Open project - Not implemented yet');
    }

    saveProject() {
        // TODO: Implement file saving
        this.updateStatus('Save project - Not implemented yet');
    }

    updateExportOutput() {
        const selectedFormat = document.querySelector('input[name="exportFormat"]:checked').value;
        const exportOutput = document.getElementById('exportOutput');
        
        if (selectedFormat === 'juce' && window.JUCECodeGenerator) {
            exportOutput.value = JUCECodeGenerator.generateCode(this.components, this.guiProperties);
        } else if (selectedFormat === 'json' && window.FileManager) {
            exportOutput.value = FileManager.exportToJSON(this.components, this.guiProperties);
        } else if (selectedFormat === 'xml' && window.FileManager) {
            exportOutput.value = FileManager.exportToXML(this.components, this.guiProperties);
        } else {
            exportOutput.value = '// Code generation not available yet';
        }
    }

    downloadExport() {
        const selectedFormat = document.querySelector('input[name="exportFormat"]:checked').value;
        const content = document.getElementById('exportOutput').value;
        
        if (!content.trim()) return;
        
        const extensions = {
            'juce': 'cpp',
            'json': 'json',
            'xml': 'xml'
        };
        
        const filename = `${this.guiProperties.pluginName.replace(/\s+/g, '_')}_export.${extensions[selectedFormat]}`;
        
        const blob = new Blob([content], { type: 'text/plain' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
        
        this.updateStatus(`Exported ${selectedFormat.toUpperCase()} code`);
    }

    createProject() {
        const projectName = document.getElementById('projectName').value.trim();
        const projectType = document.getElementById('projectType').value;
        
        if (!projectName) {
            alert('Please enter a project name');
            return;
        }
        
        // TODO: Implement project creation
        this.updateStatus(`Create project: ${projectName} (${projectType}) - Not implemented yet`);
    }

    addCMakeReplacement() {
        // TODO: Implement CMake replacement addition
        this.updateStatus('Add CMake replacement - Not implemented yet');
    }

    handleKeyboard(e) {
        if (e.ctrlKey) {
            switch(e.key) {
                case 'n':
                    e.preventDefault();
                    this.showNewProjectModal();
                    break;
                case 's':
                    e.preventDefault();
                    this.saveProject();
                    break;
                case 'o':
                    e.preventDefault();
                    this.openProject();
                    break;
                case 'e':
                    e.preventDefault();
                    this.showExportModal();
                    break;
            }
        }
        
        // Delete selected component
        if (e.key === 'Delete' && this.selectedComponent) {
            this.components.delete(this.selectedComponent);
            this.selectedComponent = null;
            this.drawCanvas();
            this.updateStatus('Component deleted');
        }
    }

    handleResize() {
        // Handle window resize if needed
        this.drawCanvas();
    }

    updateMouseCoords(e) {
        const canvas = document.getElementById('designCanvas');
        if (canvas) {
            const rect = canvas.getBoundingClientRect();
            const x = Math.round((e.clientX - rect.left) / this.zoomLevel);
            const y = Math.round((e.clientY - rect.top) / this.zoomLevel);
            
            if (x >= 0 && x <= this.guiProperties.width && y >= 0 && y <= this.guiProperties.height) {
                document.getElementById('mouseCoords').textContent = `X: ${x}, Y: ${y}`;
            }
        }
    }

    updateStatus(message) {
        document.getElementById('statusText').textContent = message;
        console.log(`[AudioPluginApp] ${message}`);
    }
}

// Global app instance
let app = null;

// Initialize app when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    app = new AudioPluginApp();
    console.log('Audio Plugin Project Manager initialized');
});

// Export for other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = AudioPluginApp;
}