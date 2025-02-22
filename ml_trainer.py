import json
import numpy as np
import logging
from pathlib import Path
from datetime import datetime
import pandas as pd
from collections import defaultdict

class GameplayLearner:
    def __init__(self):
        self.behavior_patterns = defaultdict(int)
        self.action_sequences = []
        self.performance_metrics = {}
        logging.info("GameplayLearner initialized")

    def load_gameplay_data(self, log_directory='game_logs'):
        """Load and preprocess gameplay log files."""
        try:
            log_path = Path(log_directory)
            if not log_path.exists():
                log_path.mkdir(parents=True, exist_ok=True)
                logging.warning(f"Created {log_directory} directory")
                return []

            all_data = []
            file_count = 0
            total_entries = 0

            for log_file in log_path.glob('game_logs_*.json'):
                try:
                    with open(log_file, 'r') as f:
                        log_data = json.load(f)
                        if isinstance(log_data, list):
                            total_entries += len(log_data)
                            all_data.extend(log_data)
                        else:
                            total_entries += 1
                            all_data.append(log_data)
                        file_count += 1
                except json.JSONDecodeError:
                    logging.error(f"Error decoding {log_file}")
                    continue

            logging.info(f"Loaded {total_entries} entries from {file_count} files")
            return all_data
        except Exception as e:
            logging.error(f"Error loading gameplay data: {str(e)}")
            return []

    def extract_features(self, gameplay_data):
        """Extract relevant features from gameplay data."""
        logging.info("Starting feature extraction")
        features = {
            'movement_patterns': [],
            'combat_metrics': [],
            'resource_usage': [],
            'tactical_decisions': []
        }

        for entry_idx, entry in enumerate(gameplay_data):
            try:
                # Movement patterns from input data
                if 'input_data' in entry:
                    key_states = entry['input_data'].get('keyboard', [])
                    movement = self._analyze_movement(key_states)
                    features['movement_patterns'].append(movement)
                    logging.debug(f"Entry {entry_idx}: Movement pattern - {movement}")

                # Combat metrics
                if 'game_state' in entry and 'player' in entry['game_state']:
                    player = entry['game_state']['player']
                    weapon = player.get('weapon', {})
                    combat_metrics = {
                        'accuracy': weapon.get('accuracy', 0),
                        'shots_fired': weapon.get('shots_fired', 0),
                        'hits': weapon.get('hits', 0),
                        'recoil_control': weapon.get('recoil_control', 0)
                    }
                    features['combat_metrics'].append(combat_metrics)
                    logging.debug(f"Entry {entry_idx}: Combat metrics - Accuracy: {combat_metrics['accuracy']:.2f}")

                # Resource management
                if 'game_state' in entry and 'player' in entry['game_state']:
                    player = entry['game_state']['player']
                    resource_data = {
                        'ammo': player.get('weapon', {}).get('ammo', {}).get('current', 0),
                        'health': player.get('health', 0),
                        'points': player.get('points', 0)
                    }
                    features['resource_usage'].append(resource_data)

                # Tactical decisions
                if 'game_state' in entry:
                    tactical_data = self._analyze_tactics(entry['game_state'])
                    features['tactical_decisions'].append(tactical_data)
                    logging.debug(f"Entry {entry_idx}: Tactical profile - Aggression: {tactical_data['aggression_level']:.2f}")

            except Exception as e:
                logging.warning(f"Error extracting features from entry {entry_idx}: {str(e)}")
                continue

        logging.info(f"Feature extraction completed: {len(gameplay_data)} entries processed")
        return features

    def _analyze_movement(self, key_states):
        """Analyze movement patterns from key states."""
        movement_type = 'stationary'

        if not key_states:
            return movement_type

        # Convert key states to set for easier checking
        keys = set(key_states)

        # Movement pattern analysis
        if 'w' in keys and 'shift' in keys:
            movement_type = 'rushing'
        elif 'w' in keys and 'ctrl' in keys:
            movement_type = 'sneaking'
        elif len(keys.intersection({'w', 'a', 's', 'd'})) > 1:
            movement_type = 'strafing'
        elif len(keys.intersection({'w', 'a', 's', 'd'})) == 1:
            movement_type = 'direct_movement'

        return movement_type

    def _analyze_tactics(self, game_state):
        """Analyze tactical decisions from game state."""
        tactical_profile = {
            'aggression_level': 0,  # 0-1 scale
            'positioning': 'unknown',
            'objective_focus': 0  # 0-1 scale
        }

        try:
            # Analyze aggression level based on actions and state
            player = game_state.get('player', {})
            actions = game_state.get('actions', {})

            # Calculate aggression based on multiple factors
            aggression_factors = []

            # Weapon usage
            weapon = player.get('weapon', {})
            if weapon.get('shots_fired', 0) > 0:
                aggression_factors.append(0.7)
                logging.debug("Aggressive behavior detected: Active weapon usage")

            # Movement style
            if actions.get('tactical', {}).get('sprinting', False):
                aggression_factors.append(0.8)
                logging.debug("Aggressive behavior detected: Sprinting")
            elif actions.get('tactical', {}).get('crouching', False):
                aggression_factors.append(0.3)
                logging.debug("Defensive behavior detected: Crouching")

            # Position relative to cover
            if game_state.get('environment', {}).get('in_cover', False):
                aggression_factors.append(0.2)
                tactical_profile['positioning'] = 'defensive'
                logging.debug("Defensive positioning: In cover")
            else:
                tactical_profile['positioning'] = 'aggressive'
                logging.debug("Aggressive positioning: Out of cover")

            # Calculate average aggression
            if aggression_factors:
                tactical_profile['aggression_level'] = sum(aggression_factors) / len(aggression_factors)

            # Analyze objective focus
            if game_state.get('game', {}).get('objectives_completed', 0) > 0:
                tactical_profile['objective_focus'] = 0.7
                logging.debug("High objective focus detected")

        except Exception as e:
            logging.warning(f"Error in tactical analysis: {str(e)}")

        return tactical_profile

    def analyze_gameplay(self):
        """Analyze gameplay data and generate insights."""
        try:
            logging.info("Starting gameplay analysis")
            gameplay_data = self.load_gameplay_data()
            if not gameplay_data:
                logging.warning("No gameplay data available for analysis")
                return None

            features = self.extract_features(gameplay_data)
            logging.info("Features extracted successfully")

            # Convert to pandas for analysis
            movement_df = pd.DataFrame({'movement': features['movement_patterns']})
            combat_df = pd.DataFrame(features['combat_metrics'])
            resource_df = pd.DataFrame(features['resource_usage'])
            tactical_df = pd.DataFrame([{
                'aggression': t['aggression_level'],
                'positioning': t['positioning'],
                'objective_focus': t['objective_focus']
            } for t in features['tactical_decisions']])

            # Calculate metrics
            movement_style = movement_df['movement'].mode().iloc[0] if not movement_df.empty else 'unknown'
            avg_accuracy = combat_df['accuracy'].mean() if not combat_df.empty else 0
            resource_efficiency = resource_df['points'].diff().mean() if not resource_df.empty else 0
            avg_aggression = tactical_df['aggression'].mean() if not tactical_df.empty else 0

            analysis_results = {
                'movement_style': movement_style,
                'combat_effectiveness': {
                    'accuracy': float(avg_accuracy),
                    'total_shots': int(combat_df['shots_fired'].sum()) if not combat_df.empty else 0,
                    'total_hits': int(combat_df['hits'].sum()) if not combat_df.empty else 0
                },
                'resource_efficiency': float(resource_efficiency),
                'tactical_profile': {
                    'aggression_level': float(avg_aggression),
                    'preferred_positioning': tactical_df['positioning'].mode().iloc[0] if not tactical_df.empty else 'unknown'
                }
            }

            logging.info("Gameplay analysis completed successfully")
            logging.info(f"Analysis results: {json.dumps(analysis_results, indent=2)}")
            return analysis_results

        except Exception as e:
            logging.error(f"Error in gameplay analysis: {str(e)}")
            return None

    def generate_recommendations(self, analysis_results):
        """Generate gameplay recommendations based on analysis."""
        if not analysis_results:
            return ["Insufficient data for recommendations"]

        logging.info("Generating gameplay recommendations")
        recommendations = []

        # Movement recommendations
        movement = analysis_results['movement_style']
        if movement == 'stationary':
            recommendations.append("Try to move more frequently to avoid being an easy target")
        elif movement == 'rushing':
            recommendations.append("Consider mixing in some tactical pauses to assess situations")

        # Combat recommendations
        combat = analysis_results['combat_effectiveness']
        if combat['accuracy'] < 0.3:
            recommendations.append("Focus on improving aim accuracy, try burst-firing for better control")
        if combat['total_shots'] > 0 and combat['total_hits'] / combat['total_shots'] < 0.25:
            recommendations.append("Practice trigger discipline - take more measured shots")

        # Tactical recommendations
        tactical = analysis_results['tactical_profile']
        if tactical['aggression_level'] > 0.8:
            recommendations.append("Consider a more balanced approach between aggression and defense")
        elif tactical['aggression_level'] < 0.2:
            recommendations.append("Look for more opportunities to push advantages when they arise")

        # Resource management
        if analysis_results['resource_efficiency'] < 0:
            recommendations.append("Focus on efficient resource management - prioritize point-earning actions")

        logging.info(f"Generated {len(recommendations)} recommendations")
        return recommendations