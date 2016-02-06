#!/Library/Frameworks/Python.framework/Versions/3.5/bin/python3

import hex

class SubSector:
    def __init__(self, sub_sec_num="0"):
        star_count = 0
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
                    self.subsector[space_num] = hex.Hex(False, "Star " + str(star_count))
                    star_count += 1
                else:
                    self.subsector[space_num] = hex.Hex()

    def __str__(self):
        string = ""
        for space, world in sorted(self.subsector.items()):
            string += space
            string += " "
            string += world.name
            string += " "
            string += str(world)
            string += "\n"
        return string

x = SubSector()
print(x)