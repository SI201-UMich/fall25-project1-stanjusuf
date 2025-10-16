# Name: Stanford Jusuf
# Student ID: 08874096
# Email: sjusuf@umich.edu
# Course: SI 201, Fall 2025
# Project: 1
# Project Members: None
# Gen AI Usage: Utilized Gen AI to explain concepts for temporary files and .flush() method for unit tests development.


import csv
import unittest
import tempfile


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
        if not sex or sex.strip().upper() == "NA":
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
    means = {}
    for year, islands in grouped_penguin_data.items():
        for island, species in islands.items():
            for species_name, sexes in species.items():
                for sex, weights in sexes.items():
                    if weights:
                        mean_weight = sum(weights) / len(weights)
                        means[(year, island, species_name, sex)] = mean_weight
    return means


def median_weight_by_sex(grouped_penguin_data):
    medians = {}
    for year, islands in grouped_penguin_data.items():
        for island, species in islands.items():
            for species_name, sexes in species.items():
                for sex, weights in sexes.items():
                    if weights:
                        sorted_weights = sorted(weights)
                        n = len(sorted_weights)
                        mid = n // 2
                        if n % 2 == 0:
                            median_weight = (sorted_weights[mid - 1] + sorted_weights[mid]) / 2
                        else:
                            median_weight = sorted_weights[mid]
                        medians[(year, island, species_name, sex)] = median_weight
    return medians


def mode_weight_by_sex(grouped_penguin_data):
    modes = {}
    for year, islands in grouped_penguin_data.items():
        for island, species in islands.items():
            for species_name, sexes in species.items():
                for sex, weights in sexes.items():
                    if weights:
                        weight_counts = {}
                        for weight in weights:
                            weight_counts[weight] = weight_counts.get(weight, 0) + 1
                        mode_weight = max(weight_counts, key=weight_counts.get)
                        modes[(year, island, species_name, sex)] = mode_weight
    return modes


def distribution_shapes(means, medians, modes):
    distribution_shapes = {}
    for key in means.keys():
        mean = means.get(key)
        median = medians.get(key)
        mode = modes.get(key)
        if mean is None or median is None or mode is None:
            continue
        if mean > median > mode:
            shape = "right-skewed"
        elif mean < median < mode:
            shape = "left-skewed"
        elif mean == median == mode:
            shape = "normal"
        else:
            continue
        distribution_shapes[key] = shape
    return distribution_shapes


class TestLoadPenguinData(unittest.TestCase):
    def test_load_general_case(self):
        with tempfile.NamedTemporaryFile(mode="w+", delete=False) as f:
            f.write("id,year,island,species,sex,body_mass_g\n1,2007,Torgersen,Adelie,Male,3750\n")
            f.flush()
            data = load_penguin_data(f.name)
        self.assertEqual(data["1"]["species"], "Adelie")

    def test_load_multiple_rows(self):
        with tempfile.NamedTemporaryFile(mode="w+", delete=False) as f:
            f.write("id,year,island,species,sex,body_mass_g\n1,2007,Torgersen,Adelie,Male,3750\n2,2008,Dream,Gentoo,Female,5000\n")
            f.flush()
            data = load_penguin_data(f.name)
        self.assertEqual(data["2"]["island"], "Dream")

    def test_load_empty_file(self):
        with tempfile.NamedTemporaryFile(mode="w+", delete=False) as f:
            f.write("id,year,island,species,sex,body_mass_g\n")
            f.flush()
            data = load_penguin_data(f.name)
        self.assertEqual(data, {})

    def test_load_missing_values(self):
        with tempfile.NamedTemporaryFile(mode="w+", delete=False) as f:
            f.write("id,year,island,species,sex,body_mass_g\n1,2007,Torgersen,Adelie,,\n")
            f.flush()
            data = load_penguin_data(f.name)
        self.assertEqual(data["1"]["sex"], "")
        self.assertEqual(data["1"]["body_mass_g"], "")


class TestGroupWeight(unittest.TestCase):
    def test_group_general_case(self):
        penguin_data = {"1": {"year": "2007","island": "Torgersen","species": "Adelie","sex": "Male","body_mass_g": "3750"}}
        grouped = group_weight_by_year_island_species_sex(penguin_data)
        self.assertEqual(grouped["2007"]["Torgersen"]["Adelie"]["Male"], [3750])

    def test_group_multiple_species(self):
        penguin_data = {
            "1": {"year": "2008","island": "Dream","species": "Gentoo","sex": "Female","body_mass_g": "5000"},
            "2": {"year": "2008","island": "Dream","species": "Chinstrap","sex": "Male","body_mass_g": "3600"}
        }
        grouped = group_weight_by_year_island_species_sex(penguin_data)
        self.assertIn("Gentoo", grouped["2008"]["Dream"])
        self.assertIn("Chinstrap", grouped["2008"]["Dream"])

    def test_group_skip_invalid_weight(self):
        penguin_data = {"1": {"year": "2007","island": "Torgersen","species": "Adelie","sex": "Male","body_mass_g": ""}}
        grouped = group_weight_by_year_island_species_sex(penguin_data)
        self.assertEqual(grouped, {})

    def test_group_skip_na_sex(self):
        penguin_data = {"1": {"year": "2007","island": "Torgersen","species": "Adelie","sex": "NA","body_mass_g": "3750"}}
        grouped = group_weight_by_year_island_species_sex(penguin_data)
        self.assertEqual(grouped, {})


class TestMeanWeight(unittest.TestCase):
    def test_mean_general_case(self):
        grouped = {"2007":{"Torgersen":{"Adelie":{"Male":[3750,3800]}}}}
        means = mean_weight_by_sex(grouped)
        self.assertEqual(means[("2007","Torgersen","Adelie","Male")], 3775)

    def test_mean_multiple_groups(self):
        grouped = {"2008":{"Dream":{"Gentoo":{"Female":[5000,5200]}}}}
        means = mean_weight_by_sex(grouped)
        self.assertEqual(means[("2008","Dream","Gentoo","Female")], 5100)

    def test_mean_empty_group(self):
        grouped = {"2007":{"Torgersen":{"Adelie":{"Male":[]}}}}
        means = mean_weight_by_sex(grouped)
        self.assertEqual(means, {})

    def test_mean_no_data(self):
        grouped = {}
        means = mean_weight_by_sex(grouped)
        self.assertEqual(means, {})


class TestMedianWeight(unittest.TestCase):
    def test_median_general_case_odd(self):
        grouped = {"2007":{"Torgersen":{"Adelie":{"Male":[3700,3750,3800]}}}}
        medians = median_weight_by_sex(grouped)
        self.assertEqual(medians[("2007","Torgersen","Adelie","Male")], 3750)

    def test_median_general_case_even(self):
        grouped = {"2007":{"Torgersen":{"Adelie":{"Female":[3400,3500]}}}}
        medians = median_weight_by_sex(grouped)
        self.assertEqual(medians[("2007","Torgersen","Adelie","Female")], 3450)

    def test_median_empty_group(self):
        grouped = {"2007":{"Torgersen":{"Adelie":{"Male":[]}}}}
        medians = median_weight_by_sex(grouped)
        self.assertEqual(medians, {})

    def test_median_no_data(self):
        grouped = {}
        medians = median_weight_by_sex(grouped)
        self.assertEqual(medians, {})


class TestModeWeight(unittest.TestCase):
    def test_mode_general_case(self):
        grouped = {"2007":{"Torgersen":{"Adelie":{"Male":[3750,3750,3800]}}}}
        modes = mode_weight_by_sex(grouped)
        self.assertEqual(modes[("2007","Torgersen","Adelie","Male")], 3750)

    def test_mode_multiple_groups(self):
        grouped = {"2008":{"Dream":{"Gentoo":{"Female":[5000,5200,5000]}}}}
        modes = mode_weight_by_sex(grouped)
        self.assertEqual(modes[("2008","Dream","Gentoo","Female")], 5000)

    def test_mode_empty_group(self):
        grouped = {"2007":{"Torgersen":{"Adelie":{"Male":[]}}}}
        modes = mode_weight_by_sex(grouped)
        self.assertEqual(modes, {})

    def test_mode_no_data(self):
        grouped = {}
        modes = mode_weight_by_sex(grouped)
        self.assertEqual(modes, {})


class TestDistributionShapes(unittest.TestCase):
    def test_distribution_right_skewed(self):
        means = {("2007","Torgersen","Adelie","Male"):3800}
        medians = {("2007","Torgersen","Adelie","Male"):3700}
        modes = {("2007","Torgersen","Adelie","Male"):3600}
        shapes = distribution_shapes(means, medians, modes)
        self.assertEqual(shapes[("2007","Torgersen","Adelie","Male")], "right-skewed")

    def test_distribution_left_skewed(self):
        means = {("2007","Torgersen","Adelie","Female"):3400}
        medians = {("2007","Torgersen","Adelie","Female"):3500}
        modes = {("2007","Torgersen","Adelie","Female"):3600}
        shapes = distribution_shapes(means, medians, modes)
        self.assertEqual(shapes[("2007","Torgersen","Adelie","Female")], "left-skewed")

    def test_distribution_normal(self):
        means = {("2008","Dream","Gentoo","Male"):5000}
        medians = {("2008","Dream","Gentoo","Male"):5000}
        modes = {("2008","Dream","Gentoo","Male"):5000}
        shapes = distribution_shapes(means, medians, modes)
        self.assertEqual(shapes[("2008","Dream","Gentoo","Male")], "normal")

    def test_distribution_skip_incomplete(self):
        means = {("2009","Biscoe","Chinstrap","Female"):4000}
        medians = {}
        modes = {}
        shapes = distribution_shapes(means, medians, modes)
        self.assertEqual(shapes, {})


if __name__ == "__main__":
    unittest.main()