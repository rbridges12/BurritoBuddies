
import BurritoBuddies

BurritoBuddies.output_file = "results.txt"
BurritoBuddies.input_file = "responses.txt"
#print(BurritoBuddies.format_topping_popularity_count())
#print(BurritoBuddies.format_top_3_matches())
print(BurritoBuddies.get_best_match())
print(BurritoBuddies.format_bidirectional_matches())
BurritoBuddies.output_results(3)
