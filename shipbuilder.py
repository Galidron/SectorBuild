import json

total_tonnage = 0
total_cost = 0
hull_cost = 0
hull_points = 0
hull_options = {}
hull_configurations = [
    'Standard            - Partially streamlined',
    'Streamlined         - Cost + 20%',
    'Sphere              - Partially streamlined, Cost - 20%',
    'Close Structure     - Partially streamlined, Hull Points + 10%, Cost - 10%',
    'Dispersed Structure - Hull Points - 10%, Cost - 50%',
    'Planetoid           - Hull Points + 25%, Cost + 4000 * (Tonnage / 0.8)',
    'Buffered Planetoid  - Hull Points + 50%, Cost + 4000 * (Tonnage / 0.65)',
]
hull_configuration = ''


def print_list(list):
    for index, item in enumerate(list):
        print("{0}: {1}".format(index, item))

def get_tonnage():
    tonnage = 0
    while tonnage < 1:
        try:
            tonnage = int(input('How many tons will this ships interior be? '))
        except ValueError:
            print("Tonnage requires a positve number.")
        if tonnage < 1:
            print("Tonnage must be greater than 0")
    return tonnage

def get_hull_config():
    while True:
        print_list(hull_configurations)

        HERE
        try:
            type = int(input('Enter the number of the hull configuration you will use: '))
        except ValueError:
            print("Please select a number from the list.")
        else:
            return type
