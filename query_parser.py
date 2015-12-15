from query import Query

class QueryParser(object):

    def __init__(self, raw):
        self.raw = raw
        self.index = 0
        self.brackets = []
        self.query = None

    def run(self):
        query = Query()
        query.brackets = self.get_outer_brackets(self.raw)
        self.raw = self.strip_outer_brackets(self.raw)
        query.raw = self.raw

        sub_query = self.get_next_sub_query()
        while sub_query:
            if self.has_outer_brackets(sub_query):
                query.queries.append(QueryParser.parse(sub_query))
            else: 
                query.queries.append(sub_query)
            sub_query = self.get_next_sub_query()

        return query

    def get_next_sub_query(self):
        this_query = ''
        while self.index < len(self.raw):
            val = self.raw[self.index]
            if self.is_opening_bracket(val) and not self.brackets and this_query != '':
                self.query = this_query
                return this_query
            elif self.is_opening_bracket(val) and (this_query == '' or self.brackets):
                self.brackets.append({'index': self.index, 'val': val})
            elif self.is_matching_bracket(val) and len(self.brackets) == 1:
                start_index = self.brackets.pop()['index']
                end_index = self.index
                self.index += 1
                return self.raw[start_index:end_index+1]
            elif self.is_matching_bracket(val) and len(self.brackets) > 1:
                self.brackets.pop()
            this_query += val
            self.index += 1
        return this_query

    def is_matching_bracket(self, s):
        if len(self.brackets) == 0: 
            return False
        last_bracket = self.brackets[-1]['val']
        if self.is_closing_bracket(s):
            if last_bracket == '[' and s != ']': raise Exception
            elif last_bracket == '(' and s != ')': raise Exception
            return True
        return False

    def is_opening_bracket(self, s):
        return s in '(['

    def is_closing_bracket(self, s):
        return s in ')]'

    def has_outer_brackets(self, s):
        return (s[0] == '[' and s[-1] == ']') or (s[0] == '(' and s[-1] == ')')

    def get_outer_brackets(self, s):
        if s[0] == '[' and s[-1] == ']': return '[]'
        elif s[0] == '(' and s[-1] == ')': return '()'
        return None

    def strip_outer_brackets(self, s):
        if self.has_outer_brackets(s) and len(s) >= 2:
            return s[1:-1]
        return s

    @staticmethod
    def parse(raw):
        parser = QueryParser(raw)
        return parser.run()

