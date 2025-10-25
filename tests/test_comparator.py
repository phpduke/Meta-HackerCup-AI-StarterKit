"""
Unit tests for OutputComparator utility.
"""
import unittest
import tempfile
import os
from utils.comparator import OutputComparator


class TestOutputComparator(unittest.TestCase):
    """Test cases for OutputComparator class."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        """Clean up test fixtures."""
        # Clean up temporary files
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_compare_identical_files(self):
        """Test comparison of identical files."""
        content = "Hello World\n123\n"
        
        file1 = os.path.join(self.temp_dir, "file1.txt")
        file2 = os.path.join(self.temp_dir, "file2.txt")
        
        with open(file1, 'w') as f:
            f.write(content)
        with open(file2, 'w') as f:
            f.write(content)

        result = OutputComparator.compare(file1, file2)
        self.assertTrue(result)

    def test_compare_different_files(self):
        """Test comparison of different files."""
        file1 = os.path.join(self.temp_dir, "file1.txt")
        file2 = os.path.join(self.temp_dir, "file2.txt")
        
        with open(file1, 'w') as f:
            f.write("Hello World")
        with open(file2, 'w') as f:
            f.write("Goodbye World")

        result = OutputComparator.compare(file1, file2)
        self.assertFalse(result)

    def test_compare_whitespace_differences(self):
        """Test comparison ignoring leading/trailing whitespace."""
        file1 = os.path.join(self.temp_dir, "file1.txt")
        file2 = os.path.join(self.temp_dir, "file2.txt")
        
        with open(file1, 'w') as f:
            f.write("  Hello World  \n")
        with open(file2, 'w') as f:
            f.write("Hello World")

        result = OutputComparator.compare(file1, file2)
        self.assertTrue(result)

    def test_compare_nonexistent_file1(self):
        """Test comparison with nonexistent first file."""
        file2 = os.path.join(self.temp_dir, "file2.txt")
        with open(file2, 'w') as f:
            f.write("content")

        result = OutputComparator.compare("nonexistent.txt", file2)
        self.assertFalse(result)

    def test_compare_nonexistent_file2(self):
        """Test comparison with nonexistent second file."""
        file1 = os.path.join(self.temp_dir, "file1.txt")
        with open(file1, 'w') as f:
            f.write("content")

        result = OutputComparator.compare(file1, "nonexistent.txt")
        self.assertFalse(result)

    def test_get_diff_summary_identical(self):
        """Test diff summary for identical files."""
        content = "Hello World"
        
        file1 = os.path.join(self.temp_dir, "file1.txt")
        file2 = os.path.join(self.temp_dir, "file2.txt")
        
        with open(file1, 'w') as f:
            f.write(content)
        with open(file2, 'w') as f:
            f.write(content)

        diff = OutputComparator.get_diff_summary(file1, file2)
        self.assertEqual(diff, "Outputs match!")

    def test_get_diff_summary_different(self):
        """Test diff summary for different files."""
        file1 = os.path.join(self.temp_dir, "file1.txt")
        file2 = os.path.join(self.temp_dir, "file2.txt")
        
        with open(file1, 'w') as f:
            f.write("Expected output")
        with open(file2, 'w') as f:
            f.write("Actual output")

        diff = OutputComparator.get_diff_summary(file1, file2)
        self.assertIn("Outputs differ", diff)
        self.assertIn("Expected:", diff)
        self.assertIn("Actual:", diff)
        self.assertIn("Expected output", diff)
        self.assertIn("Actual output", diff)


if __name__ == '__main__':
    unittest.main()
