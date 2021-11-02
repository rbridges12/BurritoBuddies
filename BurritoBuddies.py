# Riley Bridges
# module for finding participants' matches

from collections import defaultdict
from typing import Match
from MatchProfile import MatchProfile
import json

input_file = "responses.txt"
output_file = "results.txt"
output_json_file = "raw_results.json"

WEIGHTS = {"Rice": 1,
           "Black Beans": 2,
           "Pinto Beans": 2,
           "Chicken": 1,
           "Steak": 1,
           "Carnitas": 1,
           "Tofusada": 2,
           "Queso": 2,
           "Extra Queso": 4,
           "Veggies": 1,
           "Cheese": 1,
           "Lettuce": 1,
           "Corn": 1,
           "Pico De Gallo": 0.5,
           "Mild Salsa": 0.5,
           "Medium Salsa": 0.5,
           "Hot Salsa": 0.5,
           "Jalapenos": 1,
           "Guac": 2,
           "Sour Cream": 2}

match_profiles = []

# returns a number from 0 to 1 describing the match between the
# two given orders, where 0 is a bad match and 1 is a perfect match


def match_value(order1, order2):

    # split order strings into sets of toppings
    order_set1 = set(order1)
    order_set2 = set(order2)

    # find intersection and union of the order sets
    intersection = order_set1 & order_set2
    union = order_set1 | order_set2

    # return the rounded quotient of their sizes
    return round(len(intersection) / len(union), 4)


# returns a number from 0 to 1 describing the match between the
# two given orders, where 0 is a bad match and 1 is a perfect match
# toppings are given different importances when deciding the match value, provided by the weights list
# TODO: fix weighting, currently produces >100% matches
def match_value_weighted(order1, order2):

   # split order strings into sets of toppings
    order_set1 = set(order1.strip().split(", "))
    order_set2 = set(order2.strip().split(", "))

    # find intersection and union of the order sets
    intersection = order_set1 & order_set2
    union = order_set1 | order_set2

    similarity = len(intersection)
    difference = len(union)

    for item, weight in WEIGHTS.items():
        if weight == 0:
            difference -= 1
        if item in intersection:
            similarity += weight - 1
        else:
            difference += weight - 1

    return similarity / difference


# finds the given order's best match in other_orders
# returns a tuple (match name, match value)
# params are order: string, other_orders: dictionary {name : order}
def find_bidirectional_match(order, other_orders, similarity_function):

    # make a dictionary of all other names and their match values
    match_dict = {}
    for name, data in other_orders.items():
        other_order = data[1]
        match_dict[name] = similarity_function(order, other_order)

    # find the max match value
    max_name = max(match_dict, key=match_dict.get)
    max_val = match_dict[max_name]

    # return the max match value with the associated name
    return (max_name, max_val)


# check if two names are the same
# both names are made lowercase and the spaces are removed to ensure only names are compared
def same_name(name1, name2):
    return name1.replace(" ", "").lower() == name2.replace(" ", "").lower()


# returns a dictionary of all matches between profile and profiles and their match values:
# {name : match_value, ...}
# profile is the MatchProfile to find matches for
# profiles is a list of all MatchProfiles
# similarity_function is a function that takes 2 orders and outputs a similarity value from 0-1
def get_match_dict(profile, profiles, similarity_function) -> dict:

    match_dict = {}

    # iterate through every profile and extract the names and orders of each profile
    for other_profile in profiles:
        other_name = other_profile.name
        other_order = other_profile.order

        # if the name is different than the given profile, add the match to the dictionary
        if not same_name(profile.name, other_name):
            match_dict[other_name] = similarity_function(
                profile.order, other_order)

    # return the match dictionary
    return match_dict


# find the specified number of top matches for each profile
# profiles: a list of all profiles
# num_top_matches: the number of top matches desired, or if negative, the number of bottom matches desired
# similarity_function: function that takes 2 orders and returns a similarity value from 0-1
# returns a list of profiles with top_matches defined
def find_top_matches(profiles, num_top_matches, similarity_function) -> list:

    #match_profiles = []

    # if num_top_matches is negative, list will be sorted in ascending order
    reverse = num_top_matches > 0

    # make num_top_matches positive so it works with the for loop
    num_top_matches = abs(num_top_matches)

    # iterate through each profile
    for profile in profiles:

        # get a dictionary containing all the matches for the profile
        match_dict = get_match_dict(profile, profiles, similarity_function)

        # get a list of tuples containing the data from match_dict sorted by match value
        # if num_top_matches was positive, make the list in descending order to get top matches
        # if num_top_matches was negative, make the list in ascending order to get the worst matches
        sorted_matches = sorted(
            match_dict.items(), key=lambda x: x[1], reverse=reverse)

        # make sure the specified number of top matches <= number of possible matches
        if num_top_matches > len(sorted_matches):
            num_top_matches = len(sorted_matches)

        top_matches = sorted_matches[:num_top_matches]

        # make a copy of the match profile but with top matches added to it
        new_profile = MatchProfile(
            profile.name, profile.order, profile.email, top_matches)

        # add the profile to the output list
        match_profiles.append(new_profile)

    # return the list of profiles
    return match_profiles


# returns a formatted string of every person's top matches
def format_top_matches(profiles, num_top_matches):

    output_list = []

    # determine whether the match_type is top or worst
    match_type = "top" if (num_top_matches >= 0) else "worst"

    for profile in profiles:

        # person's header, "top matches" if num_top_matches is positive, "worst matches" if negative
        # TODO: make number of top matches printed decrease if there arent enough profiles
        output_list.append(f"{profile.name}'s {match_type} {num_top_matches} matches:\n")

        # the person's matches in sequential order
        for i, (name, percent) in enumerate(profile.top_matches):
            output_list.append(f"\t{i+1}: {name}, {percent*100:.1f}% match\n")

        # separator newline
        output_list.append("\n")
        
    output = "".join(output_list)
    return output


# convert a dictionary of {name : (email, order), ...} to a list of match_profiles
def dict_to_profiles(response_dict):
    return [MatchProfile(name, order, email)
            for name, (email, order) in response_dict.items()]


# writes results to output files
def output_results(num_top_matches):
    profiles = find_top_matches(dict_to_profiles(
        parse_responses(input_file)), num_top_matches, match_value)

    # write formatted results to output file
    with open(output_file, mode='w') as f:
        f.write(format_top_matches(profiles, num_top_matches))

    # write raw results to JSON file
    with open(output_json_file, mode="w") as f:

        # convert profile objects to dicts so json can encode them
        profile_dicts = list(map(lambda x: x.__dict__, profiles))
        json.dump(profile_dicts, f)


# parse responses from responses.txt (text file containing tsv of 2 columns of desired data)
# returns: a dictionary {name : (email, order), ...}
def parse_responses(file_name) -> dict:
    response_dict = {}

    # open responses.txt in read mode
    with open(file_name, "r") as f:
        for line in f:

            # parse and unpack items from line, raise error if values are missing
            items = line.split("\t")
            if len(items) < 4:
                raise Exception('Not enough values provided')
            email, fname, lname, order = items

            # combine first and last name after removing potential whitespace
            name = fname.strip() + " " + lname.strip()

            order_list = order.strip().split(", ")

            # add name, order, and email to dictionary
            # will prevent duplicate profiles if people fill out form twice
            response_dict[name] = (email, order_list)

    # if file is empty, throw an error
    if len(response_dict) == 0:
        raise Exception('Input file is empty')

    return response_dict


# TODO: use profiles instead of response_dict
# count the number of people who ordered each topping
# response_dict: a dictionary of name: str, order: str pairs
# returns a dictionary of {topping: str, popularity: int} pairs
def count_topping_popularity(response_dict):

    # empty dictionary that defualts to 0 when a new key is called
    counter = defaultdict(int)

    # for each order in the responses
    for email, order in response_dict.values():

        for item in order:

            # increment the items counter
            counter[item] += 1

    # return the counter defaultdict converted to a normal dict
    return dict(counter)


# TODO: comments
# TODO: use profiles instead of response_dict
def format_topping_popularity_count():
    output = "\n\n"
    popularities = count_topping_popularity(parse_responses(input_file))
    sorted_popularities = sorted(
        popularities.items(), key=lambda x: x[1], reverse=True)
    # TODO: add ranking numbers 1-n for toppings
    for topping, count in sorted_popularities:
        output += "%s: %d\n" % (topping, count)
    return output


# TODO: comments
def get_best_match():
    matches = []
    for profile in match_profiles:
        top_matches = profile.top_matches
        if len(top_matches) < 1:
            raise Exception("Not enough responses for a match")
        matches.append((profile.name, top_matches[0][0], round(
            top_matches[0][1] * 100, ndigits=1)))
    sorted_matches = sorted(matches, key=lambda x: x[2], reverse=True)
    return sorted_matches[0]
