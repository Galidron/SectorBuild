#!/Library/Frameworks/Python.framework/Versions/3.5/bin/python3

import hex

subsector = hex.Hex(False, "Star 1")
print("Test ")
print(subsector.name + " 0101 " + subsector.code())

class SubSector:
    def __init__(self,sub_sec_num = "0"):
        star_count = 0
        for column in range(1, 9):
            for row in range(10):
                if hex.d6() < 4:
                    self.space = { : hex.Hex(False,"Star ")}