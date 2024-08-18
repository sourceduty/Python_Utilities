#Computer Performance Benchmark

import os
import time
import multiprocessing
import platform
import psutil
import cpuinfo
import numpy as np
import pyopencl as cl

os.environ['PYOPENCL_COMPILER_OUTPUT'] = '1'

def cpu_stress_test(duration):
    """
    Perform intensive mathematical calculations for a given duration.
    """
    end_time = time.time() + duration
    while time.time() < end_time:
        # Perform some intensive calculations
        [x ** 0.5 for x in range(1, 10000)]

def benchmark_cpu(cores, duration_per_core):
    """
    Benchmark CPU by running stress test on all cores.
    """
    print(f"Starting CPU stress test on {cores} cores for {duration_per_core} seconds each.")
    
    processes = []
    for _ in range(cores):
        p = multiprocessing.Process(target=cpu_stress_test, args=(duration_per_core,))
        p.start()
        processes.append(p)
    
    for p in processes:
        p.join()

def measure_memory_bandwidth():
    """
    Measure memory bandwidth using a simple benchmark.
    """
    array_size = 1000000
    a = np.random.rand(array_size)
    b = np.random.rand(array_size)
    
    start_time = time.time()
    for _ in range(10):
        np.dot(a, b)
    end_time = time.time()
    
    duration = end_time - start_time
    memory_bandwidth = array_size * 8 * 10 / duration / (1024 ** 3)  # GB/s
    return memory_bandwidth

def measure_ram_speed():
    """
    Measure RAM speed by reading and writing large arrays.
    """
    array_size = 100000000
    a = np.random.rand(array_size)
    
    # Write speed
    start_time = time.time()
    b = np.copy(a)
    end_time = time.time()
    write_speed = array_size * 8 / (end_time - start_time) / (1024 ** 3)  # GB/s
    
    # Read speed
    start_time = time.time()
    np.sum(b)
    end_time = time.time()
    read_speed = array_size * 8 / (end_time - start_time) / (1024 ** 3)  # GB/s
    
    return write_speed, read_speed

def measure_gpu_performance():
    """
    Measure GPU performance using a simple PyOpenCL benchmark.
    """
    try:
        # Initialize OpenCL
        platform = cl.get_platforms()[0]
        device = platform.get_devices()[0]
        context = cl.Context([device])
        queue = cl.CommandQueue(context)
        
        # Allocate memory on GPU
        n = 10000000
        a = np.random.randn(n).astype(np.float32)
        b = np.random.randn(n).astype(np.float32)
        
        a_buf = cl.Buffer(context, cl.mem_flags.READ_ONLY | cl.mem_flags.COPY_HOST_PTR, hostbuf=a)
        b_buf = cl.Buffer(context, cl.mem_flags.READ_ONLY | cl.mem_flags.COPY_HOST_PTR, hostbuf=b)
        c_buf = cl.Buffer(context, cl.mem_flags.WRITE_ONLY, a.nbytes)
        
        # OpenCL kernel
        program = cl.Program(context, """
        __kernel void add(__global const float *a, __global const float *b, __global float *c) {
            int idx = get_global_id(0);
            c[idx] = a[idx] + b[idx];
        }
        """).build()
        
        start_time = time.time()
        for _ in range(10):
            program.add(queue, (n,), None, a_buf, b_buf, c_buf)
            queue.finish()
        end_time = time.time()
        
        gpu_performance = n * 4 * 10 / (end_time - start_time) / (1024 ** 3)  # GB/s
        return gpu_performance
    except Exception as e:
        print(f"Error during GPU performance measurement: {e}")
        return None

def generate_report(duration_per_core):
    """
    Generate and save the benchmark report to a dynamically created folder.
    """
    cores = multiprocessing.cpu_count()
    threads = psutil.cpu_count(logical=True)
    cpu_info = cpuinfo.get_cpu_info()
    cpu_freq = psutil.cpu_freq().max
    memory_bandwidth = measure_memory_bandwidth()
    ram_write_speed, ram_read_speed = measure_ram_speed()
    gpu_performance = measure_gpu_performance()
    
    start_time = time.time()
    benchmark_cpu(cores, duration_per_core)
    end_time = time.time()
    total_time = end_time - start_time
    
    # Rating
    rating = "Good" if cpu_freq > 2500 and cores >= 4 else "Average" if cpu_freq > 1500 and cores >= 2 else "Poor"
    performance = "Faster" if total_time < duration_per_core * 1.5 else "Slower"
    
    folder_path = os.path.join(os.getcwd(), "cpu_benchmark_reports")
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    
    report = (
        f"CPU Benchmark Report\n"
        f"=====================\n"
        f"System: {platform.system()}\n"
        f"Processor: {cpu_info['brand_raw']}\n"
        f"Number of Cores: {cores}\n"
        f"Number of Threads: {threads}\n"
        f"CPU Max Frequency: {cpu_freq:.2f} MHz\n"
        f"Memory Bandwidth: {memory_bandwidth:.2f} GB/s\n"
        f"RAM Write Speed: {ram_write_speed:.2f} GB/s\n"
        f"RAM Read Speed: {ram_read_speed:.2f} GB/s\n"
        f"GPU Performance: {gpu_performance:.2f} GB/s\n" if gpu_performance is not None else "GPU Performance: Error during measurement\n"
        f"Duration per Core: {duration_per_core} seconds\n"
        f"Total Time Taken: {total_time:.2f} seconds\n"
        f"Performance Rating: {rating}\n"
        f"Performance Speed: {performance}\n"
    )
    
    file_path = os.path.join(folder_path, 'cpu_benchmark_report.txt')
    
    with open(file_path, 'w') as file:
        file.write(report)
    
    print(f"Report generated and saved to {file_path}")

def determine_test_duration():
    """
    Determine an appropriate test duration based on CPU speed.
    """
    cpu_freq = psutil.cpu_freq()
    if cpu_freq:
        base_freq = cpu_freq.max
    else:
        base_freq = 2000  # Default to 2GHz if unable to determine
    
    # Determine duration (e.g., 30 seconds for every GHz)
    duration_per_core = max(30, int(base_freq / 1000 * 30))
    return duration_per_core

if __name__ == "__main__":
    duration_per_core = determine_test_duration()
    generate_report(duration_per_core)
