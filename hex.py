#!/Library/Frameworks/Python.framework/Versions/3.5/bin/python3

import random
import json


def d6():
    """Simulate the roll of a 6 sided die"""
    random.seed()
    return random.randint(1, 6)


def d3():
    """Simulate the roll of a 3 sided die"""
    random.seed()
    return random.randint(1, 3)

with open('atmospheres.json', 'r') as f:
    atmospheres = json.load(f)

with open('temperatures.json', "r") as f:
    temperatures = json.load(f)

with open('governments.json', "r") as f:
    governments = json.load(f)

with open('factionstrength.json', "r") as f:
    fac_strength = json.load(f)

with open('cultures.json', "r") as f:
    cultures = json.load(f)

with open('starportclass.json', "r") as f:
    starport_classes = json.load(f)

with open('starporttype.json', "r") as f:
    starport_types = json.load(f)


class Hex:
    """Hex Class to contain all the data for each hex of the subsector."""
    def __init__(self, name="", empty=True):
        self.is_empty       = empty
        self.name           = name
        self.size           = None
        self.atmos_type     = None
        self.atmos_num      = None
        self.gravity        = None
        self.temperature    = None
        self.temp_num       = None
        self.hydro          = None
        self.pop            = None
        self.gov_num        = None
        self.gov_type       = None
        self.factions       = []
        self.culture_num    = None
        self.culture_type   = None
        self.law            = None
        self.starport_class = None
        self.starport_type  = None
        self.tech           = None
        if not self.is_empty:
            self.gen_size()
            self.gen_atmos()
            self.gen_temp()
            self.gen_hydro()
            self.gen_pop()
            self.gen_factions()
            self.gen_culture()
            self.gen_law()
            self.gen_starport()
            self.gen_tech()

    def gen_size(self):
        """Calculate the primary world's size"""
        self.size = d6() + d6() - 2
        self.set_grav()

    def set_grav(self):
        """Set the gravity string for the primary world based on size"""
        assert (0 >= self.size <= 10), "Size not set"
        if self.size <= 6:
            self.gravity = "low"
        elif self.size >= 10:
            self.gravity = "high"
        else:
            self.gravity = "normal"

    def gen_atmos(self):
        """Calculate the primary world's atmosphere based on size"""
        assert (0 >= self.size <= 10), "Size not set"
        self.atmos_num = d6() + d6() - 7 + self.size
        self.set_atmos_type()

    def set_atmos_type(self):
        """Set the atmosphere type string based on the atmosphere"""
        assert (0 >= self.atmos_num <= 15), "Atmosphere not set"
        self.atmos_type = atmospheres[self.atmos_num]

    def gen_temp(self):
        """Calculate the primary world's temperature"""
        self.temp_num = d6() + d6()
        self.set_temp_name()

    def set_temp_name(self):
        """Set the temperature name string based on the temperature"""
        assert (-2 >= self.temp_num <= 16), "Temperature not set"
        self.temperature = temperatures[self.temp_num]

    def gen_hydro(self):
        """Calculate the amount of water on the primary world based on size atmosphere and temperature"""
        assert (0 >= self.size <= 10), "Size not set"
        assert (0 >= self.atmos_num <= 15), "Atmosphere not set"
        assert (-2 >= self.temp_num <= 16), "Temperature not set"
        if self.size > 2:
            self.hydro = 0
        elif self.atmos_num in [0, 1, 10, 11, 12]:
            self.hydro = d6() + d6() - 4
        elif self.atmos_num not in [13, 15]:
            if self.temperature == "Hot":
                self.hydro = d6() + d6() - 9
            elif self.temperature == "Boiling":
                self.hydro = d6() + d6() - 13
            else:
                self.hydro = d6() + d6() - 7
        else:
            self.hydro = d6() + d6() - 7
        if self.hydro < 0:
            self.hydro = 0

    def gen_pop(self):
        """Calculate the primary world's population"""
        self.pop = d6() + d6() - 2

    def gen_gov(self):
        """Calculate the primary world's government type based on population"""
        assert (0 >= self.pop <= 15), "Population not set"
        self.gov_num = d6() + d6() - 7 + self.pop
        if self.gov_num < 0:
            self.gov_num = 0
        self.set_gov_name()

    def set_gov_name(self):
        """Set the government name string based on government"""
        assert (0 >= self.gov_num <= 15), "Government not set"
        self.gov_type = governments[self.gov_num]

    def gen_factions(self):
        """Generate the primary world's number of factions and type of factions using government"""
        assert (0 >= self.gov_num <= 15), "Government not set"
        fac_count = d3()
        if self.gov_num in [0, 7]:
            fac_count += 1
        if self.gov_num >= 10:
            fac_count -= 1
        if fac_count > 0:
            for i in range(1, fac_count + 1):
                gov = d6() + d6() - 7 + self.pop
                if gov < 0:
                    gov = 0
                strength = d6() + d6()
                self.factions.append([gov, strength, governments[gov], fac_strength[strength]])

    def gen_culture(self):
        """Generate the primary world's culture"""
        self.culture_num = d6() * 10 + d6()
        self.set_culture_type()

    def set_culture_type(self):
        """Set the cultyre type string based on culture"""
        assert (11 >= self.culture_num <= 66), "Culture not set"
        self.culture_type = cultures[self.culture_num]

    def gen_law(self):
        """Calculate the primary world's law level based on government"""
        assert (0 >= self.gov_num <= 15), "Government not set"
        self.law = d6() + d6() - 7 + self.gov_num
        if self.law < 0:
            self.law = 0
        if self.law > 9:
            self.law = 9

    def gen_starport(self):
        """Calculate the primary world's starport based on population"""
        assert (0 >= self.pop <= 15), "Population not set"
        starport_num = d6() + d6()
        if self.pop >= 10:
            starport_num += 2
        elif self.pop >= 8:
            starport_num += 1
        elif self.pop <= 2:
            starport_num -= 2
        elif self.pop <= 4:
            starport_num -=1
        if self.starport_num < 2 :
            starport_num = 2
        elif self.starport_num > 11:
            starport_num = 11
        self.starport_class = starport_classes[starport_num]
        self.set_set_starprot_type()

    def set_starprot_type(self):
        """Set starport type string based on starport class"""
        assert  (self.starport_class in ["X", "A", "B", "C", "D", "E"]), "Starport class not set"
        self.starport_type = starport_type[self.starport_num]

    def gen_tech(self):


