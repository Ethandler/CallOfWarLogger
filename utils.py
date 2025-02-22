import time
import psutil
import logging
import functools

def performance_monitor(func):
    """Decorator to monitor function performance."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        start_memory = psutil.Process().memory_info().rss / 1024 / 1024  # MB
        
        result = func(*args, **kwargs)
        
        end_time = time.time()
        end_memory = psutil.Process().memory_info().rss / 1024 / 1024  # MB
        
        execution_time = (end_time - start_time) * 1000  # Convert to ms
        memory_delta = end_memory - start_memory
        
        if execution_time > 16.67:  # More than 60fps threshold
            logging.warning(
                f"Performance warning in {func.__name__}: "
                f"Execution time: {execution_time:.2f}ms, "
                f"Memory delta: {memory_delta:.2f}MB"
            )
            
        return result
    return wrapper

def format_timestamp(timestamp):
    """Format timestamp for logging."""
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp))

def calculate_fps(frame_times):
    """Calculate FPS from frame times."""
    if not frame_times:
        return 0
    avg_frame_time = sum(frame_times) / len(frame_times)
    return 1.0 / avg_frame_time if avg_frame_time > 0 else 0

def compress_data(data):
    """Compress data for storage optimization."""
    # Implement compression if needed
    return data

def sanitize_input(input_data):
    """Sanitize input data for storage."""
    if isinstance(input_data, dict):
        return {str(k): sanitize_input(v) for k, v in input_data.items()}
    elif isinstance(input_data, (list, tuple, set)):
        return [sanitize_input(x) for x in input_data]
    elif isinstance(input_data, (int, float, str, bool)):
        return input_data
    else:
        return str(input_data)
