"""
    Update:
        - Using page size optimization 
        - Yielding chunks of the file        

    Execution Time (10m rows): 
        - cpython:  1.3574103749124333  result: - 6.781939750071614  
        - pypy:     0.5453084169421345  result: - 0.7133407080546021

    Execution Time (1b rows):
        - pypy:     ... 
"""

import multiprocessing
import os
import mmap
import array
from collections import defaultdict
from typing import Generator

CPU_COUNT = os.cpu_count()

def to_int(x: bytes) -> int:
    # Parse sign
    sign = -1 if x[0] == 45 else 1
    idx = 1 if x[0] == 45 else 0

    # Check the position of the decimal point
    if x[idx + 1] == 46: # ASCII for "."
        return sign * ((x[idx] * 10 + x[idx + 2]) - 528) # Subtract 11 * 48 (ASCII for '0')
    else:
        return sign * ((x[idx] * 100 + x[idx + 1] * 10 + x[idx + 3]) - 5328) # Subtract 111 * 48 (ASCII for '0')

def update_city_stats(city: bytes, measurement: int, cities: dict) -> None: 
    city_stats = cities[city]
    city_stats[0] = min(city_stats[0], measurement)
    city_stats[1] = max(city_stats[1], measurement)
    city_stats[2] += measurement
    city_stats[3] += 1

def chunk_file(file_path: str) -> Generator[bytes, None, None]:
    file_size_bytes = os.path.getsize(file_path)
    base_chunk_size = file_size_bytes // CPU_COUNT

    with open(file_path, "rb") as file:
        with mmap.mmap(
            file.fileno(), length=0, access=mmap.ACCESS_READ
        ) as mmapped_file:
            start_byte = 0
            for _ in range(CPU_COUNT):
                end_byte = min(start_byte + base_chunk_size, file_size_bytes)
                end_byte = mmapped_file.find(b"\n", end_byte)
                end_byte = end_byte + 1 if end_byte != -1 else file_size_bytes
                yield (mmapped_file[start_byte:end_byte],)
                start_byte = end_byte

def init_array():
    return array.array('i', [int()] * 4)

def main(mmapped_file_chunk: bytes) -> dict:
    cities = defaultdict(init_array) 

    for line in mmapped_file_chunk.splitlines():
        # Process the line
        idx = line.index(b";")
        city = line[:idx]
        measurement = to_int(line[idx+1:])
        
        # Update the city stats
        update_city_stats(city, measurement, cities)

    return cities

def reduce_results(results):
    cities = defaultdict(init_array) 

    # Merge the results by comparing the individual chunk results
    for res in results:
        for city, item in res.items():
            city_stats = cities[city]
            city_stats[0] = min(city_stats[0], item[0])
            city_stats[1] = max(city_stats[1], item[1])
            city_stats[2] += item[2]
            city_stats[3] += item[3]

            # update_city_stats(city, item, cities)

    return cities

if __name__ == '__main__':
    import sys

    # Get the file path 
    file_path = sys.argv[1]

    # Process the chunks in parallel in the main function
    with multiprocessing.Pool(processes=CPU_COUNT) as p:
        cities: list[dict] = p.starmap(main, chunk_file(file_path))

    # Reduce the results
    final_results: dict = reduce_results(cities) 

    # Print the measurements per city
    for city in sorted(final_results.keys()):
        stats = final_results[city]
        print(f"{city.decode()}={stats[0] / 10.0:.1f}/{stats[2] / 10 / stats[3]:.1f}/{stats[1] / 10.0:.1f}")  # divide by 10.0