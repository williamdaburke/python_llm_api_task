"""Unit tests for extract_requirements.py"""
import os
import unittest
from extract_requirements import read_file, preprocess_text, simulate_llm_summary, split_text


class TestFunctions(unittest.TestCase):
    """
    Unit tests for extract_requirements.py
    """
    def test_read_file(self):
        """
        Test reading file
        """
        # Create a temporary file for testing
        with open('test_file.txt', 'w') as file:
            file.write('Hello World!')
        self.assertEqual(read_file('test_file.txt'), 'Hello World!')
        os.remove('test_file.txt')

    def test_preprocess_text(self):
        """
        Test preprocessing a sample text
        """
        text = '<p>Hello, World!</p>'
        expected_output = 'hello world'
        self.assertEqual(preprocess_text(text), expected_output)

    def test_split_text(self):
        """
        Test simulate_llm_summary in a sample text
        """
        text = """
        this is a test\n\nso is this
        and this
        
        and this
        - here too
        """
        expected_output = ['this is a test','so is this', 'and this','and this', '- here too']
        self.assertEqual(split_text(text), expected_output)

    def test_simulate_llm_summary(self):
        """
        Test simulate_llm_summary in a sample text
        """
        text = 'this is a test'
        expected_output = 'test a is this'
        self.assertEqual(simulate_llm_summary(text), expected_output)

if __name__ == '__main__':
    unittest.main()
