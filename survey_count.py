import csv
import os
import re
import sys
from enum import Enum

import gmap_lookup
from gmap_lookup import GMapIdLookup


class Address:
    def __init__(self, search_string):
        self.search_string = search_string

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


def parse_marked_register_row(row, address_ider: GMapIdLookup):
    address = row["address"]
    voted = int(row["vote2018"])

    if voted not in set(item.value for item in Voted):
        raise Exception('Unexpected voting number in "voted2018": ' + str(voted))

    return address_ider.id_of_place(address + ', Oxford'), Voted(voted)


class MarkedRegisterStats:
    def __init__(self):
        self.marked_reg_entries = 0
        self.non_voters = 0
        self.postal_voters = 0
        self.voted = 0
        self.unknown = 0

    def __str__(self):
        return 'TOTAL: {0} | VOTED: {1} | PV: {2} | DNV: {3}\nUnknown: {4}'.format(self.marked_reg_entries, self.voted,
                                                                                   self.postal_voters, self.non_voters,
                                                                                   self.unknown)


def parse_marked_register(path, address_ider):
    results = {}
    stats = MarkedRegisterStats()

    with open(path, 'r') as csv_file:
        marked_register = csv.DictReader(csv_file)
        for row in marked_register:
            voted: Voted
            address = None
            try:
                address, voted = parse_marked_register_row(row, address_ider)
            except gmap_lookup.InvalidPlaceException:
                stats.unknown += 1
                continue
            if address not in results or (address in results and results[address] == Voted.DNV):
                results[address] = voted
            stats.marked_reg_entries += 1

            if voted == Voted.DNV:
                stats.non_voters += 1
            elif voted == Voted.PV:
                stats.postal_voters += 1
            elif voted == Voted.VOTED:
                stats.voted += 1

    return results, stats


def id_from_road_and_number(road_name, house_number, address_ider):
    return address_ider.id_of_place(address_search_string(house_number, road_name))


def address_search_string(house_number, road_name):
    return house_number + ' ' + road_name + ', Oxford'


def parse_survey_data(path, address_ider):
    results = []
    with open(path, 'r') as csv_file:
        survey_response = csv.reader(csv_file)
        road_name = ''
        for row in survey_response:
            if row[0] and row[0] == 'Road name':
                continue
            if row[0] and row[0] != '':
                road_name = row[0]
            if row[1] and row[1] != '':
                house_number = row[1]
                try:
                    id = id_from_road_and_number(road_name, house_number, address_ider)
                except gmap_lookup.InvalidPlaceException:
                    print('Unable to map location: ' + address_search_string(house_number, road_name))
                results.append(id)

    return results

def parse_donnington_survey_data(path, address_ider):
    results = []
    with open(path, 'r') as csv_file:
        survey_response = csv.reader(csv_file)
        road_name = ''
        for row in survey_response:
            if row[0] and row[0] == 'Road name':
                continue
            if row[1] and row[1] != '':
                road_name = row[1]
            if row[0] and row[0] != '':
                house_number = row[0]
                try:
                    parts = road_name.split(' ')
                    if len(parts) == 1:
                        road_name = road_name + " road"
                    id = id_from_road_and_number(road_name, house_number, address_ider)
                except gmap_lookup.InvalidPlaceException:
                    print('Unable to map location: ' + address_search_string(house_number, road_name))
                results.append(id)

    return results


def analyse_data(marked_register, survey_responses):
    pass


def main():
    if len(sys.argv) < 2:
        print("Expected: <marked_register> <survey_response>[, <survey_response>...]")

    address_ider = GMapIdLookup(os.environ['gmap_key'])
    cache_path = 'gmap_cache.csv'
    address_ider.load_cache(cache_path)
    marked_register_path = sys.argv[1]
    marked_register = {}
    try:
        marked_register, marked_reg_stats = parse_marked_register(marked_register_path, address_ider)
        print(str(marked_reg_stats))

    finally:
        address_ider.save_cache(cache_path)

    results = []
    try:
        for survey_path in sys.argv[2:]:
            results.extend(parse_donnington_survey_data(survey_path, address_ider))
    finally:
        pass
        address_ider.save_cache(cache_path)

    survey_count = len(results)
    surveyed_postal = 0
    surveyed_voted = 0
    surveyed_non_on_reg = 0
    surveyed_dnv = 0
    for survey_response in results:
        if survey_response in marked_register:
            voted = marked_register[survey_response]
            if voted == Voted.DNV:
                surveyed_dnv += 1
            elif voted == Voted.PV:
                surveyed_postal += 1
            elif voted == Voted.VOTED:
                surveyed_voted += 1
        else:
            surveyed_non_on_reg += 1

    spoken_to = 0
    not_spoken_to = 0
    for voter in marked_register:
        if marked_register[voter] == Voted.PV or marked_register[voter] == Voted.VOTED:
            if voter in results:
                spoken_to += 1
            else:
                not_spoken_to += 1

    print('Spoken to: ' + str(spoken_to))
    print('Not spoken to: ' + str(not_spoken_to))

    print('surveyed_postal = ' + str(surveyed_postal))
    print('surveyed_voted = ' + str(surveyed_voted))
    print('surveyed_non_on_reg = ' + str(surveyed_non_on_reg))
    print('surveyed_dnv = ' + str(surveyed_dnv))
    print('survey_responses = ' + str(survey_count))


if __name__ == "__main__":
    main()
