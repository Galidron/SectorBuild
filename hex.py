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
    def __init__(self, empty=True, name=""):
        self.is_empty = empty
        self.name = name
        self.size = None
        self.atmos_type = None
        self.atmos_num = None
        self.gravity = None
        self.temperature = None
        self.temp_num = None
        self.hydro = None
        self.pop = None
        self.gov_num = None
        self.gov_type = None
        self.factions = []
        self.culture_num = None
        self.culture_type = None
        self.law = None
        self.starport_class = None
        self.starport_type = None
        self.tech = None
        self.bases = []
        self.travel_code = None
        self.trade_codes = []
        self.gas_giant = False
        if not self.is_empty:
            self.gen_size()
            self.gen_atmos()
            self.gen_temp()
            self.gen_hydro()
            self.gen_pop()
            self.gen_gov()
            self.gen_factions()
            self.gen_culture()
            self.gen_law()
            self.gen_starport()
            self.gen_tech()
            self.gen_bases()
            self.set_travel_code()
            self.set_trade_codes()
            self.gen_gas_giant()

    def gen_size(self):
        """Calculate the primary world's size"""
        self.size = d6() + d6() - 2
        self.set_grav()

    def set_grav(self):
        """Set the gravity string for the primary world based on size"""
        assert (self.size in range(11)), "Size not set"
        if self.size <= 6:
            self.gravity = "low"
        elif self.size >= 10:
            self.gravity = "high"
        else:
            self.gravity = "normal"

    def gen_atmos(self):
        """Calculate the primary world's atmosphere based on size"""
        assert (self.size in range(11)), "Size not set"
        self.atmos_num = d6() + d6() - 7 + self.size
        if self.atmos_num < 0:
            self.atmos_num = 0
        self.set_atmos_type()

    def set_atmos_type(self):
        """Set the atmosphere type string based on the atmosphere"""
        assert (self.atmos_num in range(16)), "Atmosphere not set" + str(self.atmos_num)
        self.atmos_type = atmospheres[str(self.atmos_num)]

    def gen_temp(self):
        """Calculate the primary world's temperature"""
        self.temp_num = d6() + d6()
        self.set_temp_name()

    def set_temp_name(self):
        """Set the temperature name string based on the temperature"""
        assert (self.temp_num in range(-2, 17)), "Temperature not set"
        self.temperature = temperatures[str(self.temp_num)]

    def gen_hydro(self):
        """Calculate the amount of water on the primary world based on size atmosphere and temperature"""
        assert (self.size in range(11)), "Size not set"
        assert (self.atmos_num in range(16)), "Atmosphere not set"
        assert (self.temp_num in range(-2, 17)), "Temperature not set"
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
        assert (self.pop in range(16)), "Population not set"
        self.gov_num = d6() + d6() - 7 + self.pop
        if self.gov_num < 0:
            self.gov_num = 0
        self.set_gov_name()

    def set_gov_name(self):
        """Set the government name string based on government"""
        assert (self.gov_num in range(16)), "Government not set"
        self.gov_type = governments[str(self.gov_num)]

    def gen_factions(self):
        """Generate the primary world's number of factions and type of factions using government"""
        assert (self.gov_num in range(16)), "Government not set"
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
                self.factions.append([gov, strength, governments[str(gov)], fac_strength[str(strength)]])

    def gen_culture(self):
        """Generate the primary world's culture"""
        self.culture_num = d6() * 10 + d6()
        self.set_culture_type()

    def set_culture_type(self):
        """Set the cultyre type string based on culture"""
        assert (self.culture_num in range(11, 67)), "Culture not set"
        self.culture_type = cultures[str(self.culture_num)]

    def gen_law(self):
        """Calculate the primary world's law level based on government"""
        assert (self.gov_num in range(16)), "Government not set"
        self.law = d6() + d6() - 7 + self.gov_num
        if self.law < 0:
            self.law = 0
        if self.law > 9:
            self.law = 9

    def gen_starport(self):
        """Calculate the primary world's starport based on population"""
        assert (self.pop in range(16)), "Population not set"
        starport_num = d6() + d6()
        if self.pop >= 10:
            starport_num += 2
        elif self.pop >= 8:
            starport_num += 1
        elif self.pop <= 2:
            starport_num -= 2
        elif self.pop <= 4:
            starport_num -= 1
        if starport_num < 2:
            starport_num = 2
        elif starport_num > 11:
            starport_num = 11
        self.starport_class = starport_classes[str(starport_num)]
        self.set_starprot_type()

    def set_starprot_type(self):
        """Set starport type string based on starport class"""
        assert (self.starport_class in ["X", "A", "B", "C", "D", "E"]), "Starport class not set"
        self.starport_type = starport_types[str(self.starport_class)]

    def gen_tech(self):
        """Calculate the primary world's tech level"""
        assert (self.starport_class in ["X", "A", "B", "C", "D", "E"]), "Starport class not set"
        assert (self.size in range(11)), "Size not set"
        assert (self.atmos_num in range(16)), "Atmosphere not set"
        assert (self.hydro in range(16)), "Hydrographics not set"
        assert (self.pop in range(16)), "Population not set"
        assert (self.gov_num in range(16)), "Government not set"
        self.tech = d6()

        if self.starport_class == "X":
            self.tech -= 4
        elif self.starport_class == "A":
            self.tech += 6
        elif self.starport_class == "B":
            self.tech += 4
        elif self.starport_class == "C":
            self.tech += 2

        if self.size < 2:
            self.tech += 2
        elif self.size < 5:
            self.tech += 1

        if self.atmos_num in [0, 1, 2, 3, 10, 11, 12, 13, 14, 15]:
            self.tech += 1

        if self.hydro in [0, 9]:
            self.tech += 1
        elif self.hydro == 10:
            self.tech += 2

        if self.pop in [1, 2, 3, 4, 5, 8]:
            self.tech += 1
        elif self.pop == 9:
            self.tech += 2
        elif self.pop == 10:
            self.tech += 4

        if self.gov_num in [0, 5]:
            self.tech += 1
        elif self.gov_num == 7:
            self.tech += 2
        elif self.gov_num in [13, 14]:
            self.tech -= 2

    def gen_bases(self):
        """Calculate the primary world's bases"""
        assert (self.starport_class in ["X", "A", "B", "C", "D", "E"]), "Starport class not set"
        if self.starport_class == "A":
            if d6() > 8:
                self.bases.append("N")
            if d6() > 10:
                self.bases.append("S")
            if d6() > 8:
                self.bases.append("R")
            self.bases.append("T")
        elif self.starport_class == "B":
            if d6() > 8:
                self.bases.append("N")
            if d6() > 8:
                self.bases.append("S")
            if d6() > 10:
                self.bases.append("R")
            self.bases.append("T")
        elif self.starport_class == "C":
            if d6() > 8:
                self.bases.append("S")
            if d6() > 10:
                self.bases.append("R")
            if d6() > 10:
                self.bases.append("T")
        elif self.starport_class == "D":
            if d6() > 7:
                self.bases.append("S")

    def set_travel_code(self):
        """Set the travel code based on atmosphere, government, and law."""
        assert (self.atmos_num in range(16)), "Atmosphere not set"
        assert (self.gov_num in range(16)), "Government not set"
        assert (self.law in range(10)), "Law not set"
        if self.atmos_num > 10:
            self.travel_code = "A"
        elif self.gov_num in [0, 7, 10]:
            self.travel_code = "A"
        elif self.law in [0, 9]:
            self.travel_code = "A"

    def set_trade_codes(self):
        """Set the trade codes based on size, atmosphere, hydrographics, population, government, law, and tech."""
        assert (self.size in range(11)), "Size not set"
        assert (self.atmos_num in range(16)), "Atmosphere not set"
        assert (self.hydro in range(16)), "Hydrographics not set"
        assert (self.pop in range(16)), "Population not set"
        assert (self.gov_num in range(16)), "Government not set"
        assert (self.law in range(10)), "Law not set"
        assert (self.tech in range(21)), "Tech not set " + str(self.tech)
        if self.atmos_num in range(4, 10) and self.hydro in range(4, 9) and self.pop in range(5, 8):
            self.trade_codes.append("Ag")
        if self.size == 0 and self.atmos_num == 0 and self.hydro == 0:
            self.trade_codes.append("As")
        if self.pop == 0 and self.gov_num == 0 and self.law == 0:
            self.trade_codes.append("Ba")
        if self.atmos_num >= 2 and self.hydro == 0:
            self.trade_codes.append("De")
        if self.atmos_num >= 10 and self.hydro >= 1:
            self.trade_codes.append("Fl")
        if self.size in range(6, 8) and self.atmos_num in [5, 6, 8] and self.hydro in range(5, 8):
            self.trade_codes.append("Ga")
        if self.pop >= 9:
            self.trade_codes.append("Hi")
        if self.tech >= 12:
            self.trade_codes.append("Ht")
        if self.atmos_num in [0, 1] and self.hydro >= 1:
            self.trade_codes.append("Ie")
        if self.atmos_num in [0, 1, 2, 4, 7, 9] and self.pop >= 9:
            self.trade_codes.append("In")
        if self.pop <= 3:
            self.trade_codes.append("Lo")
        if self.tech <= 5:
            self.trade_codes.append("Lt")
        if self.atmos_num in range(0, 4) and self.hydro in range(0, 4) and self.pop >= 6:
            self.trade_codes.append("Na")
        if self.pop <= 6:
            self.trade_codes.append("NI")
        if self.atmos_num in range(2, 5) and self.hydro in range(0, 4):
            self.trade_codes.append("Po")
        if self.atmos_num in [6, 8] and self.pop in range(6, 9) and self.gov_num in range(4, 10):
            self.trade_codes.append("Ri")
        if self.atmos_num == 0:
            self.trade_codes.append("Va")
        if self.hydro >= 10:
            self.trade_codes.append("Wa")

    def gen_gas_giant(self):
        """Calculate the presence of a gas giant in the system"""
        if d6() + d6() <= 10:
            self.gas_giant = True

    def code(self):
        assert (self.starport_class in ["X", "A", "B", "C", "D", "E"]), "Starport class not set"
        assert (self.size in range(11)), "Size not set"
        assert (self.tech in range(21)), "Tech not set " + str(self.tech)
        assert (self.atmos_num in range(16)), "Atmosphere not set"
        assert (self.hydro in range(16)), "Hydrographics not set"
        assert (self.pop in range(16)), "Population not set"
        assert (self.gov_num in range(16)), "Government not set"
        assert (self.law in range(10)), "Law not set"

        code_str = self.starport_class
        if self.size < 10:
            code_str += str(self.size)
        elif self.size == 10:
            code_str += "A"
        else:
            code_str += "Z"

        if self.atmos_num < 10:
            code_str += str(self.atmos_num)
        elif self.atmos_num == 10:
            code_str += "A"
        elif self.atmos_num == 11:
            code_str += "B"
        elif self.atmos_num == 12:
            code_str += "C"
        elif self.atmos_num == 13:
            code_str += "D"
        elif self.atmos_num == 14:
            code_str += "E"
        elif self.atmos_num == 15:
            code_str += "F"
        else:
            code_str += "Z"

        if self.hydro < 10:
            code_str += str(self.hydro)
        elif self.hydro == 10:
            code_str += "A"
        else:
            code_str += "Z"

        if self.pop < 10:
            code_str += str(self.pop)
        elif self.pop == 10:
            code_str += "A"
        elif self.pop == 11:
            code_str += "B"
        elif self.pop == 12:
            code_str += "C"
        else:
            code_str += "Z"

        if self.gov_num < 10:
            code_str += str(self.gov_num)
        elif self.gov_num == 10:
            code_str += "A"
        elif self.gov_num == 11:
            code_str += "B"
        elif self.gov_num == 12:
            code_str += "C"
        elif self.gov_num == 13:
            code_str += "D"
        elif self.gov_num == 14:
            code_str += "E"
        elif self.gov_num == 15:
            code_str += "F"
        else:
            code_str += "Z"

        code_str += str(self.law)
        code_str += "-"
        code_str += str(self.tech)

        for base in self.bases:
            code_str += " "
            code_str += base

        for trade in self.trade_codes:
            code_str += " "
            code_str += trade

        if self.travel_code:
            code_str += "    "
            code_str += self.travel_code

        return code_str
