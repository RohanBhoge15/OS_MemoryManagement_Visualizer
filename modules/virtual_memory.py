import math

class VirtualMemorySimulator:
    def __init__(self):
        pass
    
    def simulate(self, virtual_size, physical_size, page_size, access_pattern):
        """
        Simulate virtual memory management
        """
        # Calculate number of virtual pages and physical frames
        num_virtual_pages = virtual_size // page_size
        num_physical_frames = physical_size // page_size
        
        # Initialize page table (all pages initially not in memory)
        page_table = {}
        for i in range(num_virtual_pages):
            page_table[i] = {
                'page_number': i,
                'frame_number': None,
                'valid': False,
                'dirty': False,
                'reference': False
            }
        
        # Track frames
        frames = [None] * num_physical_frames
        free_frames = list(range(num_physical_frames))
        
        # Simulate access pattern
        access_log = []
        page_faults = 0
        page_hits = 0
        disk_writes = 0
        
        for access in access_pattern:
            logical_address = access['address']
            access_type = access.get('type', 'read')  # 'read' or 'write'
            
            page_number = logical_address // page_size
            offset = logical_address % page_size
            
            if page_number >= num_virtual_pages:
                access_log.append({
                    'address': logical_address,
                    'page_number': page_number,
                    'offset': offset,
                    'type': access_type,
                    'result': 'Invalid address',
                    'page_fault': False
                })
                continue
            
            page_entry = page_table[page_number]
            
            if page_entry['valid']:
                # Page hit
                page_hits += 1
                frame_number = page_entry['frame_number']
                physical_address = frame_number * page_size + offset
                page_entry['reference'] = True
                
                if access_type == 'write':
                    page_entry['dirty'] = True
                
                access_log.append({
                    'address': logical_address,
                    'page_number': page_number,
                    'offset': offset,
                    'frame_number': frame_number,
                    'physical_address': physical_address,
                    'type': access_type,
                    'result': 'Hit',
                    'page_fault': False
                })
            else:
                # Page fault
                page_faults += 1
                
                if free_frames:
                    # Allocate a free frame
                    frame_number = free_frames.pop(0)
                else:
                    # Need to replace a page (using FIFO for simplicity)
                    victim_page = None
                    for pg_num, pg_entry in page_table.items():
                        if pg_entry['valid']:
                            victim_page = pg_num
                            break
                    
                    frame_number = page_table[victim_page]['frame_number']
                    
                    # Check if victim page is dirty (needs to be written back)
                    if page_table[victim_page]['dirty']:
                        disk_writes += 1
                    
                    # Invalidate victim page
                    page_table[victim_page]['valid'] = False
                    page_table[victim_page]['frame_number'] = None
                    page_table[victim_page]['dirty'] = False
                
                # Load page into frame
                frames[frame_number] = page_number
                page_entry['frame_number'] = frame_number
                page_entry['valid'] = True
                page_entry['reference'] = True
                
                if access_type == 'write':
                    page_entry['dirty'] = True
                
                physical_address = frame_number * page_size + offset
                
                access_log.append({
                    'address': logical_address,
                    'page_number': page_number,
                    'offset': offset,
                    'frame_number': frame_number,
                    'physical_address': physical_address,
                    'type': access_type,
                    'result': 'Page Fault',
                    'page_fault': True
                })
        
        # Calculate metrics
        total_accesses = len(access_pattern)
        page_fault_rate = (page_faults / total_accesses * 100) if total_accesses > 0 else 0
        hit_rate = (page_hits / total_accesses * 100) if total_accesses > 0 else 0
        
        # Effective Access Time (EAT)
        memory_access_time = 100  # nanoseconds
        page_fault_service_time = 8000000  # 8ms in nanoseconds
        eat = (hit_rate/100) * memory_access_time + (page_fault_rate/100) * page_fault_service_time
        
        return {
            'virtual_size': virtual_size,
            'physical_size': physical_size,
            'page_size': page_size,
            'num_virtual_pages': num_virtual_pages,
            'num_physical_frames': num_physical_frames,
            'page_table': [page_table[i] for i in range(num_virtual_pages)],
            'frames': frames,
            'access_log': access_log,
            'total_accesses': total_accesses,
            'page_faults': page_faults,
            'page_hits': page_hits,
            'disk_writes': disk_writes,
            'page_fault_rate': round(page_fault_rate, 2),
            'hit_rate': round(hit_rate, 2),
            'effective_access_time': round(eat, 2)
        }
    
    def translate_address(self, logical_address, page_size, page_table):
        """
        Translate a single logical address to physical address
        """
        page_number = logical_address // page_size
        offset = logical_address % page_size
        
        # Convert page_table dict keys to integers if they're strings
        page_table_int = {int(k): v for k, v in page_table.items()}
        
        if page_number in page_table_int:
            page_entry = page_table_int[page_number]
            
            if page_entry['valid']:
                frame_number = page_entry['frame_number']
                physical_address = frame_number * page_size + offset
                
                return {
                    'logical_address': logical_address,
                    'page_number': page_number,
                    'offset': offset,
                    'frame_number': frame_number,
                    'physical_address': physical_address,
                    'success': True,
                    'binary_breakdown': {
                        'logical_binary': bin(logical_address)[2:].zfill(16),
                        'page_bits': bin(page_number)[2:].zfill(8),
                        'offset_bits': bin(offset)[2:].zfill(8),
                        'frame_bits': bin(frame_number)[2:].zfill(8),
                        'physical_binary': bin(physical_address)[2:].zfill(16)
                    }
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
                'page_number': page_number,
                'offset': offset,
                'error': 'Invalid page number',
                'success': False
            }
    
    def generate_sample_access_pattern(self, num_accesses=20, max_address=65536):
        """
        Generate a sample access pattern for testing
        """
        import random
        access_pattern = []
        
        for _ in range(num_accesses):
            access_pattern.append({
                'address': random.randint(0, max_address - 1),
                'type': random.choice(['read', 'write'])
            })
        
        return access_pattern