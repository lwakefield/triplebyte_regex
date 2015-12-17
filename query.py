from match import Match

class Query(object):

    def __init__(self):
        self.raw = ''
        self.queries = []
        self.suffix = ''

    def match(self, text, index=0):
        if '*' in self.suffix:
            return self.match_zero_or_more(text, index)
        elif '+' in self.suffix:
            return self.match_one_or_more(text, index)
        elif '?' in self.suffix:
            return self.match_zero_or_one(text, index)
        return self.match_all_sub_queries(text, index)

    def match_zero_or_one(self, text, index=0):
        match = self.match_all_sub_queries(text, index)
        if match:
            return match
        return Match(index, '')

    def match_one_or_more(self, text, index=0):
        match = self.match_all_sub_queries(text, index)
        if match:
            return self.match_zero_or_more(text, index)
        return None

    def match_zero_or_more(self, text, index=0):
        accumulated_match = Match(index, '')
        while True:
            start_index = index + len(accumulated_match.text)
            match = self.match_all_sub_queries(text, start_index)
            if match and match.index == start_index:
                accumulated_match = Match.join_matches([accumulated_match, match])
            else: break
        return accumulated_match

    def match_all_sub_queries(self, text, index=0):
        while index < len(text):
            matches = []
            for i, query in enumerate(self.queries):
                match = None
                if type(query) is str:
                    found_index = text.find(query, index)
                    match = Match(found_index, query)
                else:
                    match = query.match(text, index)

                if match is None or match.index == -1: return None

                if matches == [] or index == match.index:
                    # if len(match.text):
                    index = match.index + len(match.text)
                    # else:
                        # index += 1
                    matches.append(match)
                elif index != 0 and index != match.index:
                    curr_match = Match.join_matches(matches)
                    if len(curr_match.text) == 0:
                        index += 1
                    break
                else:
                    return None
            else:
                return Match.join_matches(matches)
        return None

class SetQuery(Query):

    def match(self, text, index=0):
        query = self.queries[0]
        for i in range(index, len(text)):
            match = None
            if '*' in self.suffix:
                match = self.match_zero_or_more(text, i)
            elif '+' in self.suffix:
                match = self.match_one_or_more(text, i)
            elif '?' in self.suffix:
                match = self.match_zero_or_one(text, i)
            elif text[index] in query:
                match = Match(i, text[i])
            if match:
                return match
        return None

    def match_zero_or_one(self, text, index=0):
        query = self.queries[0]
        if text[index] in query:
            return Match(index, text[index])
        return Match(index, '')

    def match_one_or_more(self, text, index=0):
        query = self.queries[0]
        match_text = ''
        if text[index] in query:
            return self.match_zero_or_more(text, index)
        return None

    def match_zero_or_more(self, text, index=0):
        query = self.queries[0]
        match_text = ''
        for val in text[index:]:
            if val in query:
                match_text += val
            else: 
                break
        return Match(index, match_text)

