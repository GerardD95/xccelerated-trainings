from collections import defaultdict
from multiprocessing import Pool, cpu_count
from itertools import islice
import sys
from tqdm import tqdm

from utils.city_stats import CityStats, print_cities


def process_line(line):
    line = line.strip()
    city, measurement = line.split(";")
    measurement = float(measurement)
    return city, measurement

def update_cities(chunk):
    local_cities = defaultdict(CityStats)
    for line in chunk:
        city, measurement = process_line(line)
        local_cities[city].add_measurement(measurement)
    return local_cities

def chunks(file, n):
    """Yield successive n-sized chunks from file."""
    while True:
        lines = list(islice(file, n))
        if not lines:
            break
        yield lines

def main():
    # Initialize the cities dictionary and get the file path
    cities = defaultdict(CityStats)
    file_path = str(sys.argv[1])

    # Process the file
    with open(file_path, "r") as f:
        chunk_size = 10_000_000  # Adjust the chunk size as needed
        with Pool(cpu_count()) as p:
            results = p.map(update_cities, chunks(f, chunk_size))

    # Merge the result
    for result in results:
        for city, stats in result.items():
            cities[city].min = min(cities[city].min, stats.min)
            cities[city].max = max(cities[city].max, stats.max)
            cities[city].sum += stats.sum
            cities[city].count += stats.count

    # Print the measurements per city
    print_cities(cities)

if __name__ == '__main__':
    main()
