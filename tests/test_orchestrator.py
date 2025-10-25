"""
Unit tests for ProblemSolverOrchestrator.
"""
import unittest
import tempfile
import os
import yaml
from unittest.mock import patch, MagicMock
from orchestrator import ProblemSolverOrchestrator


class TestProblemSolverOrchestrator(unittest.TestCase):
    """Test cases for ProblemSolverOrchestrator class."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        
        # Create a test config file
        self.config_data = {
            'api_keys': {
                'google': 'test-api-key'
            },
            'models': {
                'tester_agent': 'google:gemini-2.5-flash-lite',
                'brute_agent': 'google:gemini-2.5-flash-lite',
                'optimal_agent': 'google:gemini-2.5-flash-lite'
            },
            'execution': {
                'max_optimal_attempts': 3,
                'timeout_seconds': 10
            },
            'output': {
                'workspace_dir': os.path.join(self.temp_dir, 'workspace')
            },
            'files': {
                'test_inputs': 'small_inputs.txt',
                'brute_solution': 'brute.py',
                'brute_outputs': 'small_outputs.txt',
                'optimal_solution': 'optimal.py',
                'optimal_outputs': 'op.txt'
            }
        }
        
        self.config_file = os.path.join(self.temp_dir, 'test_config.yaml')
        with open(self.config_file, 'w') as f:
            yaml.dump(self.config_data, f)

    def tearDown(self):
        """Clean up test fixtures."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    @patch.dict(os.environ, {}, clear=True)
    def test_init_sets_environment_variable(self):
        """Test that initialization sets the Google API key environment variable."""
        with patch('orchestrator.TesterAgent'), \
             patch('orchestrator.BruteAgent'), \
             patch('orchestrator.OptimalAgent'):
            
            orchestrator = ProblemSolverOrchestrator(self.config_file)
            
            self.assertEqual(os.environ.get('GOOGLE_API_KEY'), 'test-api-key')

    @patch.dict(os.environ, {}, clear=True)
    def test_init_skips_placeholder_api_key(self):
        """Test that placeholder API keys are not set as environment variables."""
        # Modify config to use placeholder
        self.config_data['api_keys']['google'] = 'your-google-api-key-here'
        with open(self.config_file, 'w') as f:
            yaml.dump(self.config_data, f)
            
        with patch('orchestrator.TesterAgent'), \
             patch('orchestrator.BruteAgent'), \
             patch('orchestrator.OptimalAgent'):
            
            orchestrator = ProblemSolverOrchestrator(self.config_file)
            
            self.assertIsNone(os.environ.get('GOOGLE_API_KEY'))

    def test_init_creates_workspace_directory(self):
        """Test that initialization creates the workspace directory."""
        with patch('orchestrator.TesterAgent'), \
             patch('orchestrator.BruteAgent'), \
             patch('orchestrator.OptimalAgent'):
            
            orchestrator = ProblemSolverOrchestrator(self.config_file)
            
            self.assertTrue(os.path.exists(orchestrator.workspace))

    def test_init_sets_file_paths(self):
        """Test that initialization sets correct file paths."""
        with patch('orchestrator.TesterAgent'), \
             patch('orchestrator.BruteAgent'), \
             patch('orchestrator.OptimalAgent'):
            
            orchestrator = ProblemSolverOrchestrator(self.config_file)
            
            expected_workspace = os.path.join(self.temp_dir, 'workspace')
            self.assertEqual(orchestrator.workspace, expected_workspace)
            
            # Check file paths
            expected_files = {
                'test_inputs': os.path.join(expected_workspace, 'small_inputs.txt'),
                'brute_solution': os.path.join(expected_workspace, 'brute.py'),
                'brute_outputs': os.path.join(expected_workspace, 'small_outputs.txt'),
                'optimal_solution': os.path.join(expected_workspace, 'optimal.py'),
                'optimal_outputs': os.path.join(expected_workspace, 'op.txt')
            }
            
            self.assertEqual(orchestrator.files, expected_files)

    def test_init_sets_max_attempts(self):
        """Test that initialization sets max attempts from config."""
        with patch('orchestrator.TesterAgent'), \
             patch('orchestrator.BruteAgent'), \
             patch('orchestrator.OptimalAgent'):
            
            orchestrator = ProblemSolverOrchestrator(self.config_file)
            
            self.assertEqual(orchestrator.max_attempts, 3)

    def test_config_file_not_found(self):
        """Test behavior when config file is not found."""
        with self.assertRaises(FileNotFoundError):
            ProblemSolverOrchestrator('nonexistent_config.yaml')

    def test_invalid_config_structure(self):
        """Test behavior with invalid config structure."""
        # Create config with missing required keys
        invalid_config = {'invalid': 'config'}
        invalid_config_file = os.path.join(self.temp_dir, 'invalid_config.yaml')
        with open(invalid_config_file, 'w') as f:
            yaml.dump(invalid_config, f)
        
        with self.assertRaises(KeyError):
            ProblemSolverOrchestrator(invalid_config_file)


if __name__ == '__main__':
    unittest.main()
