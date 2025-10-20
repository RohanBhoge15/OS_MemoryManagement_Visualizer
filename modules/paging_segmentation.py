import math

class PagingSegmentation:
    def __init__(self):
        pass
    
    def simulate_paging(self, memory_size, process_size, page_size):
        """
        Simulate paging memory management
        """
        # Calculate number of pages and frames
        num_pages = math.ceil(process_size / page_size)
        num_frames = memory_size // page_size
        
        # Create page table
        page_table = []
        frames_used = []
        
        for page_num in range(num_pages):
            if page_num < num_frames:
                frame_num = page_num
                frames_used.append(frame_num)
                page_table.append({
                    'page_number': page_num,
                    'frame_number': frame_num,
                    'valid': True,
                    'page_address': page_num * page_size,
                    'physical_address': frame_num * page_size
                })
            else:
                page_table.append({
                    'page_number': page_num,
                    'frame_number': None,
                    'valid': False,
                    'page_address': page_num * page_size,
                    'physical_address': None
                })
        
        # Calculate metrics
        internal_fragmentation = 0
        if process_size % page_size != 0:
            internal_fragmentation = page_size - (process_size % page_size)
        
        memory_used = min(num_pages, num_frames) * page_size
        memory_utilization = (process_size / memory_size) * 100 if memory_size > 0 else 0
        
        # Calculate page fault probability (pages not in memory)
        pages_in_memory = min(num_pages, num_frames)
        page_fault_probability = ((num_pages - pages_in_memory) / num_pages * 100) if num_pages > 0 else 0
        
        return {
            'mode': 'paging',
            'memory_size': memory_size,
            'process_size': process_size,
            'page_size': page_size,
            'num_pages': num_pages,
            'num_frames': num_frames,
            'frames_used': len(frames_used),
            'page_table': page_table,
            'internal_fragmentation': internal_fragmentation,
            'external_fragmentation': 0,
            'memory_utilization': round(memory_utilization, 2),
            'page_fault_probability': round(page_fault_probability, 2),
            'access_efficiency': round(100 - page_fault_probability, 2)
        }
    
    def simulate_segmentation(self, memory_size, segments):
        """
        Simulate segmentation memory management
        """
        segment_table = []
        current_base = 0
        total_segment_size = 0
        allocated_segments = []
        unallocated_segments = []
        
        for i, segment in enumerate(segments):
            seg_size = segment['size']
            seg_name = segment.get('name', f'Segment {i}')
            
            if current_base + seg_size <= memory_size:
                segment_table.append({
                    'segment_number': i,
                    'segment_name': seg_name,
                    'base_address': current_base,
                    'limit': seg_size,
                    'end_address': current_base + seg_size,
                    'allocated': True
                })
                allocated_segments.append({
                    'number': i,
                    'name': seg_name,
                    'size': seg_size
                })
                current_base += seg_size
                total_segment_size += seg_size
            else:
                segment_table.append({
                    'segment_number': i,
                    'segment_name': seg_name,
                    'base_address': None,
                    'limit': seg_size,
                    'end_address': None,
                    'allocated': False
                })
                unallocated_segments.append({
                    'number': i,
                    'name': seg_name,
                    'size': seg_size
                })
        
        # Calculate metrics
        external_fragmentation = memory_size - total_segment_size
        memory_utilization = (total_segment_size / memory_size) * 100 if memory_size > 0 else 0
        
        # Segment overhead (segment table size)
        segment_overhead = len(segment_table) * 8  # Assume 8 bytes per segment table entry
        
        return {
            'mode': 'segmentation',
            'memory_size': memory_size,
            'total_segments': len(segments),
            'allocated_segments': len(allocated_segments),
            'segment_table': segment_table,
            'allocated': allocated_segments,
            'unallocated': unallocated_segments,
            'internal_fragmentation': 0,
            'external_fragmentation': external_fragmentation,
            'memory_utilization': round(memory_utilization, 2),
            'segment_overhead': segment_overhead,
            'access_efficiency': round(memory_utilization, 2)
        }
    
    def translate_logical_to_physical_paging(self, logical_address, page_size, page_table):
        """
        Translate logical address to physical address in paging
        """
        page_number = logical_address // page_size
        offset = logical_address % page_size
        
        if page_number < len(page_table):
            page_entry = page_table[page_number]
            if page_entry['valid']:
                frame_number = page_entry['frame_number']
                physical_address = frame_number * page_size + offset
                return {
                    'logical_address': logical_address,
                    'page_number': page_number,
                    'offset': offset,
                    'frame_number': frame_number,
                    'physical_address': physical_address,
                    'success': True
                }
            else:
                return {
                    'logical_address': logical_address,
                    'page_number': page_number,
                    'offset': offset,
                    'error': 'Page fault - Page not in memory',
                    'success': False
                }
        else:
            return {
                'logical_address': logical_address,
                'error': 'Invalid page number',
                'success': False
            }
    
    def translate_logical_to_physical_segmentation(self, segment_number, offset, segment_table):
        """
        Translate logical address to physical address in segmentation
        """
        if segment_number < len(segment_table):
            segment = segment_table[segment_number]
            
            if not segment['allocated']:
                return {
                    'segment_number': segment_number,
                    'offset': offset,
                    'error': 'Segment not allocated',
                    'success': False
                }
            
            if offset >= segment['limit']:
                return {
                    'segment_number': segment_number,
                    'offset': offset,
                    'error': 'Segmentation fault - Offset exceeds limit',
                    'success': False
                }
            
            physical_address = segment['base_address'] + offset
            return {
                'segment_number': segment_number,
                'offset': offset,
                'base_address': segment['base_address'],
                'limit': segment['limit'],
                'physical_address': physical_address,
                'success': True
            }
        else:
            return {
                'segment_number': segment_number,
                'offset': offset,
                'error': 'Invalid segment number',
                'success': False
            }