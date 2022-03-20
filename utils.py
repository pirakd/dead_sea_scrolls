import yaml
from os import path
from collections import defaultdict

def readYaml(fileName):
    with open(fileName) as y:
        y = yaml.load(y, Loader=yaml.FullLoader)
    return y

def filter_data_by_field(field, values, unfiltered_data):
    filtered_data = defaultdict(list)
    for entry in unfiltered_data:
        if entry[field] in values:
            filtered_data[entry[field]].append(entry)

    return filtered_data



root_path = path.dirname(__file__)
