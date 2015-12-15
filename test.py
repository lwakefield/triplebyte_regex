import unittest 
from unittest import TestCase

from query_parser import QueryParser

class Tester(TestCase):

    def test_basic_find(self):
        q = QueryParser.parse('sum do')
        match = q.match('lorem imsum dolor sit amet')
        self.assertIsNotNone(match)
        self.assertTrue(match.index == 8)
        self.assertTrue(match.text == 'sum do')

    # def test_find_two(self):
        # matcher = Matcher('Lorem Lorem')
        # matches = matcher.find_matches('em')
        # self.assertTrue(len(matches) == 2)
        # self.assertTrue(matches[0].index == 3)
        # self.assertTrue(matches[1].index == 9)

    def test_basic_query(self):
        q = QueryParser.parse('lorem ipsum')
        self.assertTrue(len(q.queries) == 1)
        self.assertTrue(q.queries[0] == 'lorem ipsum')

    def test_basic_group(self):
        q = QueryParser.parse('lor[em ip]sum')
        self.assertTrue(len(q.queries) == 3)
        self.assertTrue(q.queries[0] == 'lor')
        self.assertTrue(q.queries[1].raw == 'em ip')
        self.assertTrue(q.queries[1].brackets == '[]')
        self.assertTrue(q.queries[2] == 'sum')

    def test_nested_group(self):
        q = QueryParser.parse('lor[e[m i]p]sum')
        self.assertTrue(len(q.queries) == 3)
        self.assertTrue(q.queries[0] == 'lor')
        self.assertTrue(len(q.queries[1].queries) == 3)
        self.assertTrue(q.queries[1].queries[0] == 'e')
        self.assertTrue(q.queries[1].queries[1].raw == 'm i')
        self.assertTrue(q.queries[1].queries[2] == 'p')
        self.assertTrue(q.queries[2] == 'sum')

    def test_basic_query_match(self):
        q = QueryParser.parse('em i[p]')
        match = q.match('lorem ipsum')
        self.assertIsNotNone(match)
        self.assertTrue(match.index == 3)
        self.assertTrue(match.text == 'em ip')

        q = QueryParser.parse('em i[m]')
        match = q.match('lorem ipsum')
        self.assertIsNone(match)

    def text_basic_or_query_match(self):
        q = Query('em i[mp]')
        match = q.match('lorem ipsum')
        self.assertIsNotNone(match)
        self.assertTrue(match.index == 3)
        self.assertTrue(match.text == 'em ip')

        match = q.match('lorem imsum')
        self.assertIsNotNone(match)
        self.assertTrue(match.index == 3)
        self.assertTrue(match.text == 'em im')

        match = q.match('lorem ixsum')
        self.assertIsNone(match)

if __name__ == '__main__':
    unittest.main()

