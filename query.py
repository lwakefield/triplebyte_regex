from match import Match

class Query(object):

    def __init__(self):
        self.raw = ''
        self.queries = []
        self.brackets = None
        self.suffix = ''

    def match(self, text, index=0):
        matches = []
        for query in self.queries:
            if type(query) is str:
                found_index = text.find(query, index)
                # first query match or consecutive query match
                if (index == 0 and found_index != -1) or (index == found_index):
                    matches.append(Match(found_index, query))
                    index = found_index + len(query)
                else: return None
            else:
                match = query.match(text, index)
                if match is None: return None

                if index == 0 or (index == match.index):
                    matches.append(match)
                    index = match.index + len(match.text)
                else: return None
        return Match.join_matches(matches)

class OrQuery(object):

    def match(self, text, index=0):
        query = self.queries[0]
        if text[index] in query:
            return Match(index, text[index])
        return None
