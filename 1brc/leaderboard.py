import itertools as it
import pathlib
import subprocess
from collections import defaultdict
from timeit import default_timer as timer
import polars as pl
import sys
import sys


def make_ground_truth(txt_file):

    df = pl.scan_csv(
        txt_file,
        separator=";",
        has_header=False,
        with_column_names=lambda _: ["station_name", "measurement"],
    )

    grouped = (
        df.with_columns((pl.col("measurement") * 10).cast(pl.Int32).alias("measurement"))
        .group_by("station_name")
        .agg(
            pl.min("measurement").alias("min_measurement"),
            pl.mean("measurement").alias("mean_measurement"),
            pl.max("measurement").alias("max_measurement"),
        )
        .sort("station_name")
        .collect(streaming=True)
    )
    result = []
    for data in grouped.iter_rows():
        result.append(f"{data[0]}={data[1]/10:.1f}/{data[2]/10:.1f}/{data[3]/10:.1f}")
    return result


entries = list(pathlib.Path("entries/").glob("*.py"))
if len(sys.argv) < 2:
    print("Please provide a file path with the measurements. Usage: python leaderboard.py <file_path>")
    sys.exit()
file_path = str(sys.argv[1])

print("Generating ground truths")
ground_truth = make_ground_truth(file_path)

print("The following entries will be verified")
for entry in entries:
    print(f" - {entry}")


def compare(ground_truth, result):
    for l, r in zip(ground_truth, result):
        if l != r:
            yield f"{l}  !=  {r}"


times = defaultdict(list)
for entry in entries:
    print(f"========== {entry} ==========")
    for i in range(3):
        try:
            tic = timer()
            res = subprocess.run(
                ["python", entry, file_path],
                encoding="utf-8",
                capture_output=True,
                text=True,
            )
            toc = timer()
            res.check_returncode()
        except Exception as e:
            print(f"entry {entry} failed to run succesfully: {e}")
        else:
            print("comparing result to ground truth")
            diff = list(it.islice(compare(ground_truth, res.stdout.splitlines()), 10))

            if len(diff) != 0:
                print(f"{entry} has differences with ground truth, showing first 10")

                for diff_entry in diff:
                    print(diff_entry)
            else:
                times[entry].append(toc - tic)

    print()
    print(f"========== leaderboard ==========")
    print()
    print()

    picked_times = []
    for entry_name, entry_times in times.items():
        picked_time = sorted(entry_times)[len(entry_times) // 2]
        picked_times.append((picked_time, entry_name))

    idx = 1
    for entry_time, entry_name in sorted(picked_times):
        print(f"#{idx}: {entry_name} with {entry_time}")
        idx += 1
