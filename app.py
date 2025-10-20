from flask import Flask, render_template, request, jsonify
import base64
from io import BytesIO
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
from modules.continuous_allocation import ContinuousMemoryAllocator
from modules.paging_segmentation import PagingSegmentation
from modules.page_replacement import PageReplacementSimulator
from modules.virtual_memory import VirtualMemorySimulator
from modules.visualizer import Visualizer

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

# Initialize modules
continuous_allocator = ContinuousMemoryAllocator()
paging_segmentation = PagingSegmentation()
page_replacement = PageReplacementSimulator()
virtual_memory = VirtualMemorySimulator()
visualizer = Visualizer()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/continuous')
def continuous():
    return render_template('continuous.html')

@app.route('/paging')
def paging():
    return render_template('paging.html')

@app.route('/page-replacement')
def page_replacement_view():
    return render_template('page_replacement.html')

@app.route('/virtual-memory')
def virtual_memory_view():
    return render_template('virtual_memory.html')

# API Routes for Continuous Memory Allocation
@app.route('/api/continuous/simulate', methods=['POST'])
def simulate_continuous():
    data = request.json
    memory_size = data.get('memorySize', 1000)
    processes = data.get('processes', [])
    partition_type = data.get('partitionType', 'variable')
    algorithm = data.get('algorithm', 'first_fit')
    
    result = continuous_allocator.simulate(memory_size, processes, partition_type, algorithm)
    
    # Generate visualization
    fig = visualizer.plot_memory_allocation(result['memory_map'], memory_size)
    img = BytesIO()
    fig.savefig(img, format='png', bbox_inches='tight')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    plt.close(fig)
    
    result['plot'] = f"data:image/png;base64,{plot_url}"
    
    return jsonify(result)

@app.route('/api/continuous/compare', methods=['POST'])
def compare_continuous():
    data = request.json
    memory_size = data.get('memorySize', 1000)
    processes = data.get('processes', [])
    partition_type = data.get('partitionType', 'variable')
    
    results = continuous_allocator.compare_all(memory_size, processes, partition_type)
    
    # Generate comparison visualization
    fig = visualizer.plot_comparison_continuous(results)
    img = BytesIO()
    fig.savefig(img, format='png', bbox_inches='tight')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    plt.close(fig)
    
    return jsonify({
        'results': results,
        'plot': f"data:image/png;base64,{plot_url}"
    })

# API Routes for Paging and Segmentation
@app.route('/api/paging/simulate', methods=['POST'])
def simulate_paging():
    data = request.json
    mode = data.get('mode', 'paging')
    memory_size = data.get('memorySize', 4096)
    process_size = data.get('processSize', 1024)
    page_size = data.get('pageSize', 256)
    segments = data.get('segments', [])
    
    if mode == 'paging':
        result = paging_segmentation.simulate_paging(memory_size, process_size, page_size)
    else:
        result = paging_segmentation.simulate_segmentation(memory_size, segments)
    
    # Generate visualization
    fig = visualizer.plot_paging_segmentation(result, mode)
    img = BytesIO()
    fig.savefig(img, format='png', bbox_inches='tight')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    plt.close(fig)
    
    result['plot'] = f"data:image/png;base64,{plot_url}"
    
    return jsonify(result)

@app.route('/api/paging/compare', methods=['POST'])
def compare_paging():
    data = request.json
    memory_size = data.get('memorySize', 4096)
    process_size = data.get('processSize', 1024)
    page_size = data.get('pageSize', 256)
    segments = data.get('segments', [])
    
    paging_result = paging_segmentation.simulate_paging(memory_size, process_size, page_size)
    segmentation_result = paging_segmentation.simulate_segmentation(memory_size, segments)
    
    # Generate comparison visualization
    fig = visualizer.plot_paging_vs_segmentation(paging_result, segmentation_result)
    img = BytesIO()
    fig.savefig(img, format='png', bbox_inches='tight')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    plt.close(fig)
    
    return jsonify({
        'paging': paging_result,
        'segmentation': segmentation_result,
        'plot': f"data:image/png;base64,{plot_url}"
    })

# API Routes for Page Replacement
@app.route('/api/page-replacement/simulate', methods=['POST'])
def simulate_page_replacement():
    data = request.json
    algorithm = data.get('algorithm', 'fifo')
    reference_string = data.get('referenceString', [])
    frame_count = data.get('frameCount', 3)
    
    result = page_replacement.simulate(algorithm, reference_string, frame_count)
    
    # Generate visualization
    fig = visualizer.plot_page_replacement(result, algorithm)
    img = BytesIO()
    fig.savefig(img, format='png', bbox_inches='tight')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    plt.close(fig)
    
    result['plot'] = f"data:image/png;base64,{plot_url}"
    
    return jsonify(result)

@app.route('/api/page-replacement/compare', methods=['POST'])
def compare_page_replacement():
    data = request.json
    reference_string = data.get('referenceString', [])
    frame_count = data.get('frameCount', 3)
    
    results = page_replacement.compare_all(reference_string, frame_count)
    
    # Generate comparison visualization
    fig = visualizer.plot_page_replacement_comparison(results)
    img = BytesIO()
    fig.savefig(img, format='png', bbox_inches='tight')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    plt.close(fig)
    
    return jsonify({
        'results': results,
        'plot': f"data:image/png;base64,{plot_url}"
    })

# API Routes for Virtual Memory
@app.route('/api/virtual-memory/simulate', methods=['POST'])
def simulate_virtual_memory():
    data = request.json
    virtual_size = data.get('virtualSize', 65536)
    physical_size = data.get('physicalSize', 16384)
    page_size = data.get('pageSize', 4096)
    access_pattern = data.get('accessPattern', [])
    
    result = virtual_memory.simulate(virtual_size, physical_size, page_size, access_pattern)
    
    # Generate visualization
    fig = visualizer.plot_virtual_memory(result)
    img = BytesIO()
    fig.savefig(img, format='png', bbox_inches='tight')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    plt.close(fig)
    
    result['plot'] = f"data:image/png;base64,{plot_url}"
    
    return jsonify(result)

@app.route('/api/virtual-memory/translate', methods=['POST'])
def translate_address():
    data = request.json
    logical_address = data.get('logicalAddress', 0)
    page_size = data.get('pageSize', 4096)
    page_table = data.get('pageTable', {})
    
    result = virtual_memory.translate_address(logical_address, page_size, page_table)
    
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, port=5000)