# Riley Bridges
# module/class to represent participants and store their matches and info

class MatchProfile:

  def __init__(self, name, order, email, top_matches=None):
    self.name = name
    self.order = order
    self.email = email

    if top_matches is None:
      top_matches = []

    self.top_matches = top_matches
