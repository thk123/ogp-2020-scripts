import csv
import re
import sys
from enum import Enum


class Address:
    def __init__(self, road, house_number):
        self.road = road
        self.house_number = house_number

    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(other, Address):
            return self.road == other.road and self.house_number == other.house_number
        return False

    def __str__(self):
        if self.road and self.house_number:
            return self.house_number + " " + self.road
        else:
            return "<invalid address>"

    def __hash__(self):
        return hash(self.road) ^ self.house_number

    @staticmethod
    def from_full_string(full_address):
        pattern = r"(\d+)\s+([\w\s+]+)$"
        result = re.match(pattern, full_address)
        if not result:
            raise Exception("Could not parse " + full_address)
        street_name = result.group(2)
        number = int(result.group(1))

        return Address(street_name, number)


class Voted(Enum):
    DNV = 0
    VOTED = 1
    PV = 2


def parse_marked_register_row(row):
    address = row["address"]
    voted = int(row["vote2018"])

    if voted not in set(item.value for item in Voted):
        raise Exception('Unexpected voting number in "voted2018": ' + str(voted))

    return Address.from_full_string(address), Voted(voted)


class MarkedRegisterStats:
    def __init__(self):
        self.marked_reg_entries = 0
        self.non_voters = 0
        self.postal_voters = 0
        self.voted = 0

    def __str__(self):
        return 'TOTAL: {0} | VOTED: {1} | PV: {2} | DNV: {3}'.format(self.marked_reg_entries, self.voted,
                                                                     self.postal_voters, self.non_voters)


def parse_marked_register(path):
    results = {}
    stats = MarkedRegisterStats()
    with open(path, 'r') as csv_file:
        marked_register = csv.DictReader(csv_file)
        for row in marked_register:
            print(row)
            voted: Voted
            address, voted = parse_marked_register_row(row)
            results[address] = voted
            stats.marked_reg_entries += 1

            if voted == Voted.DNV:
                stats.non_voters += 1
            elif voted == Voted.PV:
                stats.postal_voters += 1
            elif voted == Voted.VOTED:
                stats.voted += 1

    return results, stats


def main():
    if len(sys.argv) < 2:
        print("Expected: <marked_register> <survey_response>[, <survey_response>...]")

    marked_register_path = sys.argv[1]
    marked_register, marked_reg_stats = parse_marked_register(marked_register_path)
    print(str(marked_reg_stats))
    # totals

    survey_responses = 0
    surveyed_postal = 0
    surveyed_voted = 0
    surveyed_non_on_reg = 0
    surveyde_dnv = 0


if __name__ == "__main__":
    main()
