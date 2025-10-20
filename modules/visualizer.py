import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

class Visualizer:
    def __init__(self):
        plt.style.use('default')
    
    def plot_memory_allocation(self, memory_map, total_memory):
        """
        Visualize memory allocation for continuous allocation
        """
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
        
        # Memory Map Visualization
        colors = {'allocated': '#4CAF50', 'free': '#FFC107'}
        y_pos = 0
        
        for block in memory_map:
            height = block['size']
            color = colors[block['type']]
            label = f"P{block['process']}" if block['process'] else 'Free'
            
            ax1.barh(0, block['size'], left=block['start'], height=0.5, 
                    color=color, edgecolor='black', linewidth=1.5)
            
            # Add text label in the middle of the block
            mid_point = block['start'] + block['size'] / 2
            ax1.text(mid_point, 0, label, ha='center', va='center', 
                    fontsize=10, fontweight='bold')
        
        ax1.set_xlim(0, total_memory)
        ax1.set_ylim(-0.5, 0.5)
        ax1.set_xlabel('Memory Address', fontsize=12)
        ax1.set_title('Memory Allocation Map', fontsize=14, fontweight='bold')
        ax1.set_yticks([])
        ax1.grid(axis='x', alpha=0.3)
        
        # Create legend
        allocated_patch = mpatches.Patch(color='#4CAF50', label='Allocated')
        free_patch = mpatches.Patch(color='#FFC107', label='Free')
        ax1.legend(handles=[allocated_patch, free_patch], loc='upper right')
        
        # Pie Chart for Memory Utilization
        allocated_size = sum(block['size'] for block in memory_map if block['type'] == 'allocated')
        free_size = total_memory - allocated_size
        
        sizes = [allocated_size, free_size]
        labels = ['Allocated', 'Free']
        colors_pie = ['#4CAF50', '#FFC107']
        explode = (0.05, 0)
        
        ax2.pie(sizes, explode=explode, labels=labels, colors=colors_pie, autopct='%1.1f%%',
                shadow=True, startangle=90, textprops={'fontsize': 12, 'fontweight': 'bold'})
        ax2.set_title('Memory Utilization', fontsize=14, fontweight='bold')
        
        plt.tight_layout()
        return fig
    
    def plot_comparison_continuous(self, results):
        """
        Compare continuous allocation algorithms
        """
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))
        
        algorithms = [algo for algo in results.keys() if algo != 'best_algorithm']
        best_algo = results.get('best_algorithm', '')
        
        # Extract metrics
        utilization = [results[algo]['memory_utilization'] for algo in algorithms]
        internal_frag = [results[algo]['internal_fragmentation'] for algo in algorithms]
        external_frag = [results[algo]['external_fragmentation'] for algo in algorithms]
        total_frag = [results[algo]['total_fragmentation'] for algo in algorithms]
        
        # Colors with highlight for best algorithm
        colors = ['#2196F3' if algo != best_algo else '#4CAF50' for algo in algorithms]
        
        # Memory Utilization
        bars1 = ax1.bar(algorithms, utilization, color=colors, edgecolor='black', linewidth=1.5)
        ax1.set_ylabel('Utilization (%)', fontsize=12, fontweight='bold')
        ax1.set_title('Memory Utilization Comparison', fontsize=13, fontweight='bold')
        ax1.set_ylim(0, 100)
        ax1.grid(axis='y', alpha=0.3)
        
        for i, bar in enumerate(bars1):
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.1f}%', ha='center', va='bottom', fontweight='bold')
        
        # Internal Fragmentation
        bars2 = ax2.bar(algorithms, internal_frag, color=colors, edgecolor='black', linewidth=1.5)
        ax2.set_ylabel('Fragmentation (bytes)', fontsize=12, fontweight='bold')
        ax2.set_title('Internal Fragmentation', fontsize=13, fontweight='bold')
        ax2.grid(axis='y', alpha=0.3)
        
        for i, bar in enumerate(bars2):
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(height)}', ha='center', va='bottom', fontweight='bold')
        
        # External Fragmentation
        bars3 = ax3.bar(algorithms, external_frag, color=colors, edgecolor='black', linewidth=1.5)
        ax3.set_ylabel('Fragmentation (bytes)', fontsize=12, fontweight='bold')
        ax3.set_title('External Fragmentation', fontsize=13, fontweight='bold')
        ax3.grid(axis='y', alpha=0.3)
        
        for i, bar in enumerate(bars3):
            height = bar.get_height()
            ax3.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(height)}', ha='center', va='bottom', fontweight='bold')
        
        # Total Fragmentation
        bars4 = ax4.bar(algorithms, total_frag, color=colors, edgecolor='black', linewidth=1.5)
        ax4.set_ylabel('Fragmentation (bytes)', fontsize=12, fontweight='bold')
        ax4.set_title('Total Fragmentation', fontsize=13, fontweight='bold')
        ax4.grid(axis='y', alpha=0.3)
        
        for i, bar in enumerate(bars4):
            height = bar.get_height()
            ax4.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(height)}', ha='center', va='bottom', fontweight='bold')
        
        # Add best algorithm annotation
        fig.suptitle(f'Algorithm Comparison (Best: {best_algo.upper().replace("_", " ")})', 
                    fontsize=16, fontweight='bold', color='#4CAF50')
        
        plt.tight_layout()
        return fig
    
    def plot_paging_segmentation(self, result, mode):
        """
        Visualize paging or segmentation
        """
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
        
        if mode == 'paging':
            # Page Table Visualization
            page_table = result['page_table']
            valid_pages = [p for p in page_table if p['valid']]
            invalid_pages = [p for p in page_table if not p['valid']]
            
            valid_count = len(valid_pages)
            invalid_count = len(invalid_pages)
            
            # Bar chart for page status
            categories = ['Pages in Memory', 'Pages Not in Memory']
            values = [valid_count, invalid_count]
            colors_bar = ['#4CAF50', '#F44336']
            
            bars = ax1.bar(categories, values, color=colors_bar, edgecolor='black', linewidth=1.5)
            ax1.set_ylabel('Number of Pages', fontsize=12, fontweight='bold')
            ax1.set_title('Page Distribution', fontsize=14, fontweight='bold')
            ax1.grid(axis='y', alpha=0.3)
            
            for bar in bars:
                height = bar.get_height()
                ax1.text(bar.get_x() + bar.get_width()/2., height,
                        f'{int(height)}', ha='center', va='bottom', fontweight='bold', fontsize=12)
            
            # Metrics visualization
            metrics = ['Memory\nUtilization', 'Internal\nFragmentation', 'Access\nEfficiency']
            values_metrics = [
                result['memory_utilization'],
                (result['internal_fragmentation'] / result['page_size'] * 100) if result['page_size'] > 0 else 0,
                result['access_efficiency']
            ]
            
            colors_metrics = ['#2196F3', '#FF9800', '#9C27B0']
            bars2 = ax2.bar(metrics, values_metrics, color=colors_metrics, edgecolor='black', linewidth=1.5)
            ax2.set_ylabel('Percentage (%)', fontsize=12, fontweight='bold')
            ax2.set_title('Paging Metrics', fontsize=14, fontweight='bold')
            ax2.set_ylim(0, 100)
            ax2.grid(axis='y', alpha=0.3)
            
            for bar in bars2:
                height = bar.get_height()
                ax2.text(bar.get_x() + bar.get_width()/2., height,
                        f'{height:.1f}%', ha='center', va='bottom', fontweight='bold')
        
        else:  # segmentation
            # Segment allocation visualization
            allocated = result['allocated_segments']
            unallocated = len(result['unallocated'])
            
            categories = ['Allocated Segments', 'Unallocated Segments']
            values = [allocated, unallocated]
            colors_bar = ['#4CAF50', '#F44336']
            
            bars = ax1.bar(categories, values, color=colors_bar, edgecolor='black', linewidth=1.5)
            ax1.set_ylabel('Number of Segments', fontsize=12, fontweight='bold')
            ax1.set_title('Segment Distribution', fontsize=14, fontweight='bold')
            ax1.grid(axis='y', alpha=0.3)
            
            for bar in bars:
                height = bar.get_height()
                ax1.text(bar.get_x() + bar.get_width()/2., height,
                        f'{int(height)}', ha='center', va='bottom', fontweight='bold', fontsize=12)
            
            # Segmentation metrics
            metrics = ['Memory\nUtilization', 'External\nFragmentation', 'Access\nEfficiency']
            values_metrics = [
                result['memory_utilization'],
                (result['external_fragmentation'] / result['memory_size'] * 100) if result['memory_size'] > 0 else 0,
                result['access_efficiency']
            ]
            
            colors_metrics = ['#2196F3', '#FF9800', '#9C27B0']
            bars2 = ax2.bar(metrics, values_metrics, color=colors_metrics, edgecolor='black', linewidth=1.5)
            ax2.set_ylabel('Percentage (%)', fontsize=12, fontweight='bold')
            ax2.set_title('Segmentation Metrics', fontsize=14, fontweight='bold')
            ax2.set_ylim(0, 100)
            ax2.grid(axis='y', alpha=0.3)
            
            for bar in bars2:
                height = bar.get_height()
                ax2.text(bar.get_x() + bar.get_width()/2., height,
                        f'{height:.1f}%', ha='center', va='bottom', fontweight='bold')
        
        plt.tight_layout()
        return fig
    
    def plot_paging_vs_segmentation(self, paging_result, segmentation_result):
        """
        Compare paging vs segmentation
        """
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
        
        # Memory Utilization Comparison
        categories = ['Paging', 'Segmentation']
        utilization = [paging_result['memory_utilization'], segmentation_result['memory_utilization']]
        colors = ['#2196F3', '#FF5722']
        
        bars1 = ax1.bar(categories, utilization, color=colors, edgecolor='black', linewidth=1.5)
        ax1.set_ylabel('Utilization (%)', fontsize=12, fontweight='bold')
        ax1.set_title('Memory Utilization Comparison', fontsize=14, fontweight='bold')
        ax1.set_ylim(0, 100)
        ax1.grid(axis='y', alpha=0.3)
        
        for bar in bars1:
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.1f}%', ha='center', va='bottom', fontweight='bold', fontsize=12)
        
        # Access Efficiency Comparison
        efficiency = [paging_result['access_efficiency'], segmentation_result['access_efficiency']]
        
        bars2 = ax2.bar(categories, efficiency, color=colors, edgecolor='black', linewidth=1.5)
        ax2.set_ylabel('Efficiency (%)', fontsize=12, fontweight='bold')
        ax2.set_title('Access Efficiency Comparison', fontsize=14, fontweight='bold')
        ax2.set_ylim(0, 100)
        ax2.grid(axis='y', alpha=0.3)
        
        for bar in bars2:
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.1f}%', ha='center', va='bottom', fontweight='bold', fontsize=12)
        
        # Determine better approach
        if utilization[0] > utilization[1]:
            best = "Paging"
        else:
            best = "Segmentation"
        
        fig.suptitle(f'Paging vs Segmentation (Better Utilization: {best})', 
                    fontsize=16, fontweight='bold', color='#4CAF50')
        
        plt.tight_layout()
        return fig
    
    def plot_page_replacement(self, result, algorithm):
        """
        Visualize page replacement algorithm execution
        """
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
        
        # Page Faults vs Hits
        page_faults = result['page_faults']
        page_hits = result['page_hits']
        
        categories = ['Page Hits', 'Page Faults']
        values = [page_hits, page_faults]
        colors_bar = ['#4CAF50', '#F44336']
        
        bars1 = ax1.bar(categories, values, color=colors_bar, edgecolor='black', linewidth=1.5)
        ax1.set_ylabel('Count', fontsize=12, fontweight='bold')
        ax1.set_title(f'{algorithm.upper()} - Page Hits vs Faults', fontsize=14, fontweight='bold')
        ax1.grid(axis='y', alpha=0.3)
        
        for bar in bars1:
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(height)}', ha='center', va='bottom', fontweight='bold', fontsize=12)
        
        # Hit Ratio Pie Chart
        sizes = [page_hits, page_faults]
        labels = [f'Hits ({result["hit_ratio"]}%)', f'Faults ({result["fault_ratio"]}%)']
        colors_pie = ['#4CAF50', '#F44336']
        explode = (0.05, 0.05)
        
        ax2.pie(sizes, explode=explode, labels=labels, colors=colors_pie, autopct='%1.1f%%',
                shadow=True, startangle=90, textprops={'fontsize': 11, 'fontweight': 'bold'})
        ax2.set_title(f'{algorithm.upper()} - Hit/Fault Ratio', fontsize=14, fontweight='bold')
        
        plt.tight_layout()
        return fig
    
    def plot_page_replacement_comparison(self, results):
        """
        Compare all page replacement algorithms
        """
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))
        
        algorithms = [algo for algo in results.keys() if algo != 'best_algorithm']
        best_algo = results.get('best_algorithm', '')
        
        # Extract metrics
        page_faults = [results[algo]['page_faults'] for algo in algorithms]
        hit_ratios = [results[algo]['hit_ratio'] for algo in algorithms]
        fault_ratios = [results[algo]['fault_ratio'] for algo in algorithms]
        exec_times = [results[algo]['execution_time'] for algo in algorithms]
        
        # Colors with highlight for best algorithm
        colors = ['#2196F3' if algo != best_algo else '#4CAF50' for algo in algorithms]
        
        # Page Faults Comparison
        bars1 = ax1.bar(algorithms, page_faults, color=colors, edgecolor='black', linewidth=1.5)
        ax1.set_ylabel('Page Faults', fontsize=12, fontweight='bold')
        ax1.set_title('Page Faults Comparison', fontsize=13, fontweight='bold')
        ax1.grid(axis='y', alpha=0.3)
        
        for bar in bars1:
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(height)}', ha='center', va='bottom', fontweight='bold')
        
        # Hit Ratio Comparison
        bars2 = ax2.bar(algorithms, hit_ratios, color=colors, edgecolor='black', linewidth=1.5)
        ax2.set_ylabel('Hit Ratio (%)', fontsize=12, fontweight='bold')
        ax2.set_title('Hit Ratio Comparison', fontsize=13, fontweight='bold')
        ax2.set_ylim(0, 100)
        ax2.grid(axis='y', alpha=0.3)
        
        for bar in bars2:
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.1f}%', ha='center', va='bottom', fontweight='bold')
        
        # Fault Ratio Comparison
        bars3 = ax3.bar(algorithms, fault_ratios, color=colors, edgecolor='black', linewidth=1.5)
        ax3.set_ylabel('Fault Ratio (%)', fontsize=12, fontweight='bold')
        ax3.set_title('Fault Ratio Comparison', fontsize=13, fontweight='bold')
        ax3.set_ylim(0, 100)
        ax3.grid(axis='y', alpha=0.3)
        
        for bar in bars3:
            height = bar.get_height()
            ax3.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.1f}%', ha='center', va='bottom', fontweight='bold')
        
        # Execution Time Comparison
        bars4 = ax4.bar(algorithms, exec_times, color=colors, edgecolor='black', linewidth=1.5)
        ax4.set_ylabel('Execution Time (ms)', fontsize=12, fontweight='bold')
        ax4.set_title('Execution Time Comparison', fontsize=13, fontweight='bold')
        ax4.grid(axis='y', alpha=0.3)
        
        for bar in bars4:
            height = bar.get_height()
            ax4.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.4f}', ha='center', va='bottom', fontweight='bold', fontsize=9)
        
        # Add best algorithm annotation
        fig.suptitle(f'Page Replacement Algorithm Comparison (Best: {best_algo.upper()})', 
                    fontsize=16, fontweight='bold', color='#4CAF50')
        
        plt.tight_layout()
        return fig
    
    def plot_virtual_memory(self, result):
        """
        Visualize virtual memory simulation
        """
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))
        
        # Page Hits vs Faults
        page_hits = result['page_hits']
        page_faults = result['page_faults']
        
        categories = ['Page Hits', 'Page Faults']
        values = [page_hits, page_faults]
        colors_bar = ['#4CAF50', '#F44336']
        
        bars1 = ax1.bar(categories, values, color=colors_bar, edgecolor='black', linewidth=1.5)
        ax1.set_ylabel('Count', fontsize=12, fontweight='bold')
        ax1.set_title('Page Hits vs Faults', fontsize=13, fontweight='bold')
        ax1.grid(axis='y', alpha=0.3)
        
        for bar in bars1:
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(height)}', ha='center', va='bottom', fontweight='bold', fontsize=12)
        
        # Hit Rate and Fault Rate
        metrics = ['Hit Rate', 'Fault Rate']
        values_rate = [result['hit_rate'], result['page_fault_rate']]
        colors_rate = ['#4CAF50', '#F44336']
        
        bars2 = ax2.bar(metrics, values_rate, color=colors_rate, edgecolor='black', linewidth=1.5)
        ax2.set_ylabel('Percentage (%)', fontsize=12, fontweight='bold')
        ax2.set_title('Hit/Fault Rate', fontsize=13, fontweight='bold')
        ax2.set_ylim(0, 100)
        ax2.grid(axis='y', alpha=0.3)
        
        for bar in bars2:
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.1f}%', ha='center', va='bottom', fontweight='bold')
        
        # Page Table Status
        valid_pages = sum(1 for page in result['page_table'] if page['valid'])
        invalid_pages = len(result['page_table']) - valid_pages
        
        sizes = [valid_pages, invalid_pages]
        labels = ['Pages in Memory', 'Pages on Disk']
        colors_pie = ['#2196F3', '#FF9800']
        explode = (0.05, 0)
        
        ax3.pie(sizes, explode=explode, labels=labels, colors=colors_pie, autopct='%1.1f%%',
                shadow=True, startangle=90, textprops={'fontsize': 11, 'fontweight': 'bold'})
        ax3.set_title('Page Distribution', fontsize=13, fontweight='bold')
        
        # Summary Metrics
        metrics_summary = ['Disk\nWrites', 'Total\nAccesses', 'EAT\n(ns/100)']
        values_summary = [
            result['disk_writes'],
            result['total_accesses'],
            result['effective_access_time'] / 100
        ]
        colors_summary = ['#E91E63', '#9C27B0', '#00BCD4']
        
        bars4 = ax4.bar(metrics_summary, values_summary, color=colors_summary, edgecolor='black', linewidth=1.5)
        ax4.set_ylabel('Count / Time', fontsize=12, fontweight='bold')
        ax4.set_title('Additional Metrics', fontsize=13, fontweight='bold')
        ax4.grid(axis='y', alpha=0.3)
        
        for bar in bars4:
            height = bar.get_height()
            ax4.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.1f}', ha='center', va='bottom', fontweight='bold')
        
        fig.suptitle('Virtual Memory Simulation Results', fontsize=16, fontweight='bold')
        
        plt.tight_layout()
        return fig