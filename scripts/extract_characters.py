import argparse
import csv
import sys
import polars as pl
from polars import DataFrame
from datetime import datetime, timedelta
from collections import defaultdict
import os


def parse_args():
    parser = argparse.ArgumentParser(description="Character to be extracted")
    # Add arguments
    parser.add_argument('-i', '--input', required=True, help='Input CSV file containing script data')
    parser.add_argument('-c', '--character', required=True, help='Character to be extracted')
    parser.add_argument('-o', '--output', required=True, help='Output CSV file')
    parser.add_argument('-r', '--randomize', action='store_true', help='Randomize lines for open coding')
    parser.add_argument('-n', '--number', help='Number of random lines collected')


    return parser.parse_args()


def load_character(input_file, character):
    df = pl.read_csv(input_file, has_header=True)
    df_filter = df.filter(pl.col("Name") == character) 
    return df_filter

def randomize_lines(lines, num=125):
    if num is None:
        num = 125

    randomized_lines = lines.sample(num, shuffle=True, seed=42)
    return randomized_lines


def write_results(counts: DataFrame, output_file=None):

    if output_file:
        counts.write_csv(output_file)
    else:
        counts.write_csv(sys.stdout)


def main():
    args = parse_args()

    curr_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(curr_dir, "..", "data", args.input)
    output_path = os.path.join(curr_dir, "..", "data", args.output)
    lines = load_character(input_path, args.character)
    if args.randomize:
        lines = randomize_lines(lines, args.number)
        
    write_results(lines, output_path)


if __name__ == "__main__":
    main()
    