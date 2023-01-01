import json


class Reader:
    def __init__(self, filepath: str):
        self.data = None
        with open(filepath, 'r') as jsonfile:
            self.data = json.load(jsonfile)
        pass
