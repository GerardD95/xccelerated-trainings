"""
    Update:
        - Replaced the default int() parser with a custom one, named to_int().

    Execution Time (10m rows): 
        - cpython:  8.362874208018184   result: - 0.719628125079908
        - pypy:     1.5105964170070365  result: + 0.1345866660121828

    Execution Time (1b rows):
        - pypy:     145.03504345891997 = 2.41 minutes
"""

from collections import defaultdict

def to_int(x: bytes) -> int:
    # Parse sign
    if x[0] == 45: # ASCII for "-"
        sign = -1
        idx = 1
    else:
        sign = 1
        idx = 0

    # Check the position of the decimal point
    if x[idx + 1] == 46: # ASCII for "."
        return sign * ((x[idx] * 10 + x[idx + 2]) - 528)
    else:
        return sign * ((x[idx] * 100 + x[idx + 1] * 10 + x[idx + 3]) - 5328)

def main(file_path: str) -> dict:
    cities = defaultdict(lambda: [0] * 4)

    with open(file_path, "rb") as f:

        for line in f:
            idx = line.index(b";")
            city = line[:idx]
            measurement = to_int(line[idx+1:])

            city_stats = cities[city]
            city_stats[0] = min(city_stats[0], measurement)
            city_stats[1] = max(city_stats[1], measurement)
            city_stats[2] += measurement
            city_stats[3] += 1

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