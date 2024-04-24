import unittest
import subprocess
from pathlib import Path
import sys
from io import StringIO

class TestMiniDf(unittest.TestCase):
    def setUp(self):
        # Determine the path to the mini-df script
        self.script_path = Path(__file__).parent / "mini-df"
        # Capture stdout and stderr
        self.original_stdout = sys.stdout
        self.original_stderr = sys.stderr
        self.held_stdout = StringIO()
        self.held_stderr = StringIO()
        sys.stdout = self.held_stdout
        sys.stderr = self.held_stderr

    def run_script(self, args=None):
        """Helper function to run the mini-df script with optional arguments."""
        command = ['python3', str(self.script_path)]
        if args:
            command.extend(args)
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return result.stdout, result.stderr

    def test_basic_output(self):
        """Test output without any arguments."""
        stdout, stderr = self.run_script()
        self.assertIn("Total Space:", stdout)
        self.assertIn("Used Space:", stdout)
        self.assertIn("Free Space:", stdout)

    def test_human_readable(self):
        """Ensure human-readable format is applied correctly and dynamically check for units."""
        stdout, stderr = self.run_script(['-h'])
        # Possible units to check
        possible_units = [" KB", " MB", " GB", " TB"]
        # Ensure at least one unit is found in the output, format-wise
        self.assertTrue(any(unit in stdout for unit in possible_units), f"Expected one of {possible_units} in output, got: {stdout}")

    def test_multiple_paths(self):
        """Test output for multiple paths."""
        stdout, stderr = self.run_script(['/tmp', '/var'])
        self.assertIn("/tmp", stdout)
        self.assertIn("/var", stdout)
        self.assertIn("Total Space:", stdout)
        self.assertGreater(stdout.count("Total Space:"), 1)

    def test_invalid_path(self):
        """Test response to an invalid path."""
        stdout, stderr = self.run_script(['/surelythisdoesnotexist'])
        self.assertIn("Error: The path '/surelythisdoesnotexist' does not exist.", stderr)

    def test_permission_issues(self):
        """Test output when encountering permission issues.
        Expecting a 'Permission denied' error as a correct response to restricted access."""
        stdout, stderr = self.run_script(['/root'])  # Using '/root' which is generally restricted
        if "Permission denied" in stderr:
            # If the error is found, we consider this a successful outcome.
            self.assertTrue(True, "Permission error correctly reported.")
        else:
            # If no error is found, that is considered a failure of the test.
            self.fail(f"Expected 'Permission denied' but got: {stderr}")


    def tearDown(self):
        # Restore stdout and stderr
        sys.stdout = self.original_stdout
        sys.stderr = self.original_stderr

if __name__ == '__main__':
    unittest.main()
