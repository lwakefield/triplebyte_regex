from query import *
from util import *

class QueryParser(object):
    """
        The QueryParser acts as an iterator, iterating through the raw
            query string building up a query object.
        When a new QueryParser is run, it will strip brackets and suffix
            symbols from the raw query string. If the query string is surrounded
            by square brackets (base case), it is passed to a SetQueryParser.
        The QueryParser maintains a stack of brackets to determine when
            a subquery is found. When a subquery is found it is recursively
            parsed and added to the query tree.
    """

    def __init__(self, raw):
        self.raw = raw
        self.index = 0
        self.brackets = []
        self.query = ''

    def run(self):
        """
            Runs the parser on the raw query string, returning a query object 
            The parser will recursively add subqueries to the query object
                such that we will end up with a query tree
        """
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
            if is_sub_query(self.query):
                sub_query = QueryParser.parse(self.query)
                query.queries.append(sub_query)
            else: 
                query.queries.append(self.query)

        return query

    def get_next_sub_query(self):
        """
        Finds and sets self.query to the next sub query.
        Returns true if a sub query has been found, false otherwise.
        """
        self.query = ''
        self.suffix = ''
        while self.index < len(self.raw):
            val = self.raw[self.index]
            if is_opening_bracket(val) and not self.brackets and self.query != '':
                return True
            elif is_opening_bracket(val) and (self.query == '' or self.brackets):
                self.brackets.append(val)
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
        """
        Called from get_next_sub_query, this checks if there is a suffix
        after the current query.
        If there is a suffix, then it will be added to the current query.
        """
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
        last_bracket = self.brackets[-1]
        if is_closing_bracket(s):
            if last_bracket == '[' and s != ']': raise Exception
            elif last_bracket == '(' and s != ')': raise Exception
            return True
        return False

    @staticmethod
    def parse(raw):
        parser = QueryParser(raw)
        return parser.run()

class SetQueryParser(QueryParser):

    def __init__(self, raw):
        QueryParser.__init__(self, raw)
        self.query_set = ''

    def run(self):
        """
            Runs the parser on the raw query string, returning a query object 
            The parser adds all ranges to the query set, then adds any extra
                values to the query_set
                ex. a-cD-G13579 -> query_set = abcDEFG13579
        """
        while self.raw and self.extract_next_range():
            pass

        self.query_set += self.raw

        query = SetQuery()
        query.queries = [self.query_set]
        return query

    def extract_next_range(self):
        """
        Extracts the next available range in the query string.
        The range is then parsed to its literal form and added to the query set
            ex. a-f -> abcdef, 0-9 -> 0123456789
        """
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
            else: 
                raise Exception

    @staticmethod
    def parse(raw):
        parser = SetQueryParser(raw)
        return parser.run()


