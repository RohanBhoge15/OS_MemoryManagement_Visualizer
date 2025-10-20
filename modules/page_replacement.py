import time

class PageReplacementSimulator:
    def __init__(self):
        pass
    
    def simulate(self, algorithm, reference_string, frame_count):
        """
        Simulate page replacement algorithm
        """
        start_time = time.perf_counter()
        
        if algorithm == 'fifo':
            result = self._fifo(reference_string, frame_count)
        elif algorithm == 'lru':
            result = self._lru(reference_string, frame_count)
        elif algorithm == 'lfu':
            result = self._lfu(reference_string, frame_count)
        elif algorithm == 'optimal':
            result = self._optimal(reference_string, frame_count)
        else:
            result = self._fifo(reference_string, frame_count)
        
        end_time = time.perf_counter()
        execution_time = (end_time - start_time) * 1000000  # Convert to milliseconds
        
        # Calculate metrics
        total_references = len(reference_string)
        page_faults = result['page_faults']
        page_hits = total_references - page_faults
        hit_ratio = (page_hits / total_references * 100) if total_references > 0 else 0
        fault_ratio = (page_faults / total_references * 100) if total_references > 0 else 0
        
        result['algorithm'] = algorithm
        result['total_references'] = total_references
        result['page_hits'] = page_hits
        result['hit_ratio'] = round(hit_ratio, 2)
        result['fault_ratio'] = round(fault_ratio, 2)
        result['execution_time'] = round(execution_time, 2)
        
        return result
    
    def _fifo(self, reference_string, frame_count):
        """
        First In First Out (FIFO) page replacement
        """
        frames = []
        page_faults = 0
        page_sequence = []
        queue = []
        
        for page in reference_string:
            if page not in frames:
                page_faults += 1
                if len(frames) < frame_count:
                    frames.append(page)
                    queue.append(page)
                else:
                    # Replace the oldest page (first in queue)
                    old_page = queue.pop(0)
                    frames.remove(old_page)
                    frames.append(page)
                    queue.append(page)
                
                page_sequence.append({
                    'page': page,
                    'frames': frames.copy(),
                    'fault': True
                })
            else:
                page_sequence.append({
                    'page': page,
                    'frames': frames.copy(),
                    'fault': False
                })
        
        return {
            'page_faults': page_faults,
            'page_sequence': page_sequence,
            'final_frames': frames
        }
    
    def _lru(self, reference_string, frame_count):
        """
        Least Recently Used (LRU) page replacement
        """
        frames = []
        page_faults = 0
        page_sequence = []
        recent_usage = []
        
        for page in reference_string:
            if page not in frames:
                page_faults += 1
                if len(frames) < frame_count:
                    frames.append(page)
                    recent_usage.append(page)
                else:
                    # Replace the least recently used page
                    lru_page = recent_usage.pop(0)
                    frames.remove(lru_page)
                    frames.append(page)
                    recent_usage.append(page)
                
                page_sequence.append({
                    'page': page,
                    'frames': frames.copy(),
                    'fault': True
                })
            else:
                # Update recent usage
                recent_usage.remove(page)
                recent_usage.append(page)
                
                page_sequence.append({
                    'page': page,
                    'frames': frames.copy(),
                    'fault': False
                })
        
        return {
            'page_faults': page_faults,
            'page_sequence': page_sequence,
            'final_frames': frames
        }
    
    def _lfu(self, reference_string, frame_count):
        """
        Least Frequently Used (LFU) page replacement
        """
        frames = []
        page_faults = 0
        page_sequence = []
        frequency = {}
        
        for page in reference_string:
            # Update frequency
            if page in frequency:
                frequency[page] += 1
            else:
                frequency[page] = 1
            
            if page not in frames:
                page_faults += 1
                if len(frames) < frame_count:
                    frames.append(page)
                else:
                    # Replace the least frequently used page
                    lfu_page = min(frames, key=lambda p: frequency[p])
                    frames.remove(lfu_page)
                    frames.append(page)
                
                page_sequence.append({
                    'page': page,
                    'frames': frames.copy(),
                    'fault': True,
                    'frequency': frequency.copy()
                })
            else:
                page_sequence.append({
                    'page': page,
                    'frames': frames.copy(),
                    'fault': False,
                    'frequency': frequency.copy()
                })
        
        return {
            'page_faults': page_faults,
            'page_sequence': page_sequence,
            'final_frames': frames,
            'frequency': frequency
        }
    
    def _optimal(self, reference_string, frame_count):
        """
        Optimal page replacement (Belady's algorithm)
        """
        frames = []
        page_faults = 0
        page_sequence = []
        
        for i, page in enumerate(reference_string):
            if page not in frames:
                page_faults += 1
                if len(frames) < frame_count:
                    frames.append(page)
                else:
                    # Find the page that will not be used for the longest time
                    future_use = {}
                    for frame_page in frames:
                        try:
                            next_use = reference_string[i+1:].index(frame_page)
                            future_use[frame_page] = next_use
                        except ValueError:
                            # Page not used again
                            future_use[frame_page] = float('inf')
                    
                    # Replace the page with maximum future use distance
                    page_to_replace = max(future_use, key=future_use.get)
                    frames.remove(page_to_replace)
                    frames.append(page)
                
                page_sequence.append({
                    'page': page,
                    'frames': frames.copy(),
                    'fault': True
                })
            else:
                page_sequence.append({
                    'page': page,
                    'frames': frames.copy(),
                    'fault': False
                })
        
        return {
            'page_faults': page_faults,
            'page_sequence': page_sequence,
            'final_frames': frames
        }
    
    def compare_all(self, reference_string, frame_count):
        """
        Compare all page replacement algorithms
        """
        algorithms = ['fifo', 'lru', 'lfu', 'optimal']
        results = {}
        
        for algo in algorithms:
            result = self.simulate(algo, reference_string, frame_count)
            results[algo] = {
                'algorithm': algo,
                'page_faults': result['page_faults'],
                'page_hits': result['page_hits'],
                'hit_ratio': result['hit_ratio'],
                'fault_ratio': result['fault_ratio'],
                'execution_time': result['execution_time']
            }
        
        # Find best algorithm (lowest page faults, highest hit ratio)
        best_algo = min(results.keys(), key=lambda k: (
            results[k]['page_faults'],
            -results[k]['hit_ratio']
        ))
        
        results['best_algorithm'] = best_algo
        
        return results