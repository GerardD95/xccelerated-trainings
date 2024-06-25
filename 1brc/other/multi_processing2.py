import sys
import csv
import multiprocessing as mp
from itertools import islice
from collections import defaultdict

# Define the size of chunks to read
CHUNK_SIZE = 700_000

def read_in_chunks(file_name, chunk_size=CHUNK_SIZE):
    """Generator to read a file in chunks."""
    with open(file_name, 'r') as file:
        while True:
            lines = list(islice(file, chunk_size))
            if not lines:
                break
            yield lines

def process_chunk(lines):
    """Process a chunk of lines and return the aggregated results."""
    results = {}
    
    for line in lines:
        station_name, measurement = line.strip().split(';')
        measurement = int(float(measurement) * 10)
        
        if station_name not in results:
            results[station_name] = [
                measurement,  # min
                measurement,  # max
                measurement,  # sum
                1,            # count
            ]
        else:
            results[station_name][0] = min(results[station_name][0], measurement)
            results[station_name][1] = max(results[station_name][1], measurement)
            results[station_name][2] += measurement
            results[station_name][3] += 1
   
    return results

def combine_results(results_list):
    """Combine results from multiple chunks."""
    # Merge the result
    cities = defaultdict(list)
    for result in results_list:
        for city, stats in result.items():
            if not cities[city]:  # If the city is not in the dictionary, initialize its stats
                cities[city] = stats
            else:  # If the city is already in the dictionary, update its stats
                cities[city][0] = min(cities[city][0], stats[0])
                cities[city][1] = max(cities[city][1], stats[1])
                cities[city][2] += stats[2]
                cities[city][3] += stats[3]
    
    # Calculate mean for each city
    for city, stats in cities.items():
        stats.append(stats[2] / stats[3])  # Append the mean to the list of stats
    
    return cities

def parallel_process(file_name):
    """Process the file in parallel and aggregate the results."""
    pool = mp.Pool(mp.cpu_count())
    
    chunk_results = [pool.apply_async(process_chunk, (chunk,)) for chunk in read_in_chunks(file_name)]
    
    pool.close()
    pool.join()
    
    # Collect results from all chunks
    results = [res.get() for res in chunk_results]
    
    # Combine results from all chunks
    final_results = combine_results(results)
    
    return final_results

def print_results(results):
    """Print the final aggregated results."""
    sorted_results = dict(sorted(results.items(), key=lambda x: x[0]))
    
    for city, stats in sorted_results.items():
        min_measurement = stats[0]
        mean_measurement = stats[-1]
        max_measurement = stats[1]
        print(f"{city}={min_measurement / 10:.1f}/{mean_measurement / 10:.1f}/{max_measurement / 10:.1f}")

if __name__ == "__main__":
    file_name = str(sys.argv[1])
    results = parallel_process(file_name)
    print_results(results)
