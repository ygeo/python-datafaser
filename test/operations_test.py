import copy
import unittest

from datafaser.data_tree import DataTree
from datafaser.operations import Loader
from datafaser import formats


class LoadTest(unittest.TestCase):
    _minimum_required_settings = {
        'datafaser': {
            'formats': formats.default_settings
        }
    }

    def test_load_without_directives_ok(self):
        loader = Loader(DataTree(copy.deepcopy(self._minimum_required_settings)))
        target = {}
        loader.load(DataTree(target), {})
        self.assertEquals({}, target, 'Empty result for empy directives')

    def test_load_nothing_to_data_ok(self):
        loader = Loader(DataTree(copy.deepcopy(self._minimum_required_settings)))
        target = {'There': 'Misty Mountain'}
        loader.load(DataTree(target), {'to': [{'data': 'Back'}]})
        self.assertEquals({'There': 'Misty Mountain', 'Back': {}}, target,
                          'Loading nothing to nonexistent key creates the key with an empty dictionary')

    def test_load_from_data_to_data_ok(self):
        loader = Loader(DataTree(copy.deepcopy(self._minimum_required_settings)))
        target = {'There': 'Misty Mountain'}
        loader.load(DataTree(target), {'from': [{'data': ['There']}], 'to': [{'data': 'Back'}]})
        self.assertEquals({'There': 'Misty Mountain', 'Back': 'Misty Mountain'}, target,
                          'Loading from data to data copies the source to the target')

    def test_load_from_dictionary_fails(self):
        exception = self._exception_from_loading_with({}, {'from': {}})
        self.assertIsInstance(exception, TypeError, 'Invalid from structure causes type error')

    def test_load_from_non_dict_source_fails(self):
        exception = self._exception_from_loading_with({}, {'from': [[]]})
        self.assertIsInstance(exception, TypeError, 'Invalid from source causes type error')

    def test_load_from_non_list_files_source_fails(self):
        exception = self._exception_from_loading_with({}, {'from': [{'files': 'y'}]})
        self.assertIsInstance(exception, TypeError, 'Invalid from source causes type error')

    def test_load_from_unknown_source_type_fails(self):
        exception = self._exception_from_loading_with({}, {'from': [{'x': []}]})
        self.assertIsInstance(exception, KeyError, 'Invalid from source causes type error')

    def _exception_from_loading_with(self, source, directives):
        loader = Loader(DataTree(copy.deepcopy(self._minimum_required_settings)))
        try:
            loader.load(DataTree(source), directives)
        except Exception as e:
            return e
