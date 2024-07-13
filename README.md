# CombiGen-Efficient-Combination-Generator
The CombiGen is a Python script designed to generate all possible combinations of characters from a given input string up to a specified maximum length. It efficiently writes these combinations to a file while providing real-time progress updates.
# Combination Generator

This Python script generates all possible combinations of characters from a given input string up to a specified maximum length and writes them to a file. The script is optimized for performance and memory efficiency, and it uses multithreading for improved I/O operations.

## Features

- **Combination Generation**: Generates all possible combinations of characters from an input string.
- **Maximum Length**: Supports specifying the maximum length of combinations.
- **Real-time Progress Updates**: Provides live updates on progress including percentage completion, remaining combinations, and estimated time.
- **Multithreading**: Utilizes multithreading to enhance performance by parallelizing combination generation and file writing.
- **Command-Line Interface (CLI)**: Offers flexible command-line options for specifying input, output file, update interval, and chunk size.

## Python Version

This tool requires Python 3.6 or higher.

## Installation

**Clone the Repository:**

   ```bash
   git clone https://github.com/your/repository.git
   cd repository

## Usage

**Command-Line Interface (CLI)**

Run the script with Python, providing required arguments:
```bash
python CombiGen.py <input_string> <max_length> -o <outputfile> --update_interval <update_interval> --chunk_size <chunk_size>
```
**Arguments:**
<input_string>: The input string to generate combinations from.
<max_length>: The maximum length of combinations.
-o, --outputfile: The output file to write combinations to.
--update_interval: Interval (in combinations) of progress updates.
--chunk_size: Number of combinations to write to file at once.

**Example**
Generate combinations for the alphabet and numbers up to 8 characters long:
```bash
python combination_generator.py "abcdefghijklmnopqrstuvwxyz1234567890" 8 -o output.txt --update_interval 1000 --chunk_size 10000
```
**Output**
Upon execution, the tool will provide real-time progress updates and write the combinations to the specified output file (`output.txt` in this example).

**License**
This project is licensed under the MIT License - see the LICENSE file for details.
