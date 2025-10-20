class ContinuousMemoryAllocator:
    def __init__(self):
        self.memory = []
        self.processes = []
    
    def simulate(self, memory_size, processes, partition_type, algorithm):
        """
        Simulate continuous memory allocation
        """
        if partition_type == 'fixed':
            return self._fixed_partitioning(memory_size, processes, algorithm)
        else:
            return self._variable_partitioning(memory_size, processes, algorithm)
    
    def _fixed_partitioning(self, memory_size, processes, algorithm):
        """
        Fixed partitioning with equal-sized partitions
        """
        num_partitions = len(processes) + 2
        partition_size = memory_size // num_partitions
        partitions = [{'size': partition_size, 'allocated': None} for _ in range(num_partitions)]
        
        allocated_processes = []
        unallocated_processes = []
        internal_fragmentation = 0
        
        for process in processes:
            allocated = False
            for i, partition in enumerate(partitions):
                if partition['allocated'] is None and partition['size'] >= process['size']:
                    partition['allocated'] = process['id']
                    allocated_processes.append({
                        'id': process['id'],
                        'size': process['size'],
                        'partition': i,
                        'partition_size': partition['size']
                    })
                    internal_fragmentation += (partition['size'] - process['size'])
                    allocated = True
                    break
            
            if not allocated:
                unallocated_processes.append(process)
        
        memory_map = self._create_memory_map_fixed(partitions, partition_size)
        total_allocated = sum(p['size'] for p in allocated_processes)
        memory_utilization = (total_allocated / memory_size) * 100 if memory_size > 0 else 0
        
        return {
            'algorithm': algorithm,
            'partition_type': 'fixed',
            'allocated': allocated_processes,
            'unallocated': unallocated_processes,
            'internal_fragmentation': internal_fragmentation,
            'external_fragmentation': 0,
            'memory_utilization': round(memory_utilization, 2),
            'memory_map': memory_map,
            'total_memory': memory_size
        }
    
    def _variable_partitioning(self, memory_size, processes, algorithm):
        """
        Variable partitioning using First Fit, Best Fit, or Worst Fit
        """
        memory_blocks = [{'start': 0, 'size': memory_size, 'allocated': None}]
        allocated_processes = []
        unallocated_processes = []
        
        for process in processes:
            block_index = None
            
            if algorithm == 'first_fit':
                block_index = self._first_fit(memory_blocks, process['size'])
            elif algorithm == 'best_fit':
                block_index = self._best_fit(memory_blocks, process['size'])
            elif algorithm == 'worst_fit':
                block_index = self._worst_fit(memory_blocks, process['size'])
            
            if block_index is not None:
                block = memory_blocks[block_index]
                allocated_processes.append({
                    'id': process['id'],
                    'size': process['size'],
                    'start': block['start'],
                    'end': block['start'] + process['size']
                })
                
                # Split the block
                remaining_size = block['size'] - process['size']
                memory_blocks[block_index] = {
                    'start': block['start'],
                    'size': process['size'],
                    'allocated': process['id']
                }
                
                if remaining_size > 0:
                    memory_blocks.insert(block_index + 1, {
                        'start': block['start'] + process['size'],
                        'size': remaining_size,
                        'allocated': None
                    })
            else:
                unallocated_processes.append(process)
        
        # Calculate fragmentation
        external_fragmentation = sum(block['size'] for block in memory_blocks if block['allocated'] is None)
        total_allocated = sum(p['size'] for p in allocated_processes)
        memory_utilization = (total_allocated / memory_size) * 100 if memory_size > 0 else 0
        
        memory_map = self._create_memory_map_variable(memory_blocks, memory_size)
        
        return {
            'algorithm': algorithm,
            'partition_type': 'variable',
            'allocated': allocated_processes,
            'unallocated': unallocated_processes,
            'internal_fragmentation': 0,
            'external_fragmentation': external_fragmentation,
            'memory_utilization': round(memory_utilization, 2),
            'memory_map': memory_map,
            'memory_blocks': memory_blocks,
            'total_memory': memory_size
        }
    
    def _first_fit(self, memory_blocks, size):
        """First Fit: Allocate the first block that is large enough"""
        for i, block in enumerate(memory_blocks):
            if block['allocated'] is None and block['size'] >= size:
                return i
        return None
    
    def _best_fit(self, memory_blocks, size):
        """Best Fit: Allocate the smallest block that is large enough"""
        best_index = None
        best_size = float('inf')
        
        for i, block in enumerate(memory_blocks):
            if block['allocated'] is None and block['size'] >= size:
                if block['size'] < best_size:
                    best_size = block['size']
                    best_index = i
        
        return best_index
    
    def _worst_fit(self, memory_blocks, size):
        """Worst Fit: Allocate the largest block"""
        worst_index = None
        worst_size = -1
        
        for i, block in enumerate(memory_blocks):
            if block['allocated'] is None and block['size'] >= size:
                if block['size'] > worst_size:
                    worst_size = block['size']
                    worst_index = i
        
        return worst_index
    
    def _create_memory_map_fixed(self, partitions, partition_size):
        """Create memory map for fixed partitioning"""
        memory_map = []
        for i, partition in enumerate(partitions):
            memory_map.append({
                'start': i * partition_size,
                'end': (i + 1) * partition_size,
                'size': partition_size,
                'process': partition['allocated'],
                'type': 'allocated' if partition['allocated'] else 'free'
            })
        return memory_map
    
    def _create_memory_map_variable(self, memory_blocks, total_memory):
        """Create memory map for variable partitioning"""
        memory_map = []
        for block in memory_blocks:
            memory_map.append({
                'start': block['start'],
                'end': block['start'] + block['size'],
                'size': block['size'],
                'process': block['allocated'],
                'type': 'allocated' if block['allocated'] else 'free'
            })
        return memory_map
    
    def compare_all(self, memory_size, processes, partition_type):
        """Compare all allocation algorithms"""
        algorithms = ['first_fit', 'best_fit', 'worst_fit']
        results = {}
        
        for algo in algorithms:
            result = self.simulate(memory_size, processes, partition_type, algo)
            results[algo] = {
                'algorithm': algo,
                'memory_utilization': result['memory_utilization'],
                'internal_fragmentation': result['internal_fragmentation'],
                'external_fragmentation': result['external_fragmentation'],
                'allocated_count': len(result['allocated']),
                'unallocated_count': len(result['unallocated']),
                'total_fragmentation': result['internal_fragmentation'] + result['external_fragmentation']
            }
        
        # Find best algorithm (highest utilization, lowest fragmentation)
        best_algo = max(results.keys(), key=lambda k: (
            results[k]['memory_utilization'],
            -results[k]['total_fragmentation']
        ))
        
        results['best_algorithm'] = best_algo
        
        return results