from query import *

class QueryParser(object):

    def __init__(self, raw):
        self.raw = raw
        self.index = 0
        self.brackets = []
        self.query = ''
        self.suffix = ''

    def run(self):
        suffix = self.strip_suffix(self.raw)
        brackets = self.strip_outer_brackets()

        if brackets == '[]':
            return SetQueryParser.parse(self.raw, self.suffix)

        query = Query()
        query.suffix = self.suffix
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

    def strip_outer_brackets(self):
        brackets = self.get_outer_brackets(self.raw)
        if self.has_outer_brackets(self.raw) and len(self.raw) >= 2:
            self.raw = self.raw[1:-1]
        return brackets

    def strip_suffix(self, s):
        suffix = ''
        for c in s:
            if c in '+*?':
                suffix += c
            else:
                break
        return s[:-len(suffix)]

    @staticmethod
    def parse(raw, suffix=''):
        parser = QueryParser(raw)
        parser.suffix = suffix
        return parser.run()

class SetQueryParser(QueryParser):

    def __init__(self, raw):
        QueryParser.__init__(self, raw)
        self.query_set = ''

    def run(self):
        while self.raw and self.extract_next_range():
            pass

        self.query_set += self.raw

        query = SetQuery()
        query.queries = [self.query_set]
        query.suffix = self.suffix
        return query

    def extract_next_range(self):
        if '-' in self.raw:
            index = self.raw.find('-')
            before = self.raw[index - 1]
            after = self.raw[index + 1]
            if ((before.islower() and after.islower()) or
                    (before.isupper() and after.isupper()) or
                    (before.isdigit() and after.isdigit())):
                set_range = ''.join(map(chr, range(ord(before), ord(after)+1)))
                self.query_set += set_range
                self.raw = self.raw[0:index-1] + self.raw[index+2:]
                return self.query_set
            else: raise Exception

    @staticmethod
    def parse(raw, suffix=''):
        parser = SetQueryParser(raw)
        parser.suffix = suffix
        return parser.run()


