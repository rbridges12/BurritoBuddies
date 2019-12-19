
class MatchProfile:

  def __init__(self, name, order, top_matches = []):
    self.name = name
    self.order = order
    self.top_matches = top_matches

  def get_name(self):
    return self.name

  def get_order(self):
    return self.order

  def get_top_matches(self):
    return self.top_matches

  def set_top_matches(self, top_matches):
    self.top_matches = top_matches