"""
    Update:
        - Replaced the float() conversion with int() directly by locating the index.

    Execution Time (10m rows): 
        - cpython: 7.969962834031321
        - pypy: 1.77662079106085
"""

def main(file_path: str) -> dict:
    cities = {}

    with open(file_path, "rb") as f:
        for line in f:
            idx = line.index(b";")
            city = line[:idx]
            measurement = int(line[idx+1:-3] + line[-2:-1])

            if city in cities:
                city_stats = cities[city]
                city_stats[0] = min(city_stats[0], measurement)
                city_stats[1] = max(city_stats[1], measurement)
                city_stats[2] += measurement
                city_stats[3] += 1
            else:
                cities[city] = [measurement, measurement, measurement, 1]
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