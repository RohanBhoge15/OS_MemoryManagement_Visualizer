// Page Replacement Algorithms Module

document.addEventListener('DOMContentLoaded', function() {
    
    // Initialize with sample data
    initializePage();
    
    // Event Listeners
    document.getElementById('loadSampleBtn').addEventListener('click', loadSampleData);
    document.getElementById('simulateBtn').addEventListener('click', runSimulation);
    document.getElementById('compareBtn').addEventListener('click', compareAlgorithms);
    document.getElementById('clearBtn').addEventListener('click', clearAll);
    
    function initializePage() {
        loadSampleData();
    }
    
    function loadSampleData() {
        document.getElementById('algorithm').value = 'fifo';
        document.getElementById('frameCount').value = 3;
        document.getElementById('referenceString').value = '7,0,1,2,0,3,0,4,2,3,0,3,2,1,2,0,1,7,0,1';
        
        appUtils.showNotification('Sample data loaded successfully!', 'success');
    }
    
    async function runSimulation() {
        const algorithm = document.getElementById('algorithm').value;
        const frameCount = parseInt(document.getElementById('frameCount').value);
        const referenceStringInput = document.getElementById('referenceString').value;
        
        // Validation
        if (!appUtils.validatePositiveNumber(frameCount, 'Frame Count')) return;
        
        const referenceString = appUtils.parseReferenceString(referenceStringInput);
        
        if (referenceString.length === 0) {
            appUtils.showNotification('Please enter a valid reference string', 'warning');
            return;
        }
        
        const data = {
            algorithm: algorithm,
            referenceString: referenceString,
            frameCount: frameCount
        };
        
        try {
            const result = await appUtils.makeAPIRequest('/api/page-replacement/simulate', 'POST', data);
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
        
        document.getElementById('pageHitsValue').textContent = result.page_hits;
        document.getElementById('pageFaultsValue').textContent = result.page_faults;
        document.getElementById('hitRatioValue').textContent = result.hit_ratio + '%';
        document.getElementById('execTimeValue').textContent = result.execution_time + ' µs';
        
        // Display visualization
        const visualizationDisplay = document.getElementById('visualizationDisplay');
        visualizationDisplay.style.display = 'block';
        document.getElementById('chartImage').src = result.plot;
        
        // Display execution trace
        displayExecutionTrace(result);
        
        appUtils.animateElement(metricsDisplay);
        appUtils.animateElement(visualizationDisplay);
    }
    
    function displayExecutionTrace(result) {
        const executionTrace = document.getElementById('executionTrace');
        const tableBody = document.getElementById('executionTraceBody');
        
        executionTrace.style.display = 'block';
        tableBody.innerHTML = '';
        
        result.page_sequence.forEach((step, index) => {
            const row = document.createElement('tr');
            
            // Format frame state
            const frameState = step.frames.length > 0 ? step.frames.join(', ') : 'Empty';
            const resultText = step.fault ? 'Page Fault' : 'Hit';
            const resultClass = step.fault ? 'status-fault' : 'status-hit';
            
            row.innerHTML = `
                <td><strong>${index + 1}</strong></td>
                <td>${step.page}</td>
                <td>[${frameState}]</td>
                <td><span class="status-badge ${resultClass}">${resultText}</span></td>
            `;
            
            tableBody.appendChild(row);
        });
        
        appUtils.animateElement(executionTrace);
    }
    
    async function compareAlgorithms() {
        const frameCount = parseInt(document.getElementById('frameCount').value);
        const referenceStringInput = document.getElementById('referenceString').value;
        
        // Validation
        if (!appUtils.validatePositiveNumber(frameCount, 'Frame Count')) return;
        
        const referenceString = appUtils.parseReferenceString(referenceStringInput);
        
        if (referenceString.length === 0) {
            appUtils.showNotification('Please enter a valid reference string', 'warning');
            return;
        }
        
        const data = {
            referenceString: referenceString,
            frameCount: frameCount
        };
        
        try {
            const result = await appUtils.makeAPIRequest('/api/page-replacement/compare', 'POST', data);
            displayComparisonResults(result);
            appUtils.showNotification('Comparison completed successfully!', 'success');
        } catch (error) {
            console.error('Comparison error:', error);
        }
    }
    
    function displayComparisonResults(data) {
        // Hide single simulation results
        document.getElementById('executionTrace').style.display = 'none';
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
        
        const algorithms = ['fifo', 'lru', 'lfu', 'optimal'];
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
                <td>${result.page_faults}</td>
                <td>${result.page_hits}</td>
                <td>${result.hit_ratio}%</td>
                <td>${result.fault_ratio}%</td>
                <td>${result.execution_time} µs</td>
            `;
            tableBody.appendChild(row);
        });
        
        // Display insights
        displayInsights(data.results);
        
        appUtils.animateElement(comparisonResults);
        appUtils.scrollToElement('comparisonResults');
    }
    
    function displayInsights(results) {
        const insightsContent = document.getElementById('insightsContent');
        const bestAlgo = results.best_algorithm;
        const bestResult = results[bestAlgo];
        const worstAlgo = getWorstAlgorithm(results);
        const worstResult = results[worstAlgo];
        
        const insights = `
            <ul style="list-style: none; padding: 0;">
                <li style="margin-bottom: 0.8rem;">
                    <i class="fas fa-star" style="color: #4CAF50; margin-right: 0.5rem;"></i>
                    <strong>${formatAlgorithmName(bestAlgo)}</strong> performed best with only <strong>${bestResult.page_faults}</strong> page faults 
                    and a hit ratio of <strong>${bestResult.hit_ratio}%</strong>.
                </li>
                <li style="margin-bottom: 0.8rem;">
                    <i class="fas fa-info-circle" style="color: #2196F3; margin-right: 0.5rem;"></i>
                    <strong>${formatAlgorithmName(worstAlgo)}</strong> had the most page faults with <strong>${worstResult.page_faults}</strong> 
                    faults and a hit ratio of <strong>${worstResult.hit_ratio}%</strong>.
                </li>
                <li style="margin-bottom: 0.8rem;">
                    <i class="fas fa-chart-line" style="color: #FF9800; margin-right: 0.5rem;"></i>
                    The performance difference is <strong>${worstResult.page_faults - bestResult.page_faults}</strong> page faults, 
                    representing a <strong>${((worstResult.page_faults - bestResult.page_faults) / worstResult.page_faults * 100).toFixed(1)}%</strong> improvement.
                </li>
                <li>
                    <i class="fas fa-lightbulb" style="color: #FFC107; margin-right: 0.5rem;"></i>
                    ${getAlgorithmRecommendation(bestAlgo)}
                </li>
            </ul>
        `;
        
        insightsContent.innerHTML = insights;
    }
    
    function getWorstAlgorithm(results) {
        const algorithms = ['fifo', 'lru', 'lfu', 'optimal'];
        let worstAlgo = algorithms[0];
        let maxFaults = results[algorithms[0]].page_faults;
        
        algorithms.forEach(algo => {
            if (results[algo].page_faults > maxFaults) {
                maxFaults = results[algo].page_faults;
                worstAlgo = algo;
            }
        });
        
        return worstAlgo;
    }
    
    function getAlgorithmRecommendation(algo) {
        const recommendations = {
            'fifo': 'FIFO is simple to implement but may suffer from Belady\'s anomaly. Consider LRU for better performance in most cases.',
            'lru': 'LRU provides excellent performance and is widely used in practice. It approximates optimal behavior well.',
            'lfu': 'LFU works well when pages have distinct access frequencies. However, it may retain old pages unnecessarily.',
            'optimal': 'Optimal algorithm provides the theoretical best performance but requires future knowledge, making it impractical for real systems.'
        };
        return recommendations[algo] || '';
    }
    
    function formatAlgorithmName(algo) {
        const names = {
            'fifo': 'FIFO',
            'lru': 'LRU',
            'lfu': 'LFU',
            'optimal': 'Optimal'
        };
        return names[algo] || algo;
    }
    
    function clearAll() {
        document.getElementById('algorithm').value = 'fifo';
        document.getElementById('frameCount').value = 3;
        document.getElementById('referenceString').value = '';
        
        appUtils.clearResults();
        appUtils.showNotification('All data cleared', 'info');
    }
});