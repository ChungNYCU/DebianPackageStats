import unittest
from unittest.mock import patch

from mock import mock_open
import requests
from debian_package_stats import get_all_filenames, download_contents_index

URL = 'http://ftp.uk.debian.org/debian/dists/stable/main/'

class TestDebianPackageStats(unittest.TestCase):

    @patch('requests.get')
    def test_get_all_filenames_success(self, mock_get):
        # Mock the requests.get method to return a successful response

        # Arrange
        mock_response = mock_get.return_value
        mock_response.status_code = 200
        mock_response.text = """
            <html>
                <a href="Contents1">Link 1</a>
                <a href="Contents2">Link 2</a>
                <a href="Other">Other Link</a>
            </html>
        """
        # Act
        filenames = get_all_filenames()

        # Assert
        self.assertEqual(filenames, ["Contents1", "Contents2"])

    @patch('requests.get')
    def test_get_all_filenames_failure(self, mock_get):
        # Mock the requests.get method to simulate a failed response

        # Arrange
        mock_response = mock_get.return_value
        mock_response.status_code = 404  # Simulate a 404 error

        # Act
        filenames = get_all_filenames()

        # Assert
        self.assertIsNone(filenames)
    
    @patch('requests.get')
    @patch('builtins.open', new_callable=mock_open)
    def test_download_contents_index_success(self, mock_file_open, mock_requests_get):
        # Arrange
        mock_response = mock_requests_get.return_value
        mock_response.status_code = 200
        mock_response.iter_content.return_value = [b'This', b' is', b' a', b' test']
        filename = 'test.gz'

        # Act
        result = download_contents_index(filename)

        # Assert
        mock_requests_get.assert_called_once_with(URL+filename, stream=True)
        mock_response.raise_for_status.assert_called()
        mock_file_open.assert_called_once_with(filename, 'wb')
        mock_file = mock_file_open()
        mock_file.write.assert_called()
        self.assertEqual(result, filename)

    @patch('requests.get')
    def test_download_contents_index_request_exception(self, mock_requests_get):
        # Arrange
        mock_requests_get.side_effect = requests.exceptions.RequestException('Test exception')
        filename = 'test.gz'

        # Act
        result = download_contents_index(filename)

        # Assert
        mock_requests_get.assert_called_once_with(URL+filename, stream=True)
        self.assertEqual(result, "")


if __name__ == "__main__":
    unittest.main()