class Model:
    def __init__(self, args):
        self.model_name = args[0]
        self.set_name = args[1]
        self.artist_name = args[2]
        self.source_name = args[3]

    def to_list(self):
        result = []
        result.append(self.model_name)
        result.append(self.set_name)
        result.append(self.artist_name)
        result.append(self.source_name)

        return result