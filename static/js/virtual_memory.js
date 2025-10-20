// Virtual Memory Module

document.addEventListener('DOMContentLoaded', function() {
    let accessPattern = [];
    
    // Initialize with sample data
    initializePage();
    
    // Event Listeners
    document.getElementById('addAccessBtn').addEventListener('click', () => addAccess());
    document.getElementById('generateRandomBtn').addEventListener('click', generateRandomAccesses);
    document.getElementById('loadSampleBtn').addEventListener('click', loadSampleData);
    document.getElementById('simulateBtn').addEventListener('click', runSimulation);
    document.getElementById('translateBtn').addEventListener('click', translateAddress);
    document.getElementById('clearBtn').addEventListener('click', clearAll);
    
    function initializePage() {
        loadSampleData();
    }
    
    function addAccess(address = null, type = 'read') {
        const accessPatternList = document.getElementById('accessPatternList');
        const accessAddress = address !== null ? address : 0;
        const accessType = type;
        
        const accessItem = document.createElement('div');
        accessItem.className = 'access-item fade-in';
        accessItem.innerHTML = `
            <input type="number" class="access-address" placeholder="Address (decimal)" value="${accessAddress}" min="0">
            <select class="access-type">
                <option value="read" ${accessType === 'read' ? 'selected' : ''}>Read</option>
                <option value="write" ${accessType === 'write' ? 'selected' : ''}>Write</option>
            </select>
            <button class="remove-btn" onclick="removeAccess(this)">
                <i class="fas fa-times"></i>
            </button>
        `;
        
        accessPatternList.appendChild(accessItem);
        accessPattern.push({ address: accessAddress, type: accessType });
    }
    
    window.removeAccess = function(button) {
        const accessItem = button.parentElement;
        accessItem.remove();
        updateAccessPatternArray();
    };
    
    function updateAccessPatternArray() {
        accessPattern = [];
        const accessItems = document.querySelectorAll('.access-item');
        accessItems.forEach(item => {
            const address = parseInt(item.querySelector('.access-address').value);
            const type = item.querySelector('.access-type').value;
            if (!isNaN(address) && address >= 0) {
                accessPattern.push({ address, type });
            }
        });
    }
    
    function generateRandomAccesses() {
        const accessPatternList = document.getElementById('accessPatternList');
        accessPatternList.innerHTML = '';
        accessPattern = [];
        
        const virtualSize = parseInt(document.getElementById('virtualSize').value);
        const numAccesses = 10;
        
        for (let i = 0; i < numAccesses; i++) {
            const randomAddress = Math.floor(Math.random() * virtualSize);
            const randomType = Math.random() > 0.5 ? 'read' : 'write';
            addAccess(randomAddress, randomType);
        }
        
        appUtils.showNotification('Random access pattern generated!', 'success');
    }
    
    function loadSampleData() {
        const accessPatternList = document.getElementById('accessPatternList');
        accessPatternList.innerHTML = '';
        accessPattern = [];
        
        document.getElementById('virtualSize').value = 65536;
        document.getElementById('physicalSize').value = 16384;
        document.getElementById('pageSize').value = 4096;
        
        const sampleAccesses = [
            { address: 8192, type: 'read' },
            { address: 12288, type: 'write' },
            { address: 8192, type: 'read' },
            { address: 20480, type: 'read' },
            { address: 0, type: 'write' },
            { address: 8192, type: 'read' },
            { address: 4096, type: 'read' },
            { address: 20480, type: 'write' },
            { address: 12288, type: 'read' },
            { address: 16384, type: 'read' }
        ];
        
        sampleAccesses.forEach(access => addAccess(access.address, access.type));
        
        appUtils.showNotification('Sample data loaded successfully!', 'success');
    }
    
    async function runSimulation() {
        updateAccessPatternArray();
        
        const virtualSize = parseInt(document.getElementById('virtualSize').value);
        const physicalSize = parseInt(document.getElementById('physicalSize').value);
        const pageSize = parseInt(document.getElementById('pageSize').value);
        
        // Validation
        if (!appUtils.validatePositiveNumber(virtualSize, 'Virtual Memory Size')) return;
        if (!appUtils.validatePositiveNumber(physicalSize, 'Physical Memory Size')) return;
        if (!appUtils.validatePositiveNumber(pageSize, 'Page Size')) return;
        
        if (accessPattern.length === 0) {
            appUtils.showNotification('Please add at least one memory access', 'warning');
            return;
        }
        
        const data = {
            virtualSize: virtualSize,
            physicalSize: physicalSize,
            pageSize: pageSize,
            accessPattern: accessPattern
        };
        
        try {
            const result = await appUtils.makeAPIRequest('/api/virtual-memory/simulate', 'POST', data);
            displayResults(result);
            appUtils.showNotification('Simulation completed successfully!', 'success');
        } catch (error) {
            console.error('Simulation error:', error);
        }
    }
    
    function displayResults(result) {
        // Display metrics
        const metricsDisplay = document.getElementById('metricsDisplay');
        metricsDisplay.style.display = 'block';
        
        document.getElementById('pageHitsValue').textContent = result.page_hits;
        document.getElementById('pageFaultsValue').textContent = result.page_faults;
        document.getElementById('hitRateValue').textContent = result.hit_rate + '%';
        document.getElementById('diskWritesValue').textContent = result.disk_writes;
        document.getElementById('eatValue').textContent = result.effective_access_time.toFixed(2) + ' ns';
        document.getElementById('totalAccessesValue').textContent = result.total_accesses;
        
        // Display visualization
        const visualizationDisplay = document.getElementById('visualizationDisplay');
        visualizationDisplay.style.display = 'block';
        document.getElementById('chartImage').src = result.plot;
        
        // Display page table (only valid pages)
        displayPageTable(result.page_table);
        
        // Display access log
        displayAccessLog(result.access_log);
        
        appUtils.animateElement(metricsDisplay);
        appUtils.animateElement(visualizationDisplay);
    }
    
    function displayPageTable(pageTable) {
        const pageTableDisplay = document.getElementById('pageTableDisplay');
        const tableBody = document.getElementById('pageTableBody');
        
        pageTableDisplay.style.display = 'block';
        tableBody.innerHTML = '';
        
        // Only show pages that are in memory
        const validPages = pageTable.filter(page => page.valid);
        
        if (validPages.length === 0) {
            const row = document.createElement('tr');
            row.innerHTML = '<td colspan="5" style="text-align: center;">No pages in memory</td>';
            tableBody.appendChild(row);
            return;
        }
        
        validPages.forEach(page => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td><strong>${page.page_number}</strong></td>
                <td>${page.frame_number}</td>
                <td><span class="status-badge status-valid">Yes</span></td>
                <td><span class="status-badge ${page.dirty ? 'status-fault' : 'status-hit'}">${page.dirty ? 'Yes' : 'No'}</span></td>
                <td><span class="status-badge ${page.reference ? 'status-valid' : 'status-invalid'}">${page.reference ? 'Yes' : 'No'}</span></td>
            `;
            tableBody.appendChild(row);
        });
        
        appUtils.animateElement(pageTableDisplay);
    }
    
    function displayAccessLog(accessLog) {
        const accessLogDisplay = document.getElementById('accessLogDisplay');
        const tableBody = document.getElementById('accessLogBody');
        
        accessLogDisplay.style.display = 'block';
        tableBody.innerHTML = '';
        
        accessLog.forEach((log, index) => {
            const row = document.createElement('tr');
            
            const resultClass = log.page_fault ? 'status-fault' : 'status-hit';
            const resultText = log.result;
            
            row.innerHTML = `
                <td><strong>${index + 1}</strong></td>
                <td>${log.address}</td>
                <td>${log.page_number}</td>
                <td>${log.offset}</td>
                <td>${log.frame_number !== undefined ? log.frame_number : 'N/A'}</td>
                <td>${log.physical_address !== undefined ? log.physical_address : 'N/A'}</td>
                <td><span class="status-badge ${log.type === 'read' ? 'status-valid' : 'status-fault'}">${log.type.toUpperCase()}</span></td>
                <td><span class="status-badge ${resultClass}">${resultText}</span></td>
            `;
            tableBody.appendChild(row);
        });
        
        appUtils.animateElement(accessLogDisplay);
    }
    
    async function translateAddress() {
        const logicalAddress = parseInt(document.getElementById('logicalAddress').value);
        const pageSize = parseInt(document.getElementById('pageSize').value);
        
        if (isNaN(logicalAddress) || logicalAddress < 0) {
            appUtils.showNotification('Please enter a valid logical address', 'warning');
            return;
        }
        
        // For translation, we need a page table
        // We'll use the current simulation's page table if available
        // Otherwise, create a simple example
        
        const pageNumber = Math.floor(logicalAddress / pageSize);
        const offset = logicalAddress % pageSize;
        
        // Create a simple page table for demonstration
        const pageTable = {};
        // Assume first few pages are in memory
        for (let i = 0; i <= pageNumber; i++) {
            pageTable[i] = {
                valid: i < 4, // First 4 pages in memory
                frame_number: i < 4 ? i : null
            };
        }
        
        const data = {
            logicalAddress: logicalAddress,
            pageSize: pageSize,
            pageTable: pageTable
        };
        
        try {
            const result = await appUtils.makeAPIRequest('/api/virtual-memory/translate', 'POST', data);
            displayTranslationResult(result);
        } catch (error) {
            console.error('Translation error:', error);
        }
    }
    
    function displayTranslationResult(result) {
        const translationResult = document.getElementById('translationResult');
        translationResult.style.display = 'block';
        
        if (result.success) {
            translationResult.innerHTML = `
                <h4><i class="fas fa-check-circle" style="color: #4CAF50;"></i> Translation Successful</h4>
                <p><strong>Logical Address:</strong> ${result.logical_address} (0x${result.logical_address.toString(16).toUpperCase()})</p>
                <p><strong>Page Number:</strong> ${result.page_number}</p>
                <p><strong>Offset:</strong> ${result.offset}</p>
                <p><strong>Frame Number:</strong> ${result.frame_number}</p>
                <p><strong>Physical Address:</strong> ${result.physical_address} (0x${result.physical_address.toString(16).toUpperCase()})</p>
                ${result.binary_breakdown ? `
                    <hr style="margin: 1rem 0; border: none; border-top: 1px solid #ddd;">
                    <p><strong>Binary Breakdown:</strong></p>
                    <p style="font-family: monospace; font-size: 0.9rem;">
                        Logical: ${result.binary_breakdown.logical_binary}<br>
                        Page: ${result.binary_breakdown.page_bits} | Offset: ${result.binary_breakdown.offset_bits}<br>
                        Frame: ${result.binary_breakdown.frame_bits} | Offset: ${result.binary_breakdown.offset_bits}<br>
                        Physical: ${result.binary_breakdown.physical_binary}
                    </p>
                ` : ''}
            `;
        } else {
            translationResult.innerHTML = `
                <h4><i class="fas fa-exclamation-circle" style="color: #F44336;"></i> Translation Failed</h4>
                <p><strong>Logical Address:</strong> ${result.logical_address}</p>
                <p><strong>Error:</strong> ${result.error}</p>
            `;
        }
        
        appUtils.animateElement(translationResult);
    }
    
    function clearAll() {
        const accessPatternList = document.getElementById('accessPatternList');
        accessPatternList.innerHTML = '';
        accessPattern = [];
        
        document.getElementById('virtualSize').value = 65536;
        document.getElementById('physicalSize').value = 16384;
        document.getElementById('pageSize').value = 4096;
        document.getElementById('logicalAddress').value = '';
        
        document.getElementById('translationResult').style.display = 'none';
        
        appUtils.clearResults();
        appUtils.showNotification('All data cleared', 'info');
    }
});