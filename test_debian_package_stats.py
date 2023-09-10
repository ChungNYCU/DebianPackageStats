import unittest
from unittest.mock import patch
from debian_package_stats import get_all_filenames  

class TestDebianPackageStats(unittest.TestCase):
    @patch('debian_package_stats.requests.get')
    def test_get_all_filenames_success(self, mock_get):
        # Mock the requests.get method to return a successful response
        mock_response = mock_get.return_value
        mock_response.status_code = 200
        mock_response.text = """
            <html>
                <a href="Contents1">Link 1</a>
                <a href="Contents2">Link 2</a>
                <a href="Other">Other Link</a>
            </html>
        """

        filenames = get_all_filenames()

        self.assertEqual(filenames, ["Contents1", "Contents2"])

    @patch('debian_package_stats.requests.get')
    def test_get_all_filenames_failure(self, mock_get):
        # Mock the requests.get method to simulate a failed response
        mock_response = mock_get.return_value
        mock_response.status_code = 404  # Simulate a 404 error

        filenames = get_all_filenames()

        self.assertIsNone(filenames)

if __name__ == "__main__":
    unittest.main()