import sys
from collections import defaultdict

if __name__ == "__main__":
    f = sys.argv[1]

    with open(f, "r") as f: # Read as ascii rather than unicode
        output = defaultdict(list)
        result = {}

        while line := f.readline(): # Readline goes over each char
            city, temp = line.split(";") # Split goes over each char
            output[city].append(int(float(temp) * 10)) # Append slow

        for key, value in output.items(): # Rolling values rather than calculating after
            d = {
                "min": min(value),
                "max": max(value),
                "avg": sum(value) / len(value),
            }
            result[key] = d

    for key, value in sorted(result.items()):
        print(
            f"{key}={value['min']/10:.1f}/{value['avg']/10:.1f}/{value['max']/10:.1f}",
        )

# Rolling values rather than calculating after
# Dict lookup slow(ish)
# Append sucks (performance wise)
# Readline goes over each char
# Split goes over each char
# Read as ascii rather than unicode

# Parallelism?
