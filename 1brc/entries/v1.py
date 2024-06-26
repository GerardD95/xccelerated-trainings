"""
    Initial Version:
        - Using a CityStats class to hold the inplace updated min, max, sum and count values.

    Execution Time (10m rows): 
        - cpython:  7.0134523750748485
        - pypy:     4.09423995797988
"""

from collections import defaultdict

class CityStats:
    def __init__(self):
        self.min = float('inf')
        self.max = float('-inf')
        self.sum = 0
        self.count = 0

    def add_measurement(self, measurement):
        self.min = min(self.min, measurement)
        self.max = max(self.max, measurement)
        self.sum += measurement
        self.count += 1

    def mean(self):
        return (self.sum / self.count) if self.count else None


def main(file_path: str) -> dict:
    cities = defaultdict(CityStats)

    with open(file_path, "r") as f:
        for line in f:
            city, measurement = line.strip().split(";")
            measurement = float(measurement) * 10 # multiply by 10 to prevent rounding errors
            cities[city].add_measurement(measurement)

    return cities


if __name__ == '__main__':
    import sys

    # Get the file path
    file_path = str(sys.argv[1])

    # Process the file
    cities = main(file_path)

    # Print the measurements per city
    for city in sorted(cities.keys()):
        stats = cities[city]
        print(f"{city}={stats.min / 10:.1f}/{stats.mean() / 10:.1f}/{stats.max / 10:.1f}")