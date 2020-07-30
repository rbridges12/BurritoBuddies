# Riley Bridges
# script for sending out conclusion message to all Burrito Buddies participants
# this is to avoid gmail restriction on number of BCCs

from BurritoBuddies import parse_responses, dict_to_profiles
import BurritoMail


def send_finale_message():
    profiles = dict_to_profiles(parse_responses("responses.txt"))
    sender = "burrito-buddies@burrito-buddies.iam.gserviceaccount.com"
    subject = "Burrito Buddies Finale and Giveaway Winner"

    with open("finale_msg.txt", mode="r") as f:
        msg = f.read()

    print(msg)
    BurritoMail.send_group_msg(profiles, sender, subject, msg)


if __name__ == "__main__":
    send_finale_message()
