import unittest
import subprocess
from pathlib import Path

class TestMiniLs(unittest.TestCase):
    def setUp(self):
        # Base path where the script and test files are located
        self.base_path = Path(__file__).parent
        self.mini_ls_path = self.base_path / "mini-ls"
        
        # Create a test directory that will be used in various tests
        self.test_dir = self.base_path / "test_dir"
        self.test_dir.mkdir(exist_ok=True)

    def run_mini_ls(self, args=None):
        """Helper function to run mini-ls with optional extra arguments."""
        command = [str(self.mini_ls_path)]
        if args:
            command.extend(args)
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return result.stdout, result.stderr

    def test_file_listing(self):
        """Test listing of a single known file."""
        known_file = self.test_dir / "known_file.txt"
        known_file.touch()  # Ensure the file exists
        output, errors = self.run_mini_ls([str(known_file)])
        self.assertIn("known_file.txt", output)

    def test_directory_listing_default(self):
        """Test listing of current directory when no arguments are given."""
        output, errors = self.run_mini_ls()
        self.assertIn("test_dir", output)  # Assuming 'test_dir' is in the output

    def test_recursive_listing(self):
        """Test the recursive listing functionality."""
        test_file = self.test_dir / "test_file.txt"
        test_file.touch()
        output, errors = self.run_mini_ls(["-r", str(self.test_dir)])
        self.assertIn("test_file.txt", output)

    def tearDown(self):
        """Cleanup any persistent changes made by tests."""
        # Remove any files created within the test directory
        for item in self.test_dir.glob('*'):
            if item.is_dir():
                for subitem in item.rglob('*'):
                    subitem.unlink()
                item.rmdir()
            else:
                item.unlink()
        # Remove the test directory itself if it's empty
        self.test_dir.rmdir()

if __name__ == '__main__':
    unittest.main()
