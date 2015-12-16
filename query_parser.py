from query import *

class QueryParser(object):

    def __init__(self, raw):
        self.raw = raw
        self.index = 0
        self.brackets = []
        self.query = ''
        self.suffix = ''

    def run(self):
        if self.get_outer_brackets(self.raw) == '[]':
            query = SetQuery()
            query.queries = [self.strip_outer_brackets(self.raw)]
            query.suffix = self.suffix
            return query

        query = Query()
        query.brackets = self.get_outer_brackets(self.raw)
        query.suffix = self.suffix
        self.raw = self.strip_outer_brackets(self.raw)
        query.raw = self.raw

        self.get_next_sub_query()
        while self.query:
            if self.has_outer_brackets(self.query):
                query.queries.append(QueryParser.parse(self.query, self.suffix))
            else: 
                query.queries.append(self.query)
            self.get_next_sub_query()

        return query

    def get_next_sub_query(self):
        self.query = ''
        self.suffix = ''
        while self.index < len(self.raw):
            val = self.raw[self.index]
            if self.is_opening_bracket(val) and not self.brackets and self.query != '':
                return 
            elif self.is_opening_bracket(val) and (self.query == '' or self.brackets):
                self.brackets.append({'index': self.index, 'val': val})
            elif self.is_matching_bracket(val):
                self.brackets.pop()
                if len(self.brackets) == 0:
                    self.index += 1
                    self.query += val
                    self.get_next_suffix()
                    return
            self.query += val
            self.index += 1

    def get_next_suffix(self):
        self.suffix = ''
        while self.index < len(self.raw):
            val = self.raw[self.index]
            if val in '+*?':
                self.suffix += val
            else:
                return
            self.index += 1

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
    def parse(raw, suffix=''):
        parser = QueryParser(raw)
        parser.suffix = suffix
        return parser.run()

