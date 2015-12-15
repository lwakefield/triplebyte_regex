class Matcher(object):

    def __init__(self, text):
        self.text = text

    def find_matches(self, pattern):
        if pattern in self.text:
            matches = []
            index = 0
            while True:
                if self.text.find(pattern, index) != -1:
                    new_match = Match(self.text.find(pattern, index), pattern)
                    matches.append(new_match)
                    index = new_match.index + len(pattern)
                else:
                    return matches
        return []

