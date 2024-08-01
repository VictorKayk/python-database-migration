class Migration_Column:
    def __init__(self, old: str, new: str, type: str):
        self.old = old
        self.new = new
        self.type = type

class Migration:
    def __init__(self, old_table: str, new_table: str, columns: list[Migration_Column]):
        self.old_table = old_table
        self.new_table = new_table
        self.columns = columns