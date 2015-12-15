class Match(object):

    def __init__(self, index, text):
        self.index = index
        self.text = text

    @staticmethod
    def join_matches(matches):
        match = Match(matches[0].index, '')
        for m in matches:
            match.text += m.text
        return match

