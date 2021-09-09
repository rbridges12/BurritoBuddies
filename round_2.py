# Riley Bridges
# script to send out results to 2nd wave of participants without emailing the first round

def remove_round_1_email_addrs():
  with open("new_responses.txt", mode="r") as f:
    file = f.readlines()

  new_file = []
  for i, line in enumerate(file):
    try:
      tsv = line.split("\t")
      tsv[0] = "no_address"
      new_file.append("\t".join(tsv))
    except IndexError:
      print("Line %d has incorrect format or is empty" % i)

  with open("new_responses.txt", mode="w") as f:
    f.writelines(new_file)


if __name__ == "__main__":
  remove_round_1_email_addrs()
