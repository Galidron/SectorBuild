#!/Library/Frameworks/Python.framework/Versions/3.5/bin/python3

import hex
import random
import json

with open('starnames.json', "r") as f:
    star_names = json.load(f)



class SubSector:
    def __init__(self, sub_sec_num="0"):
        self.subsector = {}
        for column in range(1, 9):
            for row in range(1, 11):
                space_num = str(sub_sec_num) + str(column)
                if row < 10:
                    space_num += "0"
                    space_num += str(row)
                else:
                    space_num += str(row)

                if hex.d6() > 3:
                    if len(star_names) > 0:
                        name = random.choice(star_names)
                        star_names.remove(name)
                    self.subsector[space_num] = hex.Hex(False, name)
                else:
                    self.subsector[space_num] = hex.Hex()

    def __str__(self):
        string = ""
        for space, world in sorted(self.subsector.items()):
            string += "{0} {1} {2}\n".format(space, world.name, world)

        return string

    def write_systems(self, file_name="system_file.txt"):
        with open(file_name, "w") as file:
            for space, world in sorted(self.subsector.items()):
                if not world.is_empty:
                    file.write("{1:20} {0} {2}\n".format(space, world.name, world))

x = SubSector()
print(x)
x.write_systems()