# Name: Stanford Jusuf
# Student ID: 08874096
# Email: sjusuf@umich.edu

import csv

def load_penguin_data(csv_filepath):
    penguin_data = []
    with open(csv_filepath, 'r', newline='') as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            penguin_data.append(row)
    return penguin_data

def characterize_penguin_data(penguin_data):
    print(f"Variables: {penguin_data[0]}")
    print(f"Sample entry: {penguin_data[3]}")
    print(f"Number of rows: {len(penguin_data) - 1}")
    return 

def main():
    penguin_data = load_penguin_data('penguins.csv')
    characterize_penguin_data(penguin_data)


if __name__ == "__main__":
    main()