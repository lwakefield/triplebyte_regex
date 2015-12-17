from query import *

class QueryParser(object):

    def __init__(self, raw):
        self.raw = raw
        self.index = 0
        self.brackets = []
        self.query = ''
        self.suffix = ''

    def run(self):
        suffix = self.get_suffix(self.raw)
        brackets = self.get_outer_brackets(self.raw)

        if suffix and brackets:
            self.raw = self.strip_suffix(self.raw)
        if brackets:
            self.raw = self.strip_outer_brackets(self.raw)

        if brackets == '[]':
            query = SetQueryParser.parse(self.raw)
            query.suffix = suffix
            return query

        query = Query()
        if suffix and brackets:
            query.suffix = suffix
        query.raw = self.raw

        while self.get_next_sub_query():
            if self.has_outer_brackets(self.query):
                sub_query = QueryParser.parse(self.query)
                query.queries.append(sub_query)
            else: 
                query.queries.append(self.query)

        return query

    def get_next_sub_query(self):
        self.query = ''
        self.suffix = ''
        while self.index < len(self.raw):
            val = self.raw[self.index]
            if self.is_opening_bracket(val) and not self.brackets and self.query != '':
                return True
            elif self.is_opening_bracket(val) and (self.query == '' or self.brackets):
                self.brackets.append({'index': self.index, 'val': val})
            elif self.is_matching_bracket(val):
                self.brackets.pop()
                if len(self.brackets) == 0:
                    self.index += 1
                    self.query += val
                    self.get_next_suffix()
                    return True
            self.query += val
            self.index += 1
        return len(self.query) > 0

    def get_next_suffix(self):
        self.suffix = ''
        while self.index < len(self.raw):
            val = self.raw[self.index]
            if val in '+*?':
                self.query += val
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

    def has_suffix(self, s):
        suffix = self.get_suffix(s)
        brackets = self.get_outer_brackets(s)
        return bool(suffix) and bool(brackets)

    def is_opening_bracket(self, s):
        return s in '(['

    def is_closing_bracket(self, s):
        return s in ')]'

    def has_outer_brackets(self, s):
        s = self.strip_suffix(s)
        return (s[0] == '[' and s[-1] == ']') or (s[0] == '(' and s[-1] == ')')

    def get_outer_brackets(self, s):
        s = self.strip_suffix(s)
        if s[0] == '[' and s[-1] == ']': return '[]'
        elif s[0] == '(' and s[-1] == ')': return '()'
        return None

    def strip_outer_brackets(self, s):
        if self.has_outer_brackets(s) and len(s) >= 2:
            return s[1:-1]
        return s

    def strip_suffix(self, s):
        suffix = self.get_suffix(s)
        if len(suffix):
            return s[:-len(suffix)]
        return s

    def get_suffix(self, s):
        suffix = ''
        for c in s[::-1]:
            if c in '+*?':
                suffix += c
            else:
                break
        return suffix[::-1]

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
    def parse(raw):
        parser = SetQueryParser(raw)
        return parser.run()


