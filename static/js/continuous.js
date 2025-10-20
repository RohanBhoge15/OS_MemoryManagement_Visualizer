// Continuous Memory Allocation Module

document.addEventListener('DOMContentLoaded', function() {
    let processes = [];
    
    // Initialize with sample data
    initializePage();
    
    // Event Listeners
    document.getElementById('addProcessBtn').addEventListener('click', addProcess);
    document.getElementById('loadSampleBtn').addEventListener('click', loadSampleData);
    document.getElementById('simulateBtn').addEventListener('click', runSimulation);
    document.getElementById('compareBtn').addEventListener('click', compareAlgorithms);
    document.getElementById('clearBtn').addEventListener('click', clearAll);
    
    function initializePage() {
        loadSampleData();
    }
    
    function addProcess(id = null, size = null) {
        const processList = document.getElementById('processList');
        const processId = id || `P${processes.length + 1}`;
        const processSize = size || 100;
        
        const processItem = document.createElement('div');
        processItem.className = 'process-item fade-in';
        processItem.innerHTML = `
            <input type="text" class="process-id" placeholder="Process ID" value="${processId}">
            <input type="number" class="process-size" placeholder="Size (bytes)" value="${processSize}" min="1">
            <button class="remove-btn" onclick="removeProcess(this)">
                <i class="fas fa-times"></i>
            </button>
        `;
        
        processList.appendChild(processItem);
        processes.push({ id: processId, size: processSize });
    }
    
    window.removeProcess = function(button) {
        const processItem = button.parentElement;
        processItem.remove();
        updateProcessesArray();
    };
    
    function updateProcessesArray() {
        processes = [];
        const processItems = document.querySelectorAll('.process-item');
        processItems.forEach(item => {
            const id = item.querySelector('.process-id').value;
            const size = parseInt(item.querySelector('.process-size').value);
            if (id && size > 0) {
                processes.push({ id, size });
            }
        });
    }
    
    function loadSampleData() {
        const processList = document.getElementById('processList');
        processList.innerHTML = '';
        processes = [];
        
        const sampleProcesses = [
            { id: 'P1', size: 212 },
            { id: 'P2', size: 417 },
            { id: 'P3', size: 112 },
            { id: 'P4', size: 426 }
        ];
        
        sampleProcesses.forEach(p => addProcess(p.id, p.size));
        
        document.getElementById('memorySize').value = 1000;
        document.getElementById('partitionType').value = 'variable';
        document.getElementById('algorithm').value = 'first_fit';
        
        appUtils.showNotification('Sample data loaded successfully!', 'success');
    }
    
    async function runSimulation() {
        updateProcessesArray();
        
        const memorySize = parseInt(document.getElementById('memorySize').value);
        const partitionType = document.getElementById('partitionType').value;
        const algorithm = document.getElementById('algorithm').value;
        
        // Validation
        if (!appUtils.validatePositiveNumber(memorySize, 'Memory Size')) return;
        if (processes.length === 0) {
            appUtils.showNotification('Please add at least one process', 'warning');
            return;
        }
        
        const data = {
            memorySize: memorySize,
            processes: processes,
            partitionType: partitionType,
            algorithm: algorithm
        };
        
        try {
            const result = await appUtils.makeAPIRequest('/api/continuous/simulate', 'POST', data);
            displayResults(result);
            appUtils.showNotification('Simulation completed successfully!', 'success');
        } catch (error) {
            console.error('Simulation error:', error);
        }
    }
    
    function displayResults(result) {
        // Hide comparison results
        document.getElementById('comparisonResults').style.display = 'none';
        
        // Display metrics
        const metricsDisplay = document.getElementById('metricsDisplay');
        metricsDisplay.style.display = 'block';
        
        document.getElementById('utilizationValue').textContent = result.memory_utilization + '%';
        document.getElementById('internalFragValue').textContent = result.internal_fragmentation + ' bytes';
        document.getElementById('externalFragValue').textContent = result.external_fragmentation + ' bytes';
        document.getElementById('allocatedCount').textContent = result.allocated.length;
        
        // Display visualization
        const visualizationDisplay = document.getElementById('visualizationDisplay');
        visualizationDisplay.style.display = 'block';
        document.getElementById('chartImage').src = result.plot;
        
        // Display allocation details
        displayAllocationTable(result);
        
        appUtils.animateElement(metricsDisplay);
        appUtils.animateElement(visualizationDisplay);
    }
    
    function displayAllocationTable(result) {
        const allocationDetails = document.getElementById('allocationDetails');
        const tableBody = document.getElementById('allocationTableBody');
        
        allocationDetails.style.display = 'block';
        tableBody.innerHTML = '';
        
        // Add allocated processes
        result.allocated.forEach(process => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td><strong>${process.id}</strong></td>
                <td>${process.size} bytes</td>
                <td>${process.start !== undefined ? process.start : 'N/A'}</td>
                <td>${process.end !== undefined ? process.end : 'N/A'}</td>
                <td><span class="status-badge status-allocated">Allocated</span></td>
            `;
            tableBody.appendChild(row);
        });
        
        // Add unallocated processes
        result.unallocated.forEach(process => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td><strong>${process.id}</strong></td>
                <td>${process.size} bytes</td>
                <td>-</td>
                <td>-</td>
                <td><span class="status-badge status-free">Not Allocated</span></td>
            `;
            tableBody.appendChild(row);
        });
        
        appUtils.animateElement(allocationDetails);
    }
    
    async function compareAlgorithms() {
        updateProcessesArray();
        
        const memorySize = parseInt(document.getElementById('memorySize').value);
        const partitionType = document.getElementById('partitionType').value;
        
        // Validation
        if (!appUtils.validatePositiveNumber(memorySize, 'Memory Size')) return;
        if (processes.length === 0) {
            appUtils.showNotification('Please add at least one process', 'warning');
            return;
        }
        
        const data = {
            memorySize: memorySize,
            processes: processes,
            partitionType: partitionType
        };
        
        try {
            const result = await appUtils.makeAPIRequest('/api/continuous/compare', 'POST', data);
            displayComparisonResults(result);
            appUtils.showNotification('Comparison completed successfully!', 'success');
        } catch (error) {
            console.error('Comparison error:', error);
        }
    }
    
    function displayComparisonResults(data) {
        // Hide single simulation results
        document.getElementById('allocationDetails').style.display = 'none';
        document.getElementById('visualizationDisplay').style.display = 'none';
        document.getElementById('metricsDisplay').style.display = 'none';
        
        const comparisonResults = document.getElementById('comparisonResults');
        comparisonResults.style.display = 'block';
        
        // Display best algorithm banner
        const bestAlgorithmBanner = document.getElementById('bestAlgorithmBanner');
        const bestAlgorithmName = document.getElementById('bestAlgorithmName');
        bestAlgorithmBanner.style.display = 'flex';
        
        const bestAlgo = data.results.best_algorithm;
        bestAlgorithmName.textContent = formatAlgorithmName(bestAlgo);
        
        // Display comparison chart
        document.getElementById('comparisonChart').src = data.plot;
        
        // Display comparison table
        const tableBody = document.getElementById('comparisonTableBody');
        tableBody.innerHTML = '';
        
        const algorithms = ['first_fit', 'best_fit', 'worst_fit'];
        algorithms.forEach(algo => {
            const result = data.results[algo];
            const row = document.createElement('tr');
            const isBest = algo === bestAlgo;
            
            if (isBest) {
                row.style.background = '#e8f5e9';
                row.style.fontWeight = 'bold';
            }
            
            row.innerHTML = `
                <td>${formatAlgorithmName(algo)} ${isBest ? '<i class="fas fa-trophy" style="color: #4CAF50;"></i>' : ''}</td>
                <td>${result.memory_utilization}%</td>
                <td>${result.internal_fragmentation} bytes</td>
                <td>${result.external_fragmentation} bytes</td>
                <td>${result.total_fragmentation} bytes</td>
                <td>${result.allocated_count}/${result.allocated_count + result.unallocated_count}</td>
            `;
            tableBody.appendChild(row);
        });
        
        appUtils.animateElement(comparisonResults);
        appUtils.scrollToElement('comparisonResults');
    }
    
    function formatAlgorithmName(algo) {
        const names = {
            'first_fit': 'First Fit',
            'best_fit': 'Best Fit',
            'worst_fit': 'Worst Fit'
        };
        return names[algo] || algo;
    }
    
    function clearAll() {
        const processList = document.getElementById('processList');
        processList.innerHTML = '';
        processes = [];
        
        document.getElementById('memorySize').value = 1000;
        document.getElementById('partitionType').value = 'variable';
        document.getElementById('algorithm').value = 'first_fit';
        
        appUtils.clearResults();
        appUtils.showNotification('All data cleared', 'info');
    }
});