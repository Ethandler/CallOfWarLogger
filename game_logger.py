#!/usr/bin/env python3
import json
import time
from datetime import datetime
from input_tracker import InputTracker
from data_collector import DataCollector
from ml_trainer import GameplayLearner
from utils import performance_monitor
import logging
import os
import sys
import platform
import ctypes

# Set up detailed logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s',
    handlers=[
        logging.FileHandler('game_logger_debug.log'),
        logging.StreamHandler()
    ]
)

class GameLogger:
    def __init__(self):
        self.input_tracker = InputTracker()
        self.data_collector = DataCollector()
        self.gameplay_learner = GameplayLearner()
        self.is_running = False
        self.session_start = None
        self.current_log = []
        self.last_analysis_time = time.time()
        self.analysis_interval = 300  # Analyze every 5 minutes

        # Log system info for debugging
        self._log_system_info()

    def _log_system_info(self):
        """Log system information for debugging purposes."""
        logging.info(f"Operating System: {platform.system()} {platform.release()}")
        logging.info(f"Python Version: {sys.version}")

        if platform.system() == 'Windows':
            try:
                # Properly handle Windows admin check
                def is_admin():
                    try:
                        return ctypes.windll.shell32.IsUserAnAdmin()
                    except AttributeError:
                        return False

                admin_status = is_admin()
                logging.info(f"Running with Administrator privileges: {bool(admin_status)}")

                if not admin_status:
                    logging.warning("⚠️ Administrator privileges required for full functionality")
                    logging.info("Please run run_logger.bat as administrator")
            except Exception as e:
                logging.warning(f"Could not check administrator privileges: {str(e)}")
        else:
            logging.info("Running on non-Windows system")

    @performance_monitor
    def start_logging(self):
        """Start the logging session."""
        try:
            self.is_running = True
            self.session_start = datetime.now()
            logging.info("=== Starting Game Logging Session ===")
            logging.info(f"Session start time: {self.session_start}")

            # Create logs directory if it doesn't exist
            if not os.path.exists('game_logs'):
                os.makedirs('game_logs')
                logging.info("Created game_logs directory")

            # Start input tracking (will run in limited mode if no admin privileges)
            self.input_tracker.start()

            if not self.input_tracker.input_tracking_available:
                if platform.system() == 'Windows':
                    logging.warning("⚠️ Running with limited functionality - administrator privileges required")
                    logging.info("To enable full functionality, run 'run_logger.bat' as administrator")
                else:
                    logging.warning("⚠️ Running with limited functionality - input tracking disabled")
                    logging.info("To enable full functionality, run the script with root privileges")
            else:
                logging.info("✅ Input tracking successfully initialized")

            self._main_loop()
        except Exception as e:
            logging.error(f"Critical error in logging session: {str(e)}", exc_info=True)
            self.stop_logging()

    def stop_logging(self):
        """Stop the logging session and save data."""
        try:
            self.is_running = False
            self.input_tracker.stop()
            self._save_logs()
            logging.info("=== Logging session stopped ===")
            if self.session_start:
                duration = datetime.now() - self.session_start
                logging.info(f"Session duration: {duration}")
            else:
                logging.warning("Session duration unknown: start time was not recorded")
        except Exception as e:
            logging.error(f"Error while stopping logging: {str(e)}", exc_info=True)

    def _main_loop(self):
        """Main logging loop that collects and processes data."""
        loop_iterations = 0
        last_save_time = time.time()

        while self.is_running:
            try:
                loop_start = time.time()

                # Collect current game state
                game_state = self.data_collector.get_game_state()

                # Get input data (will be empty if input tracking is disabled)
                input_data = self.input_tracker.get_current_input_state()

                # Combine data
                log_entry = {
                    "timestamp": time.time(),
                    "game_state": game_state,
                    "input_data": input_data
                }

                self.current_log.append(log_entry)

                # Performance monitoring
                loop_duration = time.time() - loop_start
                if loop_duration > 0.020:  # More than 50fps
                    logging.warning(f"Loop took longer than expected: {loop_duration:.3f}s")

                # Save periodically (every 1000 entries or 60 seconds)
                if len(self.current_log) >= 1000 or (time.time() - last_save_time) > 60:
                    self._save_logs()
                    self.current_log = []
                    last_save_time = time.time()

                # Periodic gameplay analysis
                current_time = time.time()
                if current_time - self.last_analysis_time > self.analysis_interval:
                    self._analyze_gameplay()
                    self.last_analysis_time = current_time

                # Log statistics every 1000 iterations
                loop_iterations += 1
                if loop_iterations % 1000 == 0:
                    self._log_statistics(game_state)

                time.sleep(max(0, 0.016 - loop_duration))  # Target ~60 FPS

            except Exception as e:
                logging.error(f"Error in main loop: {str(e)}", exc_info=True)
                if not self.is_running:
                    break

    def _analyze_gameplay(self):
        """Analyze gameplay data and generate insights."""
        try:
            logging.info("=== Starting Gameplay Analysis ===")
            analysis_results = self.gameplay_learner.analyze_gameplay()
            if analysis_results:
                recommendations = self.gameplay_learner.generate_recommendations(analysis_results)

                logging.info("=== Gameplay Analysis Results ===")
                logging.info(f"Movement Style: {analysis_results['movement_style']}")
                logging.info(f"Combat Effectiveness: {json.dumps(analysis_results['combat_effectiveness'], indent=2)}")
                logging.info(f"Resource Efficiency: {analysis_results['resource_efficiency']:.2f}")
                logging.info(f"Tactical Profile: {json.dumps(analysis_results['tactical_profile'], indent=2)}")

                logging.info("=== Gameplay Recommendations ===")
                for idx, rec in enumerate(recommendations, 1):
                    logging.info(f"{idx}. {rec}")

                # Save analysis results
                analysis_file = f"game_logs/analysis_{self.session_start.strftime('%Y%m%d_%H%M%S')}.json"
                with open(analysis_file, 'w') as f:
                    json.dump({
                        'timestamp': time.time(),
                        'analysis': analysis_results,
                        'recommendations': recommendations
                    }, f, indent=2)

                logging.info(f"Analysis results saved to {analysis_file}")
            else:
                logging.warning("No analysis results available - insufficient data")

        except Exception as e:
            logging.error(f"Error during gameplay analysis: {str(e)}", exc_info=True)

    def _log_statistics(self, game_state):
        """Log periodic statistics about the game state."""
        try:
            zombies = game_state["game"]["zombies"]
            logging.info(f"=== Statistics Update ===")
            logging.info(f"Round: {game_state['game']['round']}")
            logging.info(f"Zombies - Total: {zombies['total']}, Alive: {zombies['alive']}, Killed: {zombies['killed']}")
            logging.info(f"Player Health: {game_state['player']['health']}")
            logging.info(f"Current Weapon: {game_state['player']['weapon']['name']}")
            if game_state['game']['power_ups']['active']:
                logging.info(f"Active Power-up: {game_state['game']['power_ups']['active']}")
        except Exception as e:
            logging.error(f"Error logging statistics: {str(e)}")

    def _save_logs(self):
        """Save collected logs to file."""
        if not self.current_log:
            return

        if self.session_start is None:
            self.session_start = datetime.now()

        filename = f"game_logs/game_logs_{self.session_start.strftime('%Y%m%d_%H%M%S')}.json"
        try:
            with open(filename, 'a') as f:
                json.dump(self.current_log, f)
            logging.info(f"✅ Logs saved to {filename} ({len(self.current_log)} entries)")
        except Exception as e:
            logging.error(f"Error saving logs to {filename}: {str(e)}", exc_info=True)

if __name__ == "__main__":
    logger = GameLogger()
    try:
        logger.start_logging()
    except KeyboardInterrupt:
        logging.info("Received keyboard interrupt, stopping logger...")
        logger.stop_logging()
    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}", exc_info=True)
        logger.stop_logging()