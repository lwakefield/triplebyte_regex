from query import *
from util import *

class QueryParser(object):

    def __init__(self, raw):
        self.raw = raw
        self.index = 0
        self.brackets = []
        self.query = ''
        self.suffix = ''

    def run(self):
        suffix = get_suffix(self.raw)
        brackets = get_outer_brackets(self.raw)

        self.raw = strip(self.raw)

        if brackets == '[]':
            query = SetQueryParser.parse(self.raw)
            query.suffix = suffix
            return query

        query = Query()
        query.suffix = suffix
        query.raw = self.raw

        while self.get_next_sub_query():
            if get_outer_brackets(self.query):
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
            if is_opening_bracket(val) and not self.brackets and self.query != '':
                return True
            elif is_opening_bracket(val) and (self.query == '' or self.brackets):
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
        if is_closing_bracket(s):
            if last_bracket == '[' and s != ']': raise Exception
            elif last_bracket == '(' and s != ')': raise Exception
            return True
        return False

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


