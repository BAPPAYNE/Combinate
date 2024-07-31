import argparse
import time
import os
from itertools import combinations, chain
from concurrent.futures import ThreadPoolExecutor, as_completed

def generate_combinations(input_string, max_length, specified_lengths=None):
    if specified_lengths:
        lengths_to_generate = specified_lengths
    else:
        lengths_to_generate = range(1, max_length + 1)

    for length in lengths_to_generate:
        for comb in combinations(input_string, length):
            yield ''.join(comb)

def estimate_file_size(input_string, max_length, specified_lengths=None):
    if specified_lengths:
        total_combinations = sum(len(list(combinations(input_string, i))) for i in specified_lengths)
        average_length = sum(i * len(list(combinations(input_string, i))) for i in specified_lengths) / total_combinations
    else:
        total_combinations = sum(len(list(combinations(input_string, i))) for i in range(1, max_length + 1))
        average_length = sum(i * len(list(combinations(input_string, i))) for i in range(1, max_length + 1)) / total_combinations
    
    estimated_size_bytes = int((average_length + 1) * total_combinations)  # +1 for the newline character
    estimated_size_mb = estimated_size_bytes / (1024 * 1024)  # Convert bytes to MB
    return total_combinations, estimated_size_bytes, estimated_size_mb

def write_chunk(file_path, chunk):
    with open(file_path, 'a') as file:
        file.writelines(chunk)
        file.flush()  # Flush the file buffer to ensure real-time write

def write_combinations_to_file(input_string, max_length, file_path, update_interval=1000, chunk_size=10000, num_threads=1, specified_lengths=None):
    total_combinations, estimated_size_bytes, estimated_size_mb = estimate_file_size(input_string, max_length, specified_lengths)

    print(f"Total Combinations: {total_combinations}")
    print(f"Estimated total file size: {estimated_size_bytes} bytes ({estimated_size_mb:.2f} MiB)")

    red_color = "\033[91m"
    reset_color = "\033[0m"
    OKCYAN = '\033[96m'
    OKYELLOW = '\033[93m'
    BOLD = "\033[1m"
    OKGREEN = '\033[92m'
    HEADER = '\033[95m'
    start_time = time.time()

    # Clear the file if it already exists
    open(file_path, 'w').close()

    chunk = []
    idx_start = 0
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = []
        for comb in generate_combinations(input_string, max_length, specified_lengths):
            chunk.append(f"{comb}\n")
            if len(chunk) >= chunk_size:
                futures.append(executor.submit(write_chunk, file_path, chunk.copy()))
                idx_start += len(chunk)
                chunk.clear()
                if idx_start % update_interval == 0 or idx_start == total_combinations:
                    # Calculate progress
                    percentage_complete = (idx_start / total_combinations) * 100
                    remaining_combinations = total_combinations - idx_start
                    elapsed_time = time.time() - start_time
                    estimated_total_time = (elapsed_time / idx_start) * total_combinations
                    estimated_remaining_time = (estimated_total_time - elapsed_time) / 60  # Convert to minutes
                    write_speed = idx_start / elapsed_time if elapsed_time > 0 else 0  # Combinations per second
                    # Print verbose output
                    print(f"{red_color}Progress: {percentage_complete:.5f}% | Remaining combinations: {remaining_combinations} | Estimated remaining time: {estimated_remaining_time:.5f} minutes | Write speed: {int(write_speed)} combinations/second {reset_color}", end='\r')

        if chunk:
            futures.append(executor.submit(write_chunk, file_path, chunk))

        # Wait for all threads to finish
        for future in as_completed(futures):
            future.result()

    end_time = time.time()
    print()
    print(f"{OKGREEN}Done!{reset_color}",end="\r")
    try:
        print(f"Write Speed: {OKGREEN}{int(write_speed)}{reset_color} combinations/second",end="\r")
    except:
        print(f"{OKYELLOW}Could not find write speed. Maybe --update_interval was too big.{reset_color}")
    total_execution_time = end_time - start_time

    # Convert total execution time to hours, minutes, and seconds
    hours, rem = divmod(total_execution_time, 3600)
    minutes, seconds = divmod(rem, 60)

    print()  # To ensure the next print statement starts on a new line
    actual_size_bytes = os.path.getsize(file_path)
    actual_size_mb = actual_size_bytes / (1024 * 1024)  # Convert bytes to MiB
    print(f"Combinations written to {HEADER}{BOLD}{file_path}{reset_color}")
    print(f"Actual file size: {actual_size_bytes} B | {HEADER}{BOLD}{actual_size_mb:.2f} MiB{reset_color}")
    print(f"Total execution time: {OKCYAN}{int(hours):02}H {int(minutes):02}M {seconds:.2f}S{reset_color}")

def main():
    parser = argparse.ArgumentParser(description="Generate all combinations of a given string and write them to a file.")
    parser.add_argument("input_string", type=str, help="The input string to generate combinations from.")
    parser.add_argument("-m", "--max_length", type=int, help="The maximum length of combinations.")
    parser.add_argument("-l","--lengths", type=int, nargs='+', help="Specific lengths of combinations to generate.")
    parser.add_argument("-o", "--outputfile", type=str, default="combinations.txt", help="The output file to write combinations to.")
    parser.add_argument("-u","--update_interval", type=int, default=1000, help="Interval of progress updates.")
    parser.add_argument("-c","--chunk_size", type=int, default=10000, help="Number of combinations to write at once.")
    parser.add_argument("-t","--num_threads", type=int, default=1, help="Number of threads to use for combination generation and file writing.")

    args = parser.parse_args()

    if not args.max_length and not args.lengths:
        parser.error('Either --max_length or --lengths must be specified.')

    max_length = args.max_length if args.max_length else max(args.lengths)
    specified_lengths = args.lengths if args.lengths else None

    write_combinations_to_file(args.input_string, max_length, args.outputfile, args.update_interval, args.chunk_size, args.num_threads, specified_lengths)

if __name__ == "__main__":
    main()
