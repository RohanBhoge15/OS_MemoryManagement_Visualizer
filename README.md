# OS Memory Management Simulator

A comprehensive, interactive web-based simulator for Operating System Memory Management concepts, built with Flask (Python) backend and HTML/CSS/JavaScript frontend.

## 🎯 Features

### 1. Continuous Memory Allocation
- **Algorithms**: First Fit, Best Fit, Worst Fit
- **Partition Types**: Fixed and Variable Partitioning
- **Metrics**: 
  - Memory utilization
  - Internal fragmentation
  - External fragmentation
  - Allocation success rate
- **Visualizations**: Memory maps, comparison charts
- **Compare Mode**: Side-by-side algorithm comparison with automatic best algorithm highlighting

### 2. Paging and Segmentation
- **Paging Simulation**: 
  - Configurable page/frame sizes
  - Page table visualization
  - Logical to physical address mapping
- **Segmentation Simulation**:
  - Custom segment definitions
  - Segment table visualization
  - Dynamic memory allocation
- **Comparison Mode**: Compare paging vs segmentation approaches
- **Metrics**: Memory utilization, fragmentation, access efficiency

### 3. Page Replacement Algorithms
- **Algorithms**: FIFO, LRU, LFU, Optimal (Belady's)
- **Features**:
  - Custom reference string input
  - Step-by-step execution trace
  - Hit/fault ratio analysis
  - Execution time measurement
- **Compare Mode**: Compare all algorithms with insights and recommendations
- **Visualizations**: Hit/fault charts, performance comparisons

### 4. Virtual Memory
- **Features**:
  - Logical to physical address translation
  - Page table management
  - Access pattern simulation (read/write)
  - Effective Access Time (EAT) calculation
- **Tools**:
  - Address translation calculator
  - Binary breakdown visualization
  - Random access pattern generator
- **Metrics**: Page faults, hit rate, disk writes, EAT

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Setup Steps

1. **Clone or download the project**
```bash
cd os-memory-simulator