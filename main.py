
import BurritoBuddies
import BurritoMail

BurritoBuddies.output_file = "new_results.txt"
BurritoBuddies.input_file = "new_responses.txt"

print(BurritoBuddies.format_topping_popularity_count())
print(BurritoBuddies.get_best_match())

BurritoBuddies.output_results(10)

profiles = BurritoBuddies.match_profiles
sender = "burrito-buddies@burrito-buddies.iam.gserviceaccount.com"
BurritoMail.send_results(profiles, sender)
