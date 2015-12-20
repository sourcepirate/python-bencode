import unittest, json

from hypothesis import given
import hypothesis.strategies as st
import collections

#including the target source file.
from bencode import Bencoder


json_strat = st.recursive(
    st.integers() | st.binary(),
    lambda children: st.lists(children) | st.dictionaries(st.text(), children))


def convert2utf8(data):
    if isinstance(data, basestring):
        try:
            return data.encode('utf-8')
        except UnicodeDecodeError:
            return data
    elif isinstance(data, collections.Mapping):
        return dict(map(convert2utf8, data.iteritems()))
    elif isinstance(data, collections.Iterable):
        return type(data)(map(convert2utf8, data))
    else:
        return data


class BecodeTester(unittest.TestCase):

    def test_string_encoding(self):
        """tests string encoding"""
        strs = Bencoder.encode("announce")
        self.assertEqual(strs, "8:announce")

    def test_integer_encoding(self):
        """tests integer encoding"""
        strs = Bencoder.encode(1)
        self.assertEqual(strs, "i1e")

    def test_list_encoding(self):
        """tests list encoding"""
        strs = Bencoder.encode([1,2])
        self.assertEqual(strs, "li1ei2ee")

    def test_dict_encoding(self):
        """tests dictionary encoding"""
        strs = Bencoder.encode(dict(a="1"))
        self.assertEqual(strs, "d1:a1:1e")

    def test_string_decode(self):
        """tests string decode"""
        strs = Bencoder.decode("1:a")
        self.assertEqual(strs, "a")

    def test_list_decode(self):
        """tests list decode"""
        strs = Bencoder.decode("li34ee")
        self.assertEqual(strs, [34])

    def test_integer_decode(self):
        """test integer decode"""
        strs = Bencoder.decode("i34e")
        self.assertEqual(strs, 34)

    def test_dict_decode(self):
        """test dict decode"""
        strs = Bencoder.decode("d4:abcdli34eee")
        self.assertEqual(strs.get("abcd"), [34])

    @given(json_strat)
    def test_can_decode_encoded(self, items):
        if items == '' or items == {}:
            return

        items = convert2utf8(items)

        encoded = Bencoder.encode(items)
        decoded = Bencoder.decode(encoded)
        self.assertEqual(items, decoded)

    def test_critcal(self):
        strs = Bencoder.decode("llee")
        self.assertEqual(strs, [[]])


if __name__ == '__main__':
    unittest.main()
