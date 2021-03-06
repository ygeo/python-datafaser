import unittest
from datafaser.data_tree import DataTree


class MergeTest(unittest.TestCase):

    def test_merge_scalar_ok(self):
        result = self._merge('foo', 'bar')
        self.assertEqual('bar', result, 'Overwrites scalar even on top level')

    def test_merge_toplevel_list_appends_ok(self):
        l1 = ['foo']
        l2 = ['bar']
        result = self._merge(l1, l2)
        self.assertIsNot(l1, result, 'Original list not used')
        self.assertIsNot(l2, result, 'Added list not used')
        self.assertEqual(['foo','bar'], result, 'New list contains new items after old ones')

    def test_merge_inner_list_appends_ok(self):
        l1 = {'a': {'b': ['foo']}}
        l2 = {'a': {'b': ['bar']}}
        result = self._merge(l1, l2)
        self.assertIsNot(l1, result, 'Original list not used')
        self.assertIsNot(l2, result, 'Added list not used')
        self.assertEqual({'a': {'b': ['foo','bar']}}, result, 'New list contains new items after old ones')

    def test_merge_dict_adds_key_ok(self):
        d1 = {'foo': 1}
        d2 = {'bar': 2}
        result = self._merge(d1, d2)
        self.assertIsNot(d1, result, 'Original dict not used')
        self.assertIsNot(d2, result, 'Added dict not used')
        self.assertEqual({'foo': 1, 'bar': 2}, result, 'New dict contains both old and new items')

    def test_merge_scalar_overwrites_ok(self):
        d1 = {'foo': {'bar': 1}, 'baz': 2}
        d2 = {'foo': 'quu'}
        result = self._merge(d1, d2)
        self.assertIsNot(d1, result, 'Original dict not used')
        self.assertIsNot(d2, result, 'Added dict not used')
        self.assertEqual({'foo': 'quu', 'baz': 2}, result, 'New dict contains overriding item')

    def test_merge_repeated_references_ok(self):
        repeated = {
            'rabbit hole': {
                'Rei': 'Who am I?',
                'Shinji': 'Why am I here?'
            }
        }
        expected = {
            'deep': repeated,
            'down': repeated,
            'inside': {'honey': 'you', 'need': 'love'}
        }
        repeated1 = {'rabbit hole': {'Rei': 'Who am I?'}}
        repeated2 = {'rabbit hole': {'Shinji': 'Why am I here?'}}
        d1 = {'deep': repeated1, 'down': repeated1, 'inside': {'honey': 'you'}}
        d2 = {'deep': repeated2, 'down': repeated2, 'inside': {'need': 'love'}}

        result = self._merge(d1, d2)

        self.assertEqual(expected, result, 'Dicts containing repeated entries are merged')
        self.assertIs(result['deep'], result['down'], 'Repeated references are reflected in result')
        self.assertIsNot(result['deep'], d1['deep'], 'Repeated references do not target source data')
        self.assertIsNot(result['deep'], d2['deep'], 'Repeated references do not target merge data')

    def test_merge_cyclic_reference_ok(self):
        d1 = {'foo': {'zer': 'zor'}, 'zup': 'zop'}
        d1['foo']['bar'] = d1
        d2 = {'foo': {'baz': 'quu'}, 'zip': 'zap'}
        d2['foo']['bar'] = d2
        expected = {'foo': {'baz': 'quu', 'zer': 'zor'}, 'zip': 'zap', 'zup': 'zop'}

        result = self._merge(d1, d2)

        self.assertIs(result, result['foo']['bar'], 'Dicts are merged with cyclic reference')
        del result['foo']['bar']
        self.assertEqual(expected, result, 'Dicts are merged despite cyclic reference')

    def test_merge_into_nonexisting_branch_ok(self):
        result = self._merge({}, ['thingy'], key_path=['sub', 'part'])
        expected = {'sub': {'part': ['thingy']}}
        self.assertEqual(expected, result, 'Merging into nonexisting branch creates it')

    def _merge(self, data1, data2, **kwargs):
        d = DataTree(data1)
        d.merge(data2, **kwargs)
        return d.data
