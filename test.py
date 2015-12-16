import unittest 
from unittest import TestCase

from query_parser import QueryParser
from query import *

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
        q = QueryParser.parse('lor(em ip)sum')
        self.assertTrue(len(q.queries) == 3)
        self.assertTrue(q.queries[0] == 'lor')
        self.assertTrue(q.queries[1].raw == 'em ip')
        self.assertTrue(q.queries[1].brackets == '()')
        self.assertTrue(q.queries[2] == 'sum')

        q = QueryParser.parse('lor[em ip]sum')
        self.assertTrue(len(q.queries) == 3)
        self.assertTrue(q.queries[0] == 'lor')
        self.assertTrue(type(q.queries[1]) == OrQuery)
        self.assertTrue(q.queries[1].queries[0] == 'em ip')
        self.assertTrue(q.queries[2] == 'sum')

    def test_nested_group(self):
        q = QueryParser.parse('lor(e(m i)p)sum')
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

    def test_basic_or_query_match(self):
        q = OrQuery()
        q.queries = ['mp']

        match = q.match('m')
        self.assertIsNotNone(match)
        self.assertTrue(match.index == 0)
        self.assertTrue(match.text == 'm')

        match = q.match('p')
        self.assertIsNotNone(match)
        self.assertTrue(match.index == 0)
        self.assertTrue(match.text == 'p')

        match = q.match('q')
        self.assertIsNone(match)

    def test_embedded_or_query_match(self):
        q = QueryParser.parse('em i[mp]sum')

        match = q.match('lorem ipsum')
        self.assertIsNotNone(match)
        self.assertTrue(match.index == 3)
        self.assertTrue(match.text == 'em ipsum')

        match = q.match('lorem imsum')
        self.assertIsNotNone(match)
        self.assertTrue(match.index == 3)
        self.assertTrue(match.text == 'em imsum')

        match = q.match('lorem ixsum')
        self.assertIsNone(match)

if __name__ == '__main__':
    unittest.main()

