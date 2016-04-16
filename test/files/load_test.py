import os
import unittest
from datafaser.files import FileLoader
from datafaser.data import Data
from test.files import path_to_test_data
from datafaser.formats import FormatRegister, default_settings


class FileLoaderTest(unittest.TestCase):

    expected = {
        'yaml_files': {'a_list': ['foo', 'bar'], 'a_map': {'foo': 'bar'}},
        'json_files': {'a_list': ['foo', 'bar'], 'a_map': {'foo': 'bar'}},
        'text_files': {'a_text': 'foo is bar\n'}
    }

    def setUp(self):
        self.data = Data({})
        self.loader = FileLoader(self.data, FormatRegister(**default_settings))

    def test_loads_nothing_ok(self):
        self.loader.load([])
        self.assertEquals({}, self.data.data, 'Loader loads nothing')

    def test_loads_yaml_map_ok(self):
        self.loader.load(path_to_test_data('yaml_files', 'a_map.yaml'))
        self.assertEquals(self.expected['yaml_files']['a_map'], self.data.data, 'Loader loads contents from yaml file')

    def test_loads_yaml_ok(self):
        self.loader.load(path_to_test_data('yaml_files'))
        self.assertEquals(self.expected['yaml_files'], self.data.data, 'Loader loads yaml')

    def test_loads_json_ok(self):
        self.loader.load(path_to_test_data('json_files'))
        self.assertEquals(self.expected['json_files'], self.data.data, 'Loader loads json')

    def test_loads_text_ok(self):
        self.loader.load(path_to_test_data('text_files'))
        self.assertEquals(self.expected['text_files'], self.data.data, 'Loader loads text')

    def test_loading_without_parser_fails(self):
        exception = None
        try:
            self.loader.load(path_to_test_data('ignored_files'))
        except Exception as e:
            exception = e
        self.assertIsNotNone(exception, 'Loading with unknown extension must fail')

    def test_loads_mixed_formats_skipping_extensionless_ok(self):
        self.loader.format_register.register('datafaser.formats.ignore', None)
        self.loader.load(path_to_test_data())
        self.assertEquals(self.expected, self.data.data, 'Loader loads all supported types of data')

    def test_loads_mixed_formats_with_default_parser_ok(self):
        self.loader.default_format = 'text'
        self.loader.load(path_to_test_data())
        expected = self.expected.copy()
        expected['ignored_files'] = {'filename_without_extension': 'This file name no extension, such wild.\n'}
        self.assertEquals(expected, self.data.data, 'Loader loads all supported types of data')

    def test_load_with_absolute_path_fails(self):
        exception = None
        try:
            self.loader.load(['/test/loader/testdata/text_files'])
        except Exception as e:
            exception = e

        self.assertIsNotNone(exception, 'Loading from absolute path must fail')

    def test_load_with_backtracking_path_fails(self):
        exception = None
        try:
            self.loader.load(os.path.sep.join(['..', path_to_test_data()]))
        except Exception as e:
            exception = e

        self.assertIsNotNone(exception, 'Loading from backtracking path must fail')
