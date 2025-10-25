import os
import yaml
import json
import time
from typing import Dict, Optional, Tuple, List
from agents import TesterAgent, BruteAgent, OptimalAgent
from utils import CodeExecutor, OutputComparator, ProgressIndicator


class ProblemSolverOrchestrator:
    """Main orchestrator for the multi-agent problem solving system."""

    def __init__(self, config_path: str = "config.yaml"):
        """Initialize orchestrator with configuration."""
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)

        # Set up API key
        api_keys = self.config.get('api_keys', {})

        # Google API key for Gemini
        google_key = api_keys.get('google')
        if google_key and google_key != "your-google-api-key-here":
            os.environ['GOOGLE_API_KEY'] = google_key

        # Initialize agents
        self.tester_agent = TesterAgent(self.config['models']['tester_agent'])
        self.brute_agent = BruteAgent(self.config['models']['brute_agent'])
        self.optimal_agent = OptimalAgent(self.config['models']['optimal_agent'])

        # Initialize utilities
        timeout = self.config['execution']['timeout_seconds']
        self.executor = CodeExecutor(timeout=timeout)
        self.comparator = OutputComparator()

        # Set up workspace
        self.workspace = self.config['output']['workspace_dir']
        os.makedirs(self.workspace, exist_ok=True)

        # File paths
        self.files = {
            'test_inputs': os.path.join(self.workspace, self.config['files']['test_inputs']),
            'brute_solution': os.path.join(self.workspace, self.config['files']['brute_solution']),
            'brute_outputs': os.path.join(self.workspace, self.config['files']['brute_outputs']),
            'optimal_solution': os.path.join(self.workspace, self.config['files']['optimal_solution']),
            'optimal_outputs': os.path.join(self.workspace, self.config['files']['optimal_outputs'])
        }

        self.max_attempts = self.config['execution']['max_optimal_attempts']

    def solve(self, problem_statement: str) -> Tuple[bool, Optional[str], Dict]:
        """
        Solve the given problem using multi-agent approach.

        Args:
            problem_statement: The problem description

        Returns:
            Tuple of (success, optimal_code, metadata)
        """
        metadata = {
            'attempts': 0,
            'test_cases_generated': False,
            'brute_force_generated': False,
            'brute_force_executed': False,
            'optimal_solution_found': False,
            'errors': [],
            'optimal_attempts': []  # Store all attempts with details
        }

        print("=" * 80)
        print("STEP 1: Generating test cases...")
        print("=" * 80)

        try:
            with ProgressIndicator("Generating test cases with TesterAgent"):
                test_cases = self.tester_agent.generate_test_cases(problem_statement)
            with open(self.files['test_inputs'], 'w') as f:
                f.write(test_cases)
            metadata['test_cases_generated'] = True
            print(f"✓ Test cases saved to: {self.files['test_inputs']}\n")
        except Exception as e:
            error = f"Failed to generate test cases: {str(e)}"
            metadata['errors'].append(error)
            print(f"✗ {error}\n")
            return False, None, metadata

        print("=" * 80)
        print("STEP 2: Generating brute force solution...")
        print("=" * 80)

        try:
            with ProgressIndicator("Generating brute force solution with BruteAgent"):
                brute_code = self.brute_agent.generate_solution(problem_statement)
            with open(self.files['brute_solution'], 'w') as f:
                f.write(brute_code)
            metadata['brute_force_generated'] = True
            print(f"✓ Brute force solution saved to: {self.files['brute_solution']}\n")
        except Exception as e:
            error = f"Failed to generate brute force solution: {str(e)}"
            metadata['errors'].append(error)
            print(f"✗ {error}\n")
            return False, None, metadata

        print("=" * 80)
        print("STEP 3: Executing brute force solution...")
        print("=" * 80)

        success, error = self.executor.execute(
            self.files['brute_solution'],
            self.files['test_inputs'],
            self.files['brute_outputs']
        )

        if not success:
            error_msg = f"Brute force execution failed: {error}"
            metadata['errors'].append(error_msg)
            print(f"✗ {error_msg}\n")
            return False, None, metadata

        metadata['brute_force_executed'] = True
        print(f"✓ Brute force outputs saved to: {self.files['brute_outputs']}\n")

        print("=" * 80)
        print("STEP 4: Generating and testing optimal solution...")
        print("=" * 80)

        feedback = None
        optimal_code = None

        for attempt in range(1, self.max_attempts + 1):
            metadata['attempts'] = attempt
            print(f"\n--- Attempt {attempt}/{self.max_attempts} ---")

            attempt_data = {
                'attempt_number': attempt,
                'timestamp': time.time(),
                'code': None,
                'verdict': None,
                'error_message': None,
                'execution_success': False,
                'output_match': False,
                'output_diff': None
            }

            try:
                with ProgressIndicator(f"Generating optimal solution (attempt {attempt}/{self.max_attempts})"):
                    optimal_code = self.optimal_agent.generate_solution(
                        problem_statement,
                        feedback=feedback,
                        attempt=attempt
                    )

                attempt_data['code'] = optimal_code

                # Save this attempt separately
                attempt_file = os.path.join(self.workspace, f'optimal_attempt_{attempt}.py')
                with open(attempt_file, 'w') as f:
                    f.write(optimal_code)

                # Also update the main optimal solution file
                with open(self.files['optimal_solution'], 'w') as f:
                    f.write(optimal_code)

                print(f"✓ Generated optimal solution")

            except Exception as e:
                error = f"Failed to generate optimal solution: {str(e)}"
                attempt_data['verdict'] = 'Generation Failed'
                attempt_data['error_message'] = str(e)
                metadata['errors'].append(error)
                metadata['optimal_attempts'].append(attempt_data)
                print(f"✗ {error}")
                continue

            # Execute optimal solution
            attempt_output_file = os.path.join(self.workspace, f'optimal_attempt_{attempt}_output.txt')
            success, error = self.executor.execute(
                self.files['optimal_solution'],
                self.files['test_inputs'],
                attempt_output_file
            )

            # Also update main output file
            if success:
                with open(self.files['optimal_outputs'], 'w') as f_out:
                    with open(attempt_output_file, 'r') as f_in:
                        f_out.write(f_in.read())

            if not success:
                print(f"✗ Execution failed: {error}")
                attempt_data['verdict'] = 'Runtime Error'
                attempt_data['error_message'] = error
                attempt_data['execution_success'] = False
                metadata['optimal_attempts'].append(attempt_data)
                feedback = f"Your solution failed to execute:\n{error}\n\nPlease fix the errors."
                metadata['errors'].append(f"Attempt {attempt}: Execution failed - {error}")
                continue

            attempt_data['execution_success'] = True
            print(f"✓ Execution successful")

            # Compare outputs
            if self.comparator.compare(self.files['brute_outputs'], attempt_output_file):
                print(f"✓ Outputs match! Solution found in {attempt} attempt(s)")
                attempt_data['verdict'] = 'Accepted'
                attempt_data['output_match'] = True
                metadata['optimal_attempts'].append(attempt_data)
                metadata['optimal_solution_found'] = True
                print("\n" + "=" * 80)
                print("SUCCESS: Optimal solution found!")
                print("=" * 80)

                # Generate results JSON for viewer
                self._generate_results_json(problem_statement, metadata)

                return True, optimal_code, metadata
            else:
                diff = self.comparator.get_diff_summary(
                    self.files['brute_outputs'],
                    attempt_output_file
                )
                print(f"✗ Outputs don't match")
                print(f"Difference: {diff[:200]}...")
                attempt_data['verdict'] = 'Wrong Answer'
                attempt_data['output_match'] = False
                attempt_data['output_diff'] = diff
                metadata['optimal_attempts'].append(attempt_data)
                feedback = f"Your solution produced incorrect output:\n{diff}\n\nPlease fix the logic."
                metadata['errors'].append(f"Attempt {attempt}: Output mismatch")

        print("\n" + "=" * 80)
        print(f"FAILED: Could not find correct solution in {self.max_attempts} attempts")
        print("=" * 80)

        # Generate results JSON even on failure
        self._generate_results_json(problem_statement, metadata)

        return False, optimal_code, metadata

    def _generate_results_json(self, problem_statement: str, metadata: Dict):
        """Generate results.json for the web viewer."""
        # Read all necessary files
        test_input = ""
        brute_code = ""
        brute_output = ""

        try:
            with open(self.files['test_inputs'], 'r') as f:
                test_input = f.read()
        except:
            pass

        try:
            with open(self.files['brute_solution'], 'r') as f:
                brute_code = f.read()
        except:
            pass

        try:
            with open(self.files['brute_outputs'], 'r') as f:
                brute_output = f.read()
        except:
            pass

        results = {
            'problem_statement': problem_statement,
            'test_input': test_input,
            'test_output': brute_output,
            'brute_force_code': brute_code,
            'optimal_attempts': metadata['optimal_attempts'],
            'success': metadata['optimal_solution_found'],
            'total_attempts': metadata['attempts']
        }

        results_file = os.path.join(self.workspace, 'results.json')
        with open(results_file, 'w') as f:
            json.dump(results, f, indent=2)

        print(f"\n✓ Results saved to: {results_file}")
        print("\n" + "=" * 80)
        print("📊 VIEW RESULTS IN WEB BROWSER")
        print("=" * 80)
        print("\nTo view the beautiful HTML report, run:")
        print("\n  python -m http.server 8000")
        print("\nThen open: http://localhost:8000/viewer.html")
        print("\n(HTTP server needed to avoid CORS restrictions)")
        print("=" * 80)
