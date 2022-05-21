from cgitb import reset


class Model:
    def __init__(self, args):
        self.model = args[0]
        self.set = args[1]
        self.artist = args[2]
        self.source = args[3]
        self.source_note = args[4]
        self.supports = bool(args[5])
        self.format = args[6]
        self.folder = args[7]
        self.printed = bool(args[8])

    def to_list(self):
        result = []
        result.append(self.model)
        result.append(self.set)
        result.append(self.artist)
        result.append(self.source)
        result.append(self.source_note)
        result.append(self.supports)
        result.append(self.format)
        result.append(self.folder)
        result.append(self.printed)

        return result

class Artist:
    def __init__(self, args):
        self.name = args[0]
        self.website = args[1]
        self.email = args[2]
        self.folder = args[3]

    def to_list(self):
        result = []
        result.append(self.name)
        result.append(self.website)
        result.append(self.email)
        result.append(self.folder)

        return result

class Source:
    def __init__(self, args):
        self.name = args[0]
        self.website = args[1]

    def to_list(self):
        result = []
        result.append(self.name)
        result.append(self.website)

        return result
