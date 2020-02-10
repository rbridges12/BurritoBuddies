# Riley Bridges

from collections import defaultdict
from MatchProfile import MatchProfile

input_file = "responses.txt"
output_file = "results.txt"

WEIGHTS = {"Rice" : 1, "Black Beans" : 2, "Pinto Beans" : 2, "Chicken" : 1, "Steak" : 1, "Carnitas" : 1, "Tofusada" : 2, "Queso" : 2, "Extra Queso" : 4, "Veggies" : 1, "Cheese" : 1, "Lettuce" : 1, "Corn" : 1, "Pico De Gallo" : 0.5, "Mild Salsa" : 0.5, "Medium Salsa" : 0.5, "Hot Salsa" : 0.5, "Jalapenos" : 1, "Guac" : 2, "Sour Cream" : 2}

# returns a number from 0 to 1 describing the match between the
# two given orders, where 0 is a bad match and 1 is a perfect match
def match_value(order1, order2):

  # split order strings into sets of toppings
  order_set1 = set(order1.strip().split(", "))
  order_set2 = set(order2.strip().split(", "))

  # find intersection and union of the order sets
  intersection = order_set1 & order_set2
  union = order_set1 | order_set2

  # return the quotient of their sizes
  return len(intersection) / len(union)



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
  for name, other_order in other_orders.items():
    match_dict[name] = similarity_function(order, other_order)

  # find the max match value
  max = -1
  max_name = ""
  for name, match_val in match_dict.items():
    if match_val > max:
      max = match_val
      max_name = name

  # return the max match value with the associated name
  return (max_name, max)



# finds the
# matches for orders at the end of the list
# returns a list of tuples (name1, name2, match value)
# param is orders: dictionary {name : order}
def find_bidirectional_matches_reverseorder(orders) -> list:
  matches = []

  # repeat until <2 left to assure a match can be made
  while len(orders) >= 2:

    # remove the last item from the dict and find its match
    name, order = orders.popitem()
    match_name, match_val = find_bidirectional_match(order, orders, match_value)

    # add match to matches and remove the matched name from the dict
    matches.append((name, match_name, match_val))
    orders.pop(match_name)
  return matches



# returns a string of formatted bidirectional matches
def format_bidirectional_matches() -> str:

  # headings
  output = "Person 1\t\tPerson2\t\t% Match\n"

  # matches
  for p1, p2, match_val in find_bidirectional_matches_reverseorder(parse_responses(input_file)):
    output += "%s\t%s\t%.1f\n" %(p1, p2, match_val*100)

  return output



# returns a dictionary of all matches between profile and profiles and their match values:
# {name : match_value, ...}
# profile is the MatchProfile to find matches for
# profiles is a list of all MatchProfiles
# similarity_function is a function that takes 2 orders and outputs a similarity value from 0-1
def get_match_dict(profile, profiles, similarity_function) -> dict:

  match_dict = {}

  # iterate through every profile and extract the names and orders of each profile
  for other_profile in profiles:
    other_name = other_profile.get_name()
    other_order = other_profile.get_order()

    # if the name is different than the given profile, add the match to the dictionary
    # both names are made lowercase and the spaces are removed to ensure only names are compared
    if profile.get_name().replace(" ", "").lower() != other_name.replace(" ", "").lower():
      match_dict[other_name] = similarity_function(profile.get_order(), other_order)

  # return the match dictionary
  return match_dict



# find the specified number of top matches for each profile
# profiles: a list of all profiles
# num_top_matches: the number of top matches desired, or if negative, the number of bottom matches desired
# similarity_function: function that takes 2 orders and returns a similarity value from 0-1
# returns a list of profiles with top_matches defined
def find_top_matches(profiles, num_top_matches, similarity_function) -> list:

  match_profiles = []

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
    sorted_matches = sorted(match_dict.items(), key = lambda x : x[1], reverse = reverse)

    top_matches = []

    # make sure the specified number of top matches <= number of possible matches
    if num_top_matches > len(sorted_matches):
      num_top_matches = len(sorted_matches)

    # add the specified number of top matches to the list
    for i in range(num_top_matches):
      top_matches.append(sorted_matches[i])

    # add the list to the profile as its top_matches variable
    profile.set_top_matches(top_matches)

    # add the profile to the output list
    match_profiles.append(profile)

  # return the list of profiles
  return match_profiles



# returns a formatted string of every person's top matches
def format_top_matches(num_top_matches):

  output = ""

  # determine whether the match_type is top or worst
  match_type = "top" if (num_top_matches >= 0) else "worst"

  # get the profiles with matches from the responses file
  profiles = find_top_matches(dict_to_profiles(parse_responses(input_file)), num_top_matches, match_value)

  for profile in profiles:

    # person's header, "top matches" if num_top_matches is positive, "worst matches" if negative
    output += "%s's %s 3 matches:\n" %(profile.get_name(), match_type)

    # the person's matches in sequential order
    matches = profile.get_top_matches()
    for i in range(len(matches)):
      output += "\t%d: %s, %.1f%% match\n"% (i + 1, matches[i][0], matches[i][1]*100)

    # separator newline
    output += "\n"
  return output



# writes the top results to a file
def output_results(num_top_matches):

  # open the file and write the top results to it
  with open(output_file, mode = 'w') as f:
    f.write(format_top_matches(num_top_matches))



# parse responses from responses.txt (text file containing tab separated values of 2 columns of desired data)
# returns dictionary {name : order}
def parse_responses(file_name) -> dict:
  response_dict = {}

  # open responses.txt in read mode
  with open(file_name, "r") as f:
    for line in f:

      # split each line of file into name and order
      items = line.split("\t")
      order = items[0]

      # remove whitespace from end of name
      name = items[1].rstrip()

      # add name and order to dictionary
      response_dict[name] = order

  # if file is empty, throw an error
  if len(response_dict) == 0: raise Exception('Input file is empty')

  return response_dict


# convert a dictionary of name, order pairs into a list of profiles
def dict_to_profiles(dict: dict) -> list:

  # empty list for profiles
  profiles = []

  # for each name and order, create a new profile and add it to the list
  for name, order in dict.items():
    profile = MatchProfile(name, order)
    profiles.append(profile)

  # return the list
  return profiles



# count the number of people who ordered each topping
# response_dict: a dictionary of name: str, order: str pairs
# returns a dictionary of {topping: str, popularity: int} pairs
def count_topping_popularity(response_dict):

  # empty dictionary that defualts to 0 when a new key is called
  counter = defaultdict(int)

  # for each order in the responses
  for order in response_dict.values():

    # for each item in the order, remove whitespace from the ends of order and split it into individual items
    for item in order.strip().split(", "):

      # increment the items counter
      counter[item] += 1

  # return the counter defaultdict converted to a normal dict
  return dict(counter)



# TODO: comments
def format_topping_popularity_count():
  output = "\n\n"
  popularities = count_topping_popularity(parse_responses(input_file))
  sorted_popularities = sorted(popularities.items(), key = lambda x : x[1], reverse = True)
  # TODO: add ranking numbers 1-n for toppings
  for topping, count in sorted_popularities:
    output +=  "%s: %d\n" %(topping, count)
  return output




# TODO: comments
def get_best_match():
  matches = []
  for profile in find_top_matches(dict_to_profiles(parse_responses(input_file)), 3, match_value):
    top_matches = profile.get_top_matches()
    matches.append((profile.get_name(), top_matches[0][0], round(top_matches[0][1] * 100, ndigits = 1)))
  sorted_matches = sorted(matches, key = lambda x : x[2], reverse = True)
  return sorted_matches[0]



# TODO: add 3 worst matches
