import argparse
import json

# Define the argument parser
parser = argparse.ArgumentParser(description="Convert a text file to a JSON file with the specified format")
parser.add_argument("input_file_path", help="Path to the input text file")
parser.add_argument("output_file_path", help="Path to the output JSON file")
args = parser.parse_args()

# Initialize an empty list to store the guidelines
guidelines = []

# Read the input file and split it into sections based on "###"
with open(args.input_file_path, "r") as file:
    sections = file.read().split("###")

# Iterate through sections, skipping the first empty section
for section in sections[1:]:
    text = section.lstrip()
    # Create a dictionary for each guideline
    guideline = {"content": f'{text}'}
    guidelines.append(guideline)

# Create a dictionary with the guidelines list
data = {"guidelines": guidelines}

# Write the data as JSON to the output file
with open(args.output_file_path, "w") as json_file:
    json.dump(data, json_file, indent=4)

print(f"Conversion complete. JSON file saved to {args.output_file_path}")
