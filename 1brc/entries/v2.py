"""
    Update: 
        - Replaced the CityStats class with a list data structure.     

    Execution Time (10m rows):         
        - cpython: 7.108697833027691 
        - pypy: 3.6854527500690892 
"""

def main(file_path: str) -> dict: 
    cities = {}

    with open(file_path, "r") as f:
        for line in f:
            city, measurement = line.strip().split(";")
            measurement = float(measurement) * 10

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
        print(f"{city}={stats[0] / 10.0:.1f}/{stats[2] / 10 / stats[3]:.1f}/{stats[1] / 10.0:.1f}")  # divide by 10.0