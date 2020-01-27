from collections import defaultdict
from MatchProfile import MatchProfile

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



def match_value_weighted(order1, order2):

   # split order strings into sets of toppings
  order_set1 = set(order1.strip().split(", "))
  order_set2 = set(order2.strip().split(", "))

  # find intersection and union of the order sets
  intersection = order_set1 & order_set2
  union = order_set1 | order_set2

  similarity = len(intersection)
  difference = len(union)

  for item, weight in weights.items():
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
def find_match(order, other_orders, similarity_function):

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



# finds the best matches in the orders list, prioritizing ideal
# matches for orders at the end of the list
# returns a list of tuples (name1, name2, match value)
# param is orders: dictionary {name : order}
def find_matches_reverseorder(orders):
  matches = []

  # repeat until <2 left to assure a match can be made
  while len(orders) >= 2:
    
    # remove the last item from the dict and find its match
    name, order = orders.popitem()
    match_name, match_val = find_match(order, orders, match_value)

    # add match to matches and remove the matched name from the dict
    matches.append((name, match_name, match_val))
    orders.pop(match_name)
  return matches



# returns a dictionary of all matches bwtween profile and profiles and their match values
# profiles is a list of all MatchProfiles
# similarity_function is a function that takes 2 orders and outputs a similarity value from 0-1
def find_match_dict(profile: MatchProfile, profiles: list, similarity_function) -> dict:
  match_dict = {}

  # iterate through every profile and extract the names and orders of each profile
  for other_profile in profiles:
    other_name = other_profile.get_name()
    other_order = other_profile.get_order()
    
    # if the name is different than the given profile, add the match to the dictionary
    if profile.get_name() != other_name:
      match_dict[other_name] = similarity_function(profile.get_order(), other_order)
  
  # return the match dictionary
  return match_dict



# find the specified number of top matches for each profile
# profiles: a list of all profiles
# num_top_matches: the number of top matches desired
# similarity_function: function that takes 2 orders and returns a similarity value from 0-1
# returns a list of profiles with top_matches defined
def find_top_matches(profiles: list, num_top_matches: int, similarity_function) -> list:
  match_profiles = []

  # iterate through each profile
  for profile in profiles:

    # get a dictionary containing all the matches for the profile
    match_dict = find_match_dict(profile, profiles, similarity_function)

    # get a list of tuples containing the data from match_dict sorted by match value in descending order
    sorted_matches = sorted(match_dict.items(), key = lambda x : x[1], reverse = True)
    
    # empty list for top matches
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




# parse responses from responses.txt (text file containing tab separated values of 2 columns of desired data)
# returns dictionary {name : order}
def parse_responses_dict(file_name) -> dict:
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



# writes the top 3 results to a file
def output_results(file_name):

  # open the file and write the top 3 to it
  with open(file_name, mode = 'w') as f:
    f.write(format_top_3_matches())



# 
def format_best_matches():
  output = ""
  output += "Person 1\t\t\tPerson2\t\t\t% Match\n"
  for p1, p2, match_val in find_matches_reverseorder(parse_responses_dict("responses.txt")):
    output += p1 + "\t" + p2 + "\t" + str(round(match_val*100, ndigits = 2)) + "\n"
  return output

def format_top_3_matches():
  output = ""
  for profile in find_top_matches(dict_to_profiles(parse_responses_dict("responses.txt")), 3, match_value):
    output += "%s's top 3 matches:" % profile.get_name() + "\n"
    matches = profile.get_top_matches()
    output += "\t1:" + "%s, %d%% match"% (matches[0][0], round(matches[0][1]*100, ndigits = 1)) + "\n"
    output += "\t2:" + "%s, %d%% match"% (matches[1][0], round(matches[1][1]*100, ndigits = 1)) + "\n"
    output += "\t3:" + "%s, %d%% match"% (matches[2][0], round(matches[2][1]*100, ndigits = 1)) + "\n"
    output += "\n"
  return output

def get_best_match():
  matches = []
  for profile in find_top_matches(dict_to_profiles(parse_responses_dict("responses.txt")), 3, match_value):
    top_matches = profile.get_top_matches()
    matches.append((profile.get_name(), top_matches[0][0], round(top_matches[0][1] * 100, ndigits = 1)))
  sorted_matches = sorted(matches, key = lambda x : x[2], reverse = True)
  return sorted_matches[0]

def format_topping_popularity_count():
  output = ""
  popularities = count_topping_popularity(parse_responses_dict("responses.txt"))
  sorted_popularities = sorted(popularities.items(), key = lambda x : x[1], reverse = True)
  for item, count in sorted_popularities:
    output += item + count
  return output



weights = {"Rice" : 1, "Black Beans" : 2, "Pinto Beans" : 2, "Chicken" : 1, "Steak" : 1, "Carnitas" : 1, "Tofusada" : 2, "Queso" : 2, "Extra Queso" : 4, "Veggies" : 1, "Cheese" : 1, "Lettuce" : 1, "Corn" : 1, "Pico De Gallo" : 0.5, "Mild Salsa" : 0.5, "Medium Salsa" : 0.5, "Hot Salsa" : 0.5, "Jalapenos" : 1, "Guac" : 2, "Sour Cream" : 2}