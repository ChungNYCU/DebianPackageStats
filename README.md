# DebianPackageStats

## Overview

DebianPackageStats is a Python command-line tool designed to gather statistics about Debian packages based on their contents for a specified architecture. It retrieves and parses the "Contents index" file from a Debian mirror and outputs the top 10 packages with the most files associated with them.

## Features

- **Architecture Selection**: The tool takes an architecture (e.g., amd64, arm64, mips) as an argument to focus on specific package statistics.
- **Multi-threading**: It utilizes multi-threading to download and process the Contents index file, improving performance.
- **Error Handling**: Robust error handling ensures that the tool gracefully handles exceptions and provides meaningful error messages.
- **Unit Testing**: The project includes unit tests to validate the correctness of its core functionality.

## Design Patterns

The project follows the following design patterns:

- **Singleton Pattern**: A singleton pattern is used for managing the download queue to ensure only one instance of the download manager exists.
- **Factory Pattern**: A factory pattern is used to create package objects for efficient parsing of package data.
- **Observer Pattern**: An observer pattern is employed to notify the user interface when downloads and processing are completed.

## Dependencies

The following Python libraries are used in this project:

- `requests` for making HTTP requests to Debian mirrors.
- `threading` for multi-threading support.
- `gzip` for decompressing the Contents index file.
- `unittest` for unit testing.

## Usage

To run the tool, use the following command:

```shell
python debian_package_stats.py <architecture>
```

Example:

```shell
python debian_package_stats.py amd64
```

## Multithreading

Multithreading is implemented to improve the download and processing speed of the Contents index file. Multiple threads are used to download packages in parallel, making the tool more efficient.

## Error Handling Strategy

The tool employs a robust error-handling strategy that includes:

- Handling network errors and retries for stable downloads.
- Gracefully handling exceptions and providing informative error messages to the user.

## Unit Testing

Unit tests are included in the project to verify the correctness of its core functionality. You can run the tests using the following command:

```shell
python -m unittest test_debian_package_stats.py
```

## Author

WeiChe Chung

## Time Spent

WIP
