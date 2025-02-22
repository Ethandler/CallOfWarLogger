"""Module for monitoring system performance."""
import psutil
import threading
import time
from typing import Dict
from datetime import datetime

class PerformanceMonitor:
    def __init__(self):
        self.cpu_usage = 0.0
        self.memory_usage = 0.0
        self.is_running = False
        self.monitor_thread = None
        self.start_time = None
        
    def start(self):
        """Start performance monitoring."""
        self.is_running = True
        self.start_time = datetime.now()
        self.monitor_thread = threading.Thread(target=self._monitor_loop)
        self.monitor_thread.start()
        
    def stop(self):
        """Stop performance monitoring."""
        self.is_running = False
        if self.monitor_thread:
            self.monitor_thread.join()
            
    def _monitor_loop(self):
        """Continuous monitoring loop."""
        while self.is_running:
            self.cpu_usage = psutil.cpu_percent(interval=1)
            self.memory_usage = psutil.Process().memory_info().rss / 1024 / 1024  # Convert to MB
            time.sleep(1)
            
    def get_metrics(self) -> Dict:
        """Get current performance metrics."""
        return {
            'timestamp': datetime.now().isoformat(),
            'cpu_usage': self.cpu_usage,
            'memory_usage': self.memory_usage,
            'runtime': (datetime.now() - self.start_time).total_seconds() if self.start_time else 0
        }
