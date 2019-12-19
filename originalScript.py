
# returns a number from 0 to 1 describing the match between the 
# two given orders, where 0 is a bad match and 1 is a perfect match
def match_value(order1, order2):

  # split order strings into sets of toppings
  order_set1 = set(order1.split(", "))
  order_set2 = set(order2.split(", "))

  # find intersection and union of the order sets
  intersection = order_set1 & order_set2
  union = order_set1 | order_set2

  # return the quotient of their sizes
  return len(intersection) / len(union)



# finds the given order's best match in other_orders
# returns a tuple (match name, match value)
# params are order: string, other_orders: dictionary {name : order}
def find_match(order, other_orders):

  # make a dictionary of all other names and their match values
  match_dict = {}
  for name, other_order in other_orders.items():
    match_dict[name] = match_value(order, other_order)
  
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
    match_name, match_val = find_match(order, orders)

    # add match to matches and remove the matched name from the dict
    matches.append((name, match_name, match_val))
    orders.pop(match_name)
  return matches



# parse responses from responses.txt (text file containing tab separated values of 2 columns of desired data)
# returns dictionary {name : order}
def parse_responses():
  response_dict = {}

  # open responses.txt in read mode
  with open("responses.txt", "r") as f:
    for line in f:

      # split each line of file into name and order
      items = line.split("\t")
      order = items[0]

      # remove whitespace from end of name
      name = items[1].rstrip()

      # add name and order to dictionary
      response_dict[name] = order
  return response_dict    



print("Person 1\t\t\tPerson2\t\t\t% Match")
for p1, p2, match_val in find_matches_reverseorder(parse_responses()):
  print(p1,"\t", p2, "\t", round(match_val*100, 2))