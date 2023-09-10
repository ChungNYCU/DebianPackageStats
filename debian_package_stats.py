import gzip
import re
import threading
from typing import Any, List, Tuple, Union

import requests
from bs4 import BeautifulSoup

URL = 'http://ftp.uk.debian.org/debian/dists/stable/main/'

# Define an Observer interface
class Observer:
    def update(self, message: str) -> None:
        pass

class Package:
    def __init__(self, data: Any) -> None:
        self.data = data


class File:
    def __init__(self, data: Any) -> None:
        self.data = data


class DownloadQueueManager:
    _instance = None

    def __new__(cls) -> "DownloadQueueManager":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.queue = []
        return cls._instance

    def add_to_queue(self, item: Any) -> None:
        self.queue.append(item)

    def get_queue_size(self) -> int:
        return len(self.queue)

class DownloadManager:
    def __init__(self) -> None:
        self.observers: List[Observer] = []

    def add_observer(self, observer: Observer) -> None:
        self.observers.append(observer)

    def notify_observers(self, message: str) -> None:
        for observer in self.observers:
            observer.update(message)

class UserInterface(Observer):
    def update(self, message: str) -> None:
        print(f"User interface notified: {message}")

def get_all_filenames() -> Union[List[str], None]:

    try:
        # Send an HTTP GET request to the URL
        response = requests.get(URL)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the HTML content of the page
            soup = BeautifulSoup(response.text, 'html.parser')

            # Find all anchor tags (links) in the page
            links = soup.find_all('a')

            # Extract filenames containing "Contents"
            filenames = [link['href'] for link in links if re.search(r'Contents', link['href'])]
            return filenames
        else:
            print('Failed to retrieve the directory listing.')
            return None
    except requests.exceptions.RequestException as e:
        print(f'Error making the HTTP request: {e}')
        return None
    
def download_contents_index(filename: str) -> str:
    # Construct the full URL by appending the 'filename' to the base 'URL'.
    url = URL + filename

    try:
        # Send an HTTP GET request to the URL and stream the response.
        response = requests.get(url, stream=True)
        
        # Check if the HTTP response status code indicates success (2xx).
        response.raise_for_status()

        # Open a file in binary write ('wb') mode to save the downloaded content.
        with open(filename, "wb") as content_file:
            # Iterate over the response content in chunks of 8192 bytes.
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    content_file.write(chunk)

        # Return the filename as a signal of success.
        return filename

    except requests.exceptions.RequestException as e:
        # Handle any exceptions raised during the request, such as network errors.
        print(f"Error downloading Contents index: {e}")
        
        # Return an empty string to indicate failure.
        return ""


def parse_contents_index(contents_data: Any) -> Any:
    pass

def get_top_10_packages(package_data: Any) -> List[Tuple[str, int]]:
    pass

def main() -> None:
    download_manager = DownloadManager()
    download_manager.add_observer(UserInterface())

    filenames = get_all_filenames()

    # Check if filenames were retrieved successfully
    if filenames:
        print(f"Retrieve filename from url: {URL}")
        print("Select a filename:")
        for idx, filename in enumerate(filenames, start=1):
            print(f"{idx}. {filename}")

        while True:
            try:
                choice = int(input("Enter the number of your preferred filename (or 0 to exit): "))
                if 0 <= choice <= len(filenames):
                    if choice == 0:
                        break
                    selected_filename = filenames[choice - 1]
                    print(f"Downloading: {selected_filename}")
                    # Download Contents index
                    contents_data = download_contents_index(selected_filename)

                    # Parse Contents index
                    # package_data = parse_contents_index(contents_data)

                    # Calculate and display statistics
                    # top_packages = get_top_10_packages(package_data)
                    # for package, num_files in top_packages:
                    #     print(f"{package}\t{num_files}")
                    print(contents_data)
                else:
                    print("Invalid choice. Please enter a valid number.")
            except ValueError:
                print("Invalid input. Please enter a number.")
    else:
        print("Unable to find any files. Please check if the URL is correct.")


if __name__ == "__main__":
    main()
