"""
Unit tests for CodeExecutor utility.
"""
import unittest
import tempfile
import os
from utils.executor import CodeExecutor


class TestCodeExecutor(unittest.TestCase):
    """Test cases for CodeExecutor class."""

    def setUp(self):
        """Set up test fixtures."""
        self.executor = CodeExecutor(timeout=5)
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        """Clean up test fixtures."""
        # Clean up temporary files
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_execute_simple_code(self):
        """Test execution of simple Python code."""
        # Create a simple Python script
        code_content = """
print("Hello, World!")
"""
        code_file = os.path.join(self.temp_dir, "test_code.py")
        with open(code_file, 'w') as f:
            f.write(code_content)

        # Create empty input file
        input_file = os.path.join(self.temp_dir, "input.txt")
        with open(input_file, 'w') as f:
            f.write("")

        # Output file
        output_file = os.path.join(self.temp_dir, "output.txt")

        # Execute
        success, error = self.executor.execute(code_file, input_file, output_file)

        # Verify
        self.assertTrue(success, f"Execution failed: {error}")
        self.assertEqual(error, "")
        
        # Check output
        with open(output_file, 'r') as f:
            output = f.read().strip()
        self.assertEqual(output, "Hello, World!")

    def test_execute_with_input(self):
        """Test execution with input data."""
        # Create a Python script that reads input
        code_content = """
import sys
line = sys.stdin.readline().strip()
print(f"Input was: {line}")
"""
        code_file = os.path.join(self.temp_dir, "test_input.py")
        with open(code_file, 'w') as f:
            f.write(code_content)

        # Create input file
        input_file = os.path.join(self.temp_dir, "input.txt")
        with open(input_file, 'w') as f:
            f.write("test input\n")

        # Output file
        output_file = os.path.join(self.temp_dir, "output.txt")

        # Execute
        success, error = self.executor.execute(code_file, input_file, output_file)

        # Verify
        self.assertTrue(success, f"Execution failed: {error}")
        
        # Check output
        with open(output_file, 'r') as f:
            output = f.read().strip()
        self.assertEqual(output, "Input was: test input")

    def test_execute_nonexistent_code_file(self):
        """Test execution with nonexistent code file."""
        input_file = os.path.join(self.temp_dir, "input.txt")
        output_file = os.path.join(self.temp_dir, "output.txt")
        
        # Create input file
        with open(input_file, 'w') as f:
            f.write("")

        success, error = self.executor.execute("nonexistent.py", input_file, output_file)
        
        self.assertFalse(success)
        self.assertIn("Code file not found", error)

    def test_execute_nonexistent_input_file(self):
        """Test execution with nonexistent input file."""
        code_file = os.path.join(self.temp_dir, "test.py")
        output_file = os.path.join(self.temp_dir, "output.txt")
        
        # Create code file
        with open(code_file, 'w') as f:
            f.write("print('test')")

        success, error = self.executor.execute(code_file, "nonexistent_input.txt", output_file)
        
        self.assertFalse(success)
        self.assertIn("Input file not found", error)

    def test_execute_syntax_error(self):
        """Test execution with syntax error in code."""
        # Create a Python script with syntax error
        code_content = """
print("Hello World"
# Missing closing parenthesis
"""
        code_file = os.path.join(self.temp_dir, "syntax_error.py")
        with open(code_file, 'w') as f:
            f.write(code_content)

        # Create input file
        input_file = os.path.join(self.temp_dir, "input.txt")
        with open(input_file, 'w') as f:
            f.write("")

        # Output file
        output_file = os.path.join(self.temp_dir, "output.txt")

        # Execute
        success, error = self.executor.execute(code_file, input_file, output_file)

        # Verify failure
        self.assertFalse(success)
        self.assertIn("Execution failed", error)


if __name__ == '__main__':
    unittest.main()
