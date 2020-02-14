
import BurritoBuddies

BurritoBuddies.output_file = "new_results.txt"
BurritoBuddies.input_file = "new_responses.txt"
#print(BurritoBuddies.format_topping_popularity_count())
#print(BurritoBuddies.format_top_3_matches())
print(BurritoBuddies.get_best_match())
print(BurritoBuddies.format_bidirectional_matches())
BurritoBuddies.output_results(10)
print(BurritoBuddies.find_top_matches(BurritoBuddies.dict_to_profiles(BurritoBuddies.parse_responses(BurritoBuddies.input_file)), 10, BurritoBuddies.match_value)[0].get_top_matches())
