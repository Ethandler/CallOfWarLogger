"""Main entry point for the Call of Duty: World at War data logging system."""
import time
from datetime import datetime
import signal
import sys
from typing import Dict

from input_tracker import InputTracker
from game_state import GameState
from data_logger import DataLogger
from performance_monitor import PerformanceMonitor
import config

class GameLogger:
    def __init__(self):
        self.input_tracker = InputTracker()
        self.game_state = GameState()
        self.data_logger = DataLogger(config.LOG_FILE_PATH)
        self.performance_monitor = PerformanceMonitor()
        self.is_running = False
        
    def start(self):
        """Start all logging components."""
        print("Starting game logging system...")
        
        # Register signal handlers
        signal.signal(signal.SIGINT, self._handle_shutdown)
        signal.signal(signal.SIGTERM, self._handle_shutdown)
        
        # Start all components
        self.input_tracker.start()
        self.data_logger.start()
        self.performance_monitor.start()
        self.is_running = True
        
        print("Logging system started. Press Ctrl+C to stop.")
        
        # Main logging loop
        self._logging_loop()
        
    def stop(self):
        """Stop all logging components."""
        print("\nStopping logging system...")
        self.is_running = False
        
        # Stop all components
        self.input_tracker.stop()
        self.data_logger.stop()
        self.performance_monitor.stop()
        
        print("Logging system stopped.")
        
    def _logging_loop(self):
        """Main logging loop."""
        last_log_time = time.time()
        
        while self.is_running:
            current_time = time.time()
            
            # Check if it's time to log data
            if current_time - last_log_time >= config.LOGGING_INTERVAL:
                try:
                    # Get current states
                    input_state = self.input_tracker.get_current_state()
                    aim_metrics = self.input_tracker.calculate_aim_metrics()
                    
                    # Update game state
                    self.game_state.update(input_state)
                    game_state = self.game_state.get_state()
                    
                    # Get performance metrics
                    performance_metrics = self.performance_monitor.get_metrics()
                    
                    # Combine all data
                    log_entry = {
                        'timestamp': datetime.now().isoformat(),
                        'input_state': input_state,
                        'aim_metrics': aim_metrics,
                        'game_state': game_state,
                        'performance': performance_metrics
                    }
                    
                    # Log the data
                    self.data_logger.log_event(log_entry)
                    
                    last_log_time = current_time
                    
                except Exception as e:
                    print(f"Error in logging loop: {str(e)}")
                    
            # Small sleep to prevent CPU overuse
            time.sleep(0.001)
            
    def _handle_shutdown(self, signum, frame):
        """Handle shutdown signals."""
        self.stop()
        sys.exit(0)

def main():
    """Main entry point."""
    try:
        logger = GameLogger()
        logger.start()
    except Exception as e:
        print(f"Error starting logger: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
