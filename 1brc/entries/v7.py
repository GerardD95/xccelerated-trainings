"""
    Update:
        - Used mmap to read the file in memory instead of reading it line by line.

    Execution Time (10m rows): 
        - cpython:  8.139350124984048   result: - 0.223524083034136
        - pypy:     1.2586491249967366  result: - 0.2519472920103

    Execution Time (1b rows):
        - pypy:     ...
"""

from collections import defaultdict
import mmap
import array

def to_int(x: bytes) -> int:
    # Parse sign
    sign = -1 if x[0] == 45 else 1
    idx = 1 if x[0] == 45 else 0

    # Check the position of the decimal point
    if x[idx + 1] == 46: # ASCII for "."
        return sign * ((x[idx] * 10 + x[idx + 2]) - 528) # Subtract 11 * 48 (ASCII for '0')
    else:
        return sign * ((x[idx] * 100 + x[idx + 1] * 10 + x[idx + 3]) - 5328) # Subtract 111 * 48 (ASCII for '0')

def process_line(line: bytes, cities: dict) -> None:
    idx = line.index(b";")
    city = line[:idx]
    measurement = to_int(line[idx+1:])

    city_stats = cities[city]
    city_stats[0] = min(city_stats[0], measurement)
    city_stats[1] = max(city_stats[1], measurement)
    city_stats[2] += measurement
    city_stats[3] += 1

def main(file_path: str) -> dict:
    cities = defaultdict(lambda: array.array('i', [int()] * 4))

    with open(file_path, "rb") as f:
        with mmap.mmap(f.fileno(), length=0, access=mmap.ACCESS_READ) as mm:
            start = 0
            while True:
                end = mm.find(b'\n', start)  # Find the next newline
                if end == -1:  # No more lines
                    break
                line = mm[start:end]  # Extract the line
                start = end + 1  # Move the start to the next character after the newline

                process_line(line, cities)

    return cities

if __name__ == '__main__':
    import sys

    # Get the file path 
    file_path = sys.argv[1]

    # Process the file
    cities = main(file_path)

    # Print the measurements per city
    for city in sorted(cities.keys()):
        stats = cities[city]
        print(f"{city.decode()}={stats[0] / 10.0:.1f}/{stats[2] / 10 / stats[3]:.1f}/{stats[1] / 10.0:.1f}")  # divide by 10.0