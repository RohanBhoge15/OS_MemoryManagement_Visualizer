import random

class HelperFunctions:
    
    @staticmethod
    def generate_sample_processes(count=5, min_size=50, max_size=300):
        """
        Generate sample processes for continuous memory allocation
        """
        processes = []
        for i in range(count):
            processes.append({
                'id': f'P{i+1}',
                'size': random.randint(min_size, max_size)
            })
        return processes
    
    @staticmethod
    def generate_sample_segments(count=4):
        """
        Generate sample segments for segmentation
        """
        segment_names = ['Code', 'Data', 'Stack', 'Heap', 'Shared', 'Library']
        segments = []
        sizes = [512, 768, 256, 1024, 384, 640]
        
        for i in range(min(count, len(segment_names))):
            segments.append({
                'name': segment_names[i],
                'size': sizes[i]
            })
        return segments
    
    @staticmethod
    def generate_reference_string(length=20, max_page=9):
        """
        Generate sample reference string for page replacement algorithms
        """
        return [random.randint(0, max_page) for _ in range(length)]
    
    @staticmethod
    def generate_access_pattern(num_accesses=20, max_address=65535):
        """
        Generate sample access pattern for virtual memory
        """
        access_pattern = []
        for _ in range(num_accesses):
            access_pattern.append({
                'address': random.randint(0, max_address),
                'type': random.choice(['read', 'write'])
            })
        return access_pattern
    
    @staticmethod
    def format_bytes(bytes_value):
        """
        Format bytes to human-readable format
        """
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if bytes_value < 1024.0:
                return f"{bytes_value:.2f} {unit}"
            bytes_value /= 1024.0
        return f"{bytes_value:.2f} PB"
    
    @staticmethod
    def calculate_fragmentation_percentage(fragmentation, total_memory):
        """
        Calculate fragmentation as percentage
        """
        if total_memory == 0:
            return 0
        return (fragmentation / total_memory) * 100
    
    @staticmethod
    def get_sample_data(data_type):
        """
        Get predefined sample data based on type
        """
        if data_type == 'continuous':
            return {
                'memorySize': 1000,
                'processes': [
                    {'id': 'P1', 'size': 212},
                    {'id': 'P2', 'size': 417},
                    {'id': 'P3', 'size': 112},
                    {'id': 'P4', 'size': 426}
                ],
                'partitionType': 'variable'
            }
        
        elif data_type == 'paging':
            return {
                'memorySize': 4096,
                'processSize': 3000,
                'pageSize': 512
            }
        
        elif data_type == 'segmentation':
            return {
                'memorySize': 4096,
                'segments': [
                    {'name': 'Code', 'size': 1024},
                    {'name': 'Data', 'size': 768},
                    {'name': 'Stack', 'size': 512},
                    {'name': 'Heap', 'size': 896}
                ]
            }
        
        elif data_type == 'page_replacement':
            return {
                'referenceString': [7, 0, 1, 2, 0, 3, 0, 4, 2, 3, 0, 3, 2, 1, 2, 0, 1, 7, 0, 1],
                'frameCount': 3
            }
        
        elif data_type == 'virtual_memory':
            return {
                'virtualSize': 65536,
                'physicalSize': 16384,
                'pageSize': 4096,
                'accessPattern': [
                    {'address': 8192, 'type': 'read'},
                    {'address': 12288, 'type': 'write'},
                    {'address': 8192, 'type': 'read'},
                    {'address': 20480, 'type': 'read'},
                    {'address': 0, 'type': 'write'},
                    {'address': 8192, 'type': 'read'},
                    {'address': 4096, 'type': 'read'},
                    {'address': 20480, 'type': 'write'},
                    {'address': 12288, 'type': 'read'},
                    {'address': 16384, 'type': 'read'}
                ]
            }
        
        return {}