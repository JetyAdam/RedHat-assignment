import unittest
import subprocess

class TestMiniGrep(unittest.TestCase):

    def run_script(self, args, input_text=None):
        """Utility method to run the script with given arguments and optional stdin."""
        process = subprocess.Popen(['./mini-grep'] + args,
                                   stdin=subprocess.PIPE,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE,
                                   text=True)
        stdout, stderr = process.communicate(input=input_text)
        return stdout, stderr, process.returncode

    def test_complex_patterns(self):
        # Input text includes various special characters and scenarios
        input_text = "This is a test.\nMaybe a second test line?\n123-456-7890\nThis line has a special regex character [ and ].\nend."

        # Test with a complex regex pattern that includes a regex special character
        stdout, stderr, exit_code = self.run_script(['-e', r'\d{3}-\d{3}-\d{4}'], input_text)
        self.assertIn('3:123-456-7890', stdout, "Should find the phone number format")

        # Test a regex that includes literal brackets
        stdout, stderr, exit_code = self.run_script(['-e', r'\[ and \]'], input_text)
        self.assertIn('4:This line has a special regex character [ and ].', stdout, "Should match line with brackets")

        # Test the absence of matches with another pattern
        stdout, stderr, exit_code = self.run_script(['-e', 'xyz'], input_text)
        self.assertEqual('', stdout, "Should not find any matches")
        self.assertEqual('No matches found.\n', stderr, "Should indicate no matches were found")

        # Test using multiple flags and checking for no errors
        stdout, stderr, exit_code = self.run_script(['-q', '-e', 'test'], input_text)
        self.assertIn('test', stdout, "Quiet mode should omit line numbers but still show matches")
        self.assertTrue(':' not in stdout, "Line numbers should be omitted in quiet mode")
        self.assertEqual('', stderr, "There should be no error messages")

if __name__ == '__main__':
    unittest.main()
