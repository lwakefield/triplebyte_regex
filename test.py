import unittest 
from unittest import TestCase

from query_parser import *
from query import *

class Tester(TestCase):

    def test_basic_match(self):
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
        self.assertTrue(q.queries[2] == 'sum')

        q = QueryParser.parse('lor[em ip]sum')
        self.assertTrue(len(q.queries) == 3)
        self.assertTrue(q.queries[0] == 'lor')
        self.assertTrue(type(q.queries[1]) == SetQuery)
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

    def test_basic_set_query_match(self):
        q = SetQuery()
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

    def test_embedded_set_query_match(self):
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

    def test_basic_suffix(self):
        q = QueryParser.parse('i [am]* this')
        match = q.match('i  this')
        self.assertIsNotNone(match)
        match = q.match('i am this')
        self.assertIsNotNone(match)
        match = q.match('i amma this')
        self.assertIsNotNone(match)

        q = QueryParser.parse('i [am]+')
        self.assertIsNotNone(q)
        self.assertTrue(len(q.queries) == 2)
        self.assertTrue(q.queries[1].queries == ['am'])
        self.assertTrue(q.queries[1].suffix == '+')
        match = q.match('lorem i aam not')
        self.assertIsNotNone(match)
        self.assertTrue(match.index == 6)
        self.assertTrue(match.text == 'i aam')

        q = QueryParser.parse('i [am]? this')
        match = q.match('i  this')
        self.assertIsNotNone(match)
        match = q.match('i a this')
        self.assertIsNotNone(match)
        match = q.match('i am this')
        self.assertIsNone(match)

        q = QueryParser.parse('hello( i am)*')
        match = q.match('hello')
        self.assertIsNotNone(match)
        self.assertTrue(match.text == 'hello')
        match = q.match('hello i am')
        self.assertIsNotNone(match)
        self.assertTrue(match.text == 'hello i am')
        match = q.match('hello i am i am')
        self.assertIsNotNone(match)
        self.assertTrue(match.text == 'hello i am i am')

        q = QueryParser.parse('hello( i am)+')
        match = q.match('hello')
        self.assertIsNone(match)
        match = q.match('hello i am')
        self.assertIsNotNone(match)
        self.assertTrue(match.text == 'hello i am')
        match = q.match('hello i am i am')
        self.assertIsNotNone(match)
        self.assertTrue(match.text == 'hello i am i am')

        q = QueryParser.parse('hello( i am)? this')
        match = q.match('hello this')
        self.assertIsNotNone(match)
        match = q.match('hello i am this')
        self.assertIsNotNone(match)
        self.assertTrue(match.text == 'hello i am this')
        match = q.match('hello i am i am this')
        self.assertIsNone(match)

    def test_set_parser(self):
        q = SetQueryParser.parse('basic')
        self.assertTrue(q.queries == ['basic'])

        q = SetQueryParser.parse('a-z')
        self.assertTrue(q.queries == ['abcdefghijklmnopqrstuvwxyz'])

        q = SetQueryParser.parse('j-l')
        self.assertTrue(q.queries == ['jkl'])

        q = SetQueryParser.parse('J-L')
        self.assertTrue(q.queries == ['JKL'])

        q = SetQueryParser.parse('0-9')
        self.assertTrue(q.queries == ['0123456789'])

        q = SetQueryParser.parse('4-6')
        self.assertTrue(q.queries == ['456'])

        q = SetQueryParser.parse('0-9a-z')
        self.assertTrue(q.queries == ['0123456789abcdefghijklmnopqrstuvwxyz'])

        q = SetQueryParser.parse('0-9a-z')
        self.assertTrue(q.queries == ['0123456789abcdefghijklmnopqrstuvwxyz'])

        q = SetQueryParser.parse('0-3a-cJ-L')
        self.assertTrue(q.queries == ['0123abcJKL'])

    def test_complex_queries(self):
        q = QueryParser.parse('[a-zA-Z0-9]*@[a-z]*.com')
        match = q.match('lawrence112@testemail.com')
        self.assertIsNotNone(match)
        self.assertTrue(match.index == 0)
        self.assertTrue(match.text == 'lawrence112@testemail.com')
        match = q.match('not a valid email address @.notcom')
        self.assertIsNone(match)
        match = q.match('there is an email@address.com in this string')
        self.assertIsNotNone(match)
        self.assertTrue(match.text == 'email@address.com')
        self.assertTrue(match.index == 12)

if __name__ == '__main__':
    unittest.main()

