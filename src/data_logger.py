"""Module for logging game data to file."""
import json
from datetime import datetime
from typing import Dict, List
import threading
import time
import os

class DataLogger:
    def __init__(self, filename: str = "game_logs.json"):
        self.filename = filename
        self.buffer: List[Dict] = []
        self.buffer_lock = threading.Lock()
        self.is_running = False
        self.flush_thread = None
        
    def start(self):
        """Start the logging system."""
        self.is_running = True
        self.flush_thread = threading.Thread(target=self._periodic_flush)
        self.flush_thread.start()
        
    def stop(self):
        """Stop the logging system and flush remaining data."""
        self.is_running = False
        if self.flush_thread:
            self.flush_thread.join()
        self._flush_buffer()
        
    def log_event(self, event_data: Dict):
        """Log a new event to the buffer."""
        event_data['timestamp'] = datetime.now().isoformat()
        
        with self.buffer_lock:
            self.buffer.append(event_data)
            
    def _periodic_flush(self):
        """Periodically flush the buffer to file."""
        while self.is_running:
            time.sleep(5)  # Flush every 5 seconds
            self._flush_buffer()
            
    def _flush_buffer(self):
        """Flush the current buffer to file."""
        with self.buffer_lock:
            if not self.buffer:
                return
                
            try:
                # Load existing data if file exists
                existing_data = []
                if os.path.exists(self.filename):
                    with open(self.filename, 'r') as f:
                        existing_data = json.load(f)
                        
                # Append new data
                existing_data.extend(self.buffer)
                
                # Write back to file
                with open(self.filename, 'w') as f:
                    json.dump(existing_data, f, indent=2)
                    
                self.buffer.clear()
                
            except Exception as e:
                print(f"Error flushing buffer: {str(e)}")
                
    def get_session_data(self) -> List[Dict]:
        """Get all data for the current session."""
        try:
            with open(self.filename, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return []
