import os


class OutputComparator:
    """Utility to compare output files."""

    @staticmethod
    def compare(file1: str, file2: str) -> bool:
        """
        Compare two output files, ignoring leading/trailing whitespace.

        Args:
            file1: Path to first file
            file2: Path to second file

        Returns:
            True if files match (after stripping whitespace), False otherwise
        """
        if not os.path.exists(file1):
            return False

        if not os.path.exists(file2):
            return False

        try:
            with open(file1, 'r') as f1:
                content1 = f1.read().strip()

            with open(file2, 'r') as f2:
                content2 = f2.read().strip()

            return content1 == content2

        except Exception:
            return False

    @staticmethod
    def get_diff_summary(file1: str, file2: str) -> str:
        """
        Get a summary of differences between two files.

        Args:
            file1: Path to expected output
            file2: Path to actual output

        Returns:
            String describing the differences
        """
        try:
            with open(file1, 'r') as f1:
                expected = f1.read().strip()

            with open(file2, 'r') as f2:
                actual = f2.read().strip()

            if expected == actual:
                return "Outputs match!"

            summary = "Outputs differ:\n"
            summary += f"Expected:\n{expected[:500]}\n\n"
            summary += f"Actual:\n{actual[:500]}\n"

            return summary

        except Exception as e:
            return f"Error comparing files: {str(e)}"
