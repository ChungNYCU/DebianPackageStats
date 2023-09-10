import gzip
import re
import sys
import threading
from typing import List, Tuple, Union

import requests
from bs4 import BeautifulSoup

URL = 'http://ftp.uk.debian.org/debian/dists/stable/main/'
NUMBERS_OF_TOP_PACKAGES = 10
CHUNK_SIZE = 8192
THREADS = 4 # 4 threads can handle Contents-amd64.gz in 5 sec on my own machine

def get_all_filenames() -> Union[List[str], None]:
    """
    Retrieve a list of filenames containing 'Contents' from a URL directory listing.

    Returns:
        Union[List[str], None]: A list of filenames if successful, or None on failure.
    """
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
    """
    Download a Contents index file from a specified URL and save it locally.

    Args:
        filename (str): The name of the Contents index file or a reserved architecture name.

    Returns:
        str: The filename of the downloaded Contents index file if successful, or an empty string on failure.
    """
    # If user passed the arg, parse the filename
    reserved_args = set(['amd64', 'arm64', 'mips'])
    if filename in reserved_args:
        if filename == 'mips':
            filename = f"Contents-{filename}64el.gz"
        else:
            filename = f"Contents-{filename}.gz"

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
            for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
                if chunk:
                    content_file.write(chunk)

        # Return the filename as a signal of success.
        return filename

    except requests.exceptions.RequestException as e:
        # Handle any exceptions raised during the request, such as network errors.
        print(f"Error downloading Contents index: {e}")
        
        # Return an empty string to indicate failure.
        return ""

def parse_contents_index(contents_data: str) -> List[Tuple[str, int]]:
    """
    Parse the Contents index data to extract package statistics.
    # Considering that the amount of data is in the millions, 
    # I decided to use multi-threading to handle the process

    Args:
        contents_data (str): The path to the Contents index file.

    Returns:
        List[Tuple[str, int]]: A list of tuples containing package names and the number of associated files.
    """
    package_stats = {}  # Dictionary to store package statistics

    def parse_lines(start, end):
        nonlocal package_stats
        try:
            with gzip.open(contents_data, "rt", encoding="utf-8") as contents_file:
                for line_number, line in enumerate(contents_file, start=1):
                    if start <= line_number <= end:
                        # the line's format like below:
                        # bin/abpoa       science/abpoa
                        parts = line.strip().split()
                        if len(parts) == 2:
                            file_path, package_name = parts
                            package_stats[package_name] = package_stats.get(package_name, 0) + 1

        except FileNotFoundError as e:
            print(f"Error parsing Contents index: {e}")

    num_lines = sum(1 for _ in gzip.open(contents_data, "rt", encoding="utf-8"))
    num_threads = min(THREADS, num_lines)  

    # Divide the lines among the threads
    step = num_lines // num_threads
    thread_ranges = [(i * step + 1, (i + 1) * step) for i in range(num_threads)]

    # Create and start threads
    threads = []
    for start, end in thread_ranges:
        thread = threading.Thread(target=parse_lines, args=(start, end))
        threads.append(thread)
        thread.start()

    # Wait for all threads to finish
    for thread in threads:
        thread.join()

    # Calculate and return statistics as a list of tuples (package_name, num_files)
    sorted_stats = sorted(package_stats.items(), key=lambda x: x[1], reverse=True)
    return sorted_stats

def get_top_x_packages(x: int, package_data: List[Tuple[str, int]]) -> List[Tuple[str, int]]:
    """
    Get the top X packages based on a specific criteria from a list of package data.

    Args:
        x (int): The number of top packages to retrieve.
        package_data (List[Tuple[str, int]]): A list of tuples containing package names and associated values.

    Returns:
        List[Tuple[str, int]]: A list of the top X packages based on the specified criteria.
    """
    return package_data[:x]

def process_selected_architecture(architecture: str) -> None:
    """
    Download, parse, and display package statistics for a selected Debian architecture.

    Args:
        architecture (str): The Debian architecture to process.

    Returns:
        None
    """
    selected_filename = architecture
    print(f"Downloading: {selected_filename}")
    
    # Download Contents index
    contents_data = download_contents_index(selected_filename)
    
    if contents_data:
        # Parse Contents index
        package_data = parse_contents_index(contents_data)
    else:
        return
    
    # Calculate and display statistics
    top_packages = get_top_x_packages(NUMBERS_OF_TOP_PACKAGES, package_data)

    max_package_length = max(len(package) for package, _ in top_packages)
    max_num_files_length = max(len(str(num_files)) for _, num_files in top_packages)
    max_length = max_package_length + max_num_files_length

    for i, (package, num_files) in enumerate(top_packages, start=1):
        # Calculate the length difference and add spaces accordingly
        space = " " * (max_length - len(str(i)) - len(package) - len(str(num_files)))
        # Print the formatted output with numbering
        print(f"{i}. {package}{space}\t{num_files}")

def display_all_contents_on_mirror() -> None:
    """
    Display a list of available Debian mirror contents and allow the user to select an architecture for analysis.

    Returns:
        None
    """
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
                    process_selected_architecture(filenames[choice - 1])
                    break
                else:
                    print("Invalid choice. Please enter a valid number.")
            except ValueError:
                print("Invalid input. Please enter a number.")
    else:
        print("Unable to find any files. Please check if the URL is correct.")

def main() -> None:
    """Main function to interact with the user and perform package statistics analysis."""

    # Check if command-line arguments were provided for architecture, only accept 'amd64', 'arm64', and 'mips'.
    if len(sys.argv) == 2:
        architecture = sys.argv[1]
        print(f"Running package statistics analysis for architecture: {architecture}")
        process_selected_architecture(architecture)
    else:
        # If user did not provide the arg, retrieve all Contents files from the mirror
        display_all_contents_on_mirror()
        
    
if __name__ == "__main__":
    main()
