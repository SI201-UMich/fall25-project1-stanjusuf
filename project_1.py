# Name: Stanford Jusuf
# Student ID: 08874096
# Email: sjusuf@umich.edu

import csv

def load_penguin_data(csv_filepath):
    penguin_data = {}

    with open(csv_filepath, 'r', newline='') as csvfile:
        csv_reader = csv.reader(csvfile)
        headers = next(csv_reader)
        for row in csv_reader:
            key = row[0]
            values = {headers[i]: row[i] for i in range(1, len(row))}
            penguin_data[key] = values

    return penguin_data

def group_weight_by_year_island_species_sex(penguin_data):
    grouped_penguin_data = {}

    for _, record in penguin_data.items():
        year = record.get("year")
        island = record.get("island")
        species = record.get("species")
        sex = record.get("sex")
        weight = record.get("body_mass_g")
        if not weight or not weight.isdigit():
            continue
        weight = int(weight)
        if year not in grouped_penguin_data:
            grouped_penguin_data[year] = {}
        if island not in grouped_penguin_data[year]:
            grouped_penguin_data[year][island] = {}
        if species not in grouped_penguin_data[year][island]:
            grouped_penguin_data[year][island][species] = {}
        if sex not in grouped_penguin_data[year][island][species]:
            grouped_penguin_data[year][island][species][sex] = []
        grouped_penguin_data[year][island][species][sex].append(weight)

    return grouped_penguin_data

def mean_weight_by_sex(grouped_penguin_data):
    pass

def median_weight_by_sex(grouped_penguin_data):
    pass

def mode_meight_by_sex(grouped_penguin_data):
    pass

def distribution_shapes(means, medians, modes):
    pass

def generate_report(distribution_shapes):
    pass

def main():
    penguin_data = load_penguin_data('penguins.csv')
    print(penguin_data)


if __name__ == "__main__":
    main()