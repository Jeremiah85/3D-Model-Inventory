class Model:
    def __init__(self, args):
        self.model_name = args[0]
        self.set_name = args[1]
        self.artist_name = args[2]
        self.source_name= args[3]
        self.source_note = args[4]
        self.supports = bool(args[5])
        self.format = args[6]
        self.artist_folder = args[7]
        self.printed = bool(args[8])

    def to_list(self):
        result = []
        result.append(self.model_name)
        result.append(self.set_name)
        result.append(self.artist_name)
        result.append(self.source_name)
        result.append(self.source_note)
        result.append(self.supports)
        result.append(self.format)
        result.append(self.artist_folder)
        result.append(self.printed)

        return result