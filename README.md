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

- **Observer Pattern**: An observer pattern is employed to notify the user interface when downloads and processing are completed.

## Dependencies

The following Python libraries are used in this project:

- `requests` for making HTTP requests to Debian mirrors.
- `threading` for multi-threading support.
- `gzip` for decompressing the Contents index file.
- `unittest` for unit testing.
- `re` Utilized for regular expressions, aiding in advanced text manipulation and pattern matching within the project.
- `typing` Essential for type hinting and enhancing code readability, making it easier to understand the expected data types and function signatures.
- `bs4`(Beautiful Soup): Instrumental in parsing and extracting structured information from HTML documents, simplifying web scraping and data extraction tasks.

## Usage
To execute the tool, please follow the command structure below. You can either specify an architecture as an argument, or run it without an argument to retrieve package statistics from the mirror.

**Command Usage:**
The tool exclusively accepts the following architectures: `amd64`, `arm64`, and `mips`, with sensitivity to letter case.
```shell
python debian_package_stats.py <architecture>
```

**Example with Architecture Argument:**

```shell
python debian_package_stats.py amd64
```

**Example without Architecture Argument (Interactive Mode):**

```shell
python debian_package_stats.py
```

When running the tool without an argument, you will be prompted to select a Contents file from the mirror. Here's a sample interaction:

```shell
Retrieve filename from URL: http://ftp.uk.debian.org/debian/dists/stable/main/
Select a filename:
1. Contents-all.gz
2. Contents-amd64.gz
3. Contents-arm64.gz
4. Contents-armel.gz
5. Contents-armhf.gz
6. Contents-i386.gz
7. Contents-mips64el.gz
8. Contents-mipsel.gz
9. Contents-ppc64el.gz
10. Contents-s390x.gz
11. Contents-source.gz
12. Contents-udeb-all.gz
13. Contents-udeb-amd64.gz
14. Contents-udeb-arm64.gz
15. Contents-udeb-armel.gz
16. Contents-udeb-armhf.gz
17. Contents-udeb-i386.gz
18. Contents-udeb-mips64el.gz
19. Contents-udeb-mipsel.gz
20. Contents-udeb-ppc64el.gz
21. Contents-udeb-s390x.gz
Enter the number of your preferred filename (or 0 to exit): 2
```

Whether you use the interactive or argument-based approach, you will receive the results in a professional format:

```shell
Downloading: Contents-amd64.gz
1. devel/piglit                                         53,007
2. science/esys-particle                                18,408
3. math/acl2-books                                      16,907
4. libdevel/libboost1.74-dev,libdevel/libboost1.81-dev  14,268
5. lisp/racket                                          9,599
6. net/zoneminder                                       8,160
7. electronics/horizon-eda                              8,130
8. libdevel/libtorch-dev                                8,089
9. libdevel/liboce-modeling-dev                         7,435
10. kernel/linux-headers-6.1.0-10-amd64                 6,497
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

I spent approximately 4 hours on this exercise.
