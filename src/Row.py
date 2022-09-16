class Row:
  def __init__(self,  title ,exterior ,tradable ,count):
    self.title = title
    self.exterior = exterior
    self.tradeLock = tradable
    self.count = count
    
  def print_row(self):
    print(f'{self.title},  {self.exterior}, {self.tradeLock}, {self.count}')