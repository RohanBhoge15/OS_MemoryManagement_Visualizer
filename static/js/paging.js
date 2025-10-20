// Paging and Segmentation Module

document.addEventListener('DOMContentLoaded', function() {
    let segments = [];
    
    // Initialize with sample data
    initializePage();
    
    // Event Listeners
    document.getElementById('mode').addEventListener('change', toggleMode);
    document.getElementById('addSegmentBtn').addEventListener('click', addSegment);
    document.getElementById('loadSampleBtn').addEventListener('click', loadSampleData);
    document.getElementById('simulateBtn').addEventListener('click', runSimulation);
    document.getElementById('compareBtn').addEventListener('click', compareApproaches);
    document.getElementById('clearBtn').addEventListener('click', clearAll);
    
    function initializePage() {
        loadSampleData();
    }
    
    function toggleMode() {
        const mode = document.getElementById('mode').value;
        const pagingConfig = document.getElementById('pagingConfig');
        const segmentationConfig = document.getElementById('segmentationConfig');
        
        if (mode === 'paging') {
            pagingConfig.style.display = 'block';
            segmentationConfig.style.display = 'none';
        } else {
            pagingConfig.style.display = 'none';
            segmentationConfig.style.display = 'block';
        }
    }
    
    function addSegment(name = null, size = null) {
        const segmentList = document.getElementById('segmentList');
        const segmentName = name || `Segment ${segments.length + 1}`;
        const segmentSize = size || 512;
        
        const segmentItem = document.createElement('div');
        segmentItem.className = 'segment-item fade-in';
        segmentItem.innerHTML = `
            <input type="text" class="segment-name" placeholder="Segment Name" value="${segmentName}">
            <input type="number" class="segment-size" placeholder="Size (bytes)" value="${segmentSize}" min="1">
            <button class="remove-btn" onclick="removeSegment(this)">
                <i class="fas fa-times"></i>
            </button>
        `;
        
        segmentList.appendChild(segmentItem);
        segments.push({ name: segmentName, size: segmentSize });
    }
    
    window.removeSegment = function(button) {
        const segmentItem = button.parentElement;
        segmentItem.remove();
        updateSegmentsArray();
    };
    
    function updateSegmentsArray() {
        segments = [];
        const segmentItems = document.querySelectorAll('.segment-item');
        segmentItems.forEach(item => {
            const name = item.querySelector('.segment-name').value;
            const size = parseInt(item.querySelector('.segment-size').value);
            if (name && size > 0) {
                segments.push({ name, size });
            }
        });
    }
    
    function loadSampleData() {
        const mode = document.getElementById('mode').value;
        
        if (mode === 'paging') {
            document.getElementById('memorySize').value = 4096;
            document.getElementById('processSize').value = 3000;
            document.getElementById('pageSize').value = 512;
        } else {
            const segmentList = document.getElementById('segmentList');
            segmentList.innerHTML = '';
            segments = [];
            
            const sampleSegments = [
                { name: 'Code', size: 1024 },
                { name: 'Data', size: 768 },
                { name: 'Stack', size: 512 },
                { name: 'Heap', size: 896 }
            ];
            
            sampleSegments.forEach(s => addSegment(s.name, s.size));
            document.getElementById('segMemorySize').value = 4096;
        }
        
        appUtils.showNotification('Sample data loaded successfully!', 'success');
    }
    
    async function runSimulation() {
        const mode = document.getElementById('mode').value;
        let data = { mode: mode };
        
        if (mode === 'paging') {
            const memorySize = parseInt(document.getElementById('memorySize').value);
            const processSize = parseInt(document.getElementById('processSize').value);
            const pageSize = parseInt(document.getElementById('pageSize').value);
            
            // Validation
            if (!appUtils.validatePositiveNumber(memorySize, 'Memory Size')) return;
            if (!appUtils.validatePositiveNumber(processSize, 'Process Size')) return;
            if (!appUtils.validatePositiveNumber(pageSize, 'Page Size')) return;
            
            data.memorySize = memorySize;
            data.processSize = processSize;
            data.pageSize = pageSize;
        } else {
            updateSegmentsArray();
            const memorySize = parseInt(document.getElementById('segMemorySize').value);
            
            // Validation
            if (!appUtils.validatePositiveNumber(memorySize, 'Memory Size')) return;
            if (segments.length === 0) {
                appUtils.showNotification('Please add at least one segment', 'warning');
                return;
            }
            
            data.memorySize = memorySize;
            data.segments = segments;
        }
        
        try {
            const result = await appUtils.makeAPIRequest('/api/paging/simulate', 'POST', data);
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
        
        if (result.mode === 'paging') {
            document.getElementById('fragmentationValue').textContent = result.internal_fragmentation + ' bytes';
            document.getElementById('tableLabel').textContent = 'Pages in Memory';
            document.getElementById('tableCount').textContent = result.frames_used + '/' + result.num_frames;
        } else {
            document.getElementById('fragmentationValue').textContent = result.external_fragmentation + ' bytes';
            document.getElementById('tableLabel').textContent = 'Segments Allocated';
            document.getElementById('tableCount').textContent = result.allocated_segments + '/' + result.total_segments;
        }
        
        document.getElementById('efficiencyValue').textContent = result.access_efficiency + '%';
        
        // Display visualization
        const visualizationDisplay = document.getElementById('visualizationDisplay');
        visualizationDisplay.style.display = 'block';
        document.getElementById('chartImage').src = result.plot;
        
        // Display table
        if (result.mode === 'paging') {
            displayPageTable(result.page_table);
            document.getElementById('segmentTableDisplay').style.display = 'none';
        } else {
            displaySegmentTable(result.segment_table);
            document.getElementById('pageTableDisplay').style.display = 'none';
        }
        
        appUtils.animateElement(metricsDisplay);
        appUtils.animateElement(visualizationDisplay);
    }
    
    function displayPageTable(pageTable) {
        const pageTableDisplay = document.getElementById('pageTableDisplay');
        const tableBody = document.getElementById('pageTableBody');
        
        pageTableDisplay.style.display = 'block';
        tableBody.innerHTML = '';
        
        pageTable.forEach(page => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td><strong>${page.page_number}</strong></td>
                <td>${page.frame_number !== null ? page.frame_number : 'N/A'}</td>
                <td><span class="status-badge status-${page.valid ? 'valid' : 'invalid'}">${page.valid ? 'Valid' : 'Invalid'}</span></td>
                <td>${page.page_address}</td>
                <td>${page.physical_address !== null ? page.physical_address : 'N/A'}</td>
            `;
            tableBody.appendChild(row);
        });
        
        appUtils.animateElement(pageTableDisplay);
    }
    
    function displaySegmentTable(segmentTable) {
        const segmentTableDisplay = document.getElementById('segmentTableDisplay');
        const tableBody = document.getElementById('segmentTableBody');
        
        segmentTableDisplay.style.display = 'block';
        tableBody.innerHTML = '';
        
        segmentTable.forEach(segment => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td><strong>${segment.segment_number}</strong></td>
                <td>${segment.segment_name}</td>
                <td>${segment.base_address !== null ? segment.base_address : 'N/A'}</td>
                <td>${segment.limit} bytes</td>
                <td>${segment.end_address !== null ? segment.end_address : 'N/A'}</td>
                <td><span class="status-badge status-${segment.allocated ? 'allocated' : 'free'}">${segment.allocated ? 'Allocated' : 'Not Allocated'}</span></td>
            `;
            tableBody.appendChild(row);
        });
        
        appUtils.animateElement(segmentTableDisplay);
    }
    
    async function compareApproaches() {
        // Get paging parameters
        const memorySize = parseInt(document.getElementById('memorySize').value);
        const processSize = parseInt(document.getElementById('processSize').value);
        const pageSize = parseInt(document.getElementById('pageSize').value);
        
        // Get segmentation parameters
        updateSegmentsArray();
        
        // Validation
        if (!appUtils.validatePositiveNumber(memorySize, 'Memory Size')) return;
        if (!appUtils.validatePositiveNumber(processSize, 'Process Size')) return;
        if (!appUtils.validatePositiveNumber(pageSize, 'Page Size')) return;
        if (segments.length === 0) {
            appUtils.showNotification('Please add segments for comparison', 'warning');
            return;
        }
        
        const data = {
            memorySize: memorySize,
            processSize: processSize,
            pageSize: pageSize,
            segments: segments
        };
        
        try {
            const result = await appUtils.makeAPIRequest('/api/paging/compare', 'POST', data);
            displayComparisonResults(result);
            appUtils.showNotification('Comparison completed successfully!', 'success');
        } catch (error) {
            console.error('Comparison error:', error);
        }
    }
    
    function displayComparisonResults(data) {
        // Hide single simulation results
        document.getElementById('pageTableDisplay').style.display = 'none';
        document.getElementById('segmentTableDisplay').style.display = 'none';
        document.getElementById('visualizationDisplay').style.display = 'none';
        document.getElementById('metricsDisplay').style.display = 'none';
        
        const comparisonResults = document.getElementById('comparisonResults');
        comparisonResults.style.display = 'block';
        
        // Determine better approach
        const betterApproach = data.paging.memory_utilization > data.segmentation.memory_utilization ? 'Paging' : 'Segmentation';
        
        const bestApproachBanner = document.getElementById('bestApproachBanner');
        const bestApproachName = document.getElementById('bestApproachName');
        bestApproachBanner.style.display = 'flex';
        bestApproachName.textContent = betterApproach;
        
        // Display comparison chart
        document.getElementById('comparisonChart').src = data.plot;
        
        // Update comparison summary
        document.getElementById('pagingUtilization').textContent = data.paging.memory_utilization + '%';
        document.getElementById('pagingFragmentation').textContent = data.paging.internal_fragmentation + ' bytes';
        document.getElementById('pagingEfficiency').textContent = data.paging.access_efficiency + '%';
        
        document.getElementById('segmentationUtilization').textContent = data.segmentation.memory_utilization + '%';
        document.getElementById('segmentationFragmentation').textContent = data.segmentation.external_fragmentation + ' bytes';
        document.getElementById('segmentationEfficiency').textContent = data.segmentation.access_efficiency + '%';
        
        appUtils.animateElement(comparisonResults);
        appUtils.scrollToElement('comparisonResults');
    }
    
    function clearAll() {
        document.getElementById('memorySize').value = 4096;
        document.getElementById('processSize').value = 3000;
        document.getElementById('pageSize').value = 512;
        document.getElementById('segMemorySize').value = 4096;
        
        const segmentList = document.getElementById('segmentList');
        segmentList.innerHTML = '';
        segments = [];
        
        document.getElementById('mode').value = 'paging';
        toggleMode();
        
        appUtils.clearResults();
        appUtils.showNotification('All data cleared', 'info');
    }
});