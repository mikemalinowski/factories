from factories.examples.zoo import Zoo
from factories.examples.reader import DataReader

import os
import sys
import factories

import unittest


# ------------------------------------------------------------------------------
class FactoryTests(unittest.TestCase):
    """
    This contains a suite of tests against the main Factory object
    """

    # --------------------------------------------------------------------------
    def test_factory_is_instancable(self):
        """
        Checks to ensure we can instance a factory object
        
        :return: 
        """
        DataReader()

    # --------------------------------------------------------------------------
    def test_loading_plugins(self):
        """
        Tests that plugin paths result in the correct amount
        of plugins.
        
        :return: 
        """
        reader = DataReader()

        # -- Check we have the three available plugins
        self.assertEqual(
            2,
            len(reader.factory.plugins())
        )

    # --------------------------------------------------------------------------
    def test_accessing_identifiers(self):
        """
        Validates that we can access all the required identifiers
        
        :return: 
        """
        # -- Instance a factory
        reader = DataReader()

        # -- Ensure our available is as expected
        self.assertEqual(
            2,
            len(reader.factory.identifiers())
        )

        for identifier in reader.factory.identifiers():
            self.assertIsNotNone(
                reader.factory.request(identifier)
            )

    # --------------------------------------------------------------------------
    def test_unregister_path(self):
        """
        Tests the removal of plugin paths does indeed remove accessible
        plugins.

        :return: 
        """
        reader = DataReader()

        # -- Ensure we actually have some plugins
        self.assertGreater(
            len(reader.factory.identifiers()),
            0,
        )

        # -- Test we have one registered plugin path
        self.assertEqual(
            1,
            len(reader.factory.paths()),
        )

        # -- Remove the paths
        reader.factory.remove_path(
            reader.factory.paths()[0],
        )

        # -- Test we have no paths
        self.assertEqual(
            0,
            len(reader.factory.paths())
        )

        # -- Finally, test the available and the plugin list are
        # -- empty
        self.assertIs(
            len(reader.factory.plugins()),
            0,
        )
        self.assertIs(
            len(reader.factory.identifiers()),
            0
        )

    # --------------------------------------------------------------------------
    def test_unregister_with_multiple_paths(self):
        """
        Tests the removal of plugin paths does indeed remove accessible
        plugins.

        :return: 
        """
        reader = DataReader()

        # -- Add our path, which will
        additional_path = os.path.join(
            os.path.dirname(__file__),
            'test_plugins',
        )

        reader.factory.add_path(additional_path)

        # -- Ensure we actually have some plugins
        self.assertEqual(
            len(reader.factory.identifiers()),
            4,
        )

        # -- Test we have one registered plugin path
        self.assertEqual(
            2,
            len(reader.factory.paths()),
        )

        # -- Remove the paths
        reader.factory.remove_path(
            additional_path,
        )

        # -- Test we have no paths
        self.assertEqual(
            1,
            len(reader.factory.paths())
        )

        # -- Finally, test the available and the plugin list are
        # -- empty
        self.assertIs(
            len(reader.factory.plugins()),
            2,
        )
        self.assertIs(
            len(reader.factory.identifiers()),
            2
        )

    # --------------------------------------------------------------------------
    def test_clearing_a_factory(self):
        """
        Checks that plugins can be cleared

        :return:
        """
        reader = DataReader()

        self.assertTrue(
            len(reader.factory.plugins()) == 2
        )

        reader.factory.clear()

        self.assertTrue(
            len(reader.factory.plugins()) == 0
        )

    # --------------------------------------------------------------------------
    def test_handling_bad_python(self):
        """
        This will attempt to load a bad python file into the factory
        
        :return:
        """
        reader = DataReader()

        reader.factory.add_path(
            os.path.join(
                os.path.dirname(__file__),
                'test_plugins',
            )
        )

    # --------------------------------------------------------------------------
    def test_reloading_factory(self):
        """
        This will perform a reload of a factory ensuring that the plugin
        counts remain the same.
        
        :return: 
        """
        reader = DataReader()

        self.assertTrue(
            len(reader.factory.plugins()) == 2
        )

        reader.factory.reload()

        self.assertTrue(
            len(reader.factory.plugins()) == 2
        )

    # --------------------------------------------------------------------------
    def test_requesting_unknown_plugin(self):
        """
        Ensures the factory copes when a user requests a plugin which does 
        not exist
        
        :return: 
        """
        reader = DataReader()

        non_existant_plugin = reader.factory.request('nothing')

        self.assertIsNone(
            non_existant_plugin,
        )

    # --------------------------------------------------------------------------
    def test_getting_latest_plugin(self):
        """
        Ensures we can access plugins by version
        
        :return: 
        """
        reader = DataReader()

        # -- Add our test plugins
        reader.factory.add_path(
            os.path.join(
                os.path.dirname(__file__),
                'test_plugins',
            )
        )

        # -- Request the json reader
        json_reader = reader.factory.request('JSONReader')

        self.assertEqual(
            json_reader.version,
            2,
        )

    # --------------------------------------------------------------------------
    def test_getting_specific_plugin_version(self):
        """
        Ensures we can access plugins by version

        :return: 
        """
        reader = DataReader()

        # -- Add our test plugins
        reader.factory.add_path(
            os.path.join(
                os.path.dirname(__file__),
                'test_plugins',
            )
        )

        # -- Request the json reader
        json_reader = reader.factory.request('JSONReader')

        self.assertEqual(
            json_reader.version,
            2,
        )

        # -- Now access version 1
        old_reader = reader.factory.request(
            'JSONReader',
            version=1,
        )

        self.assertEqual(
            old_reader.version,
            1,
        )

    # --------------------------------------------------------------------------
    def test_out_of_range_version(self):
        """
        Ensures we can access plugins by version

        :return: 
        """
        reader = DataReader()

        # -- Request the json reader
        json_reader = reader.factory.request('JSONReader', version=99)

        self.assertIsNone(
            json_reader,
        )

    # --------------------------------------------------------------------------
    def test_version_request_on_non_versioned_factory(self):
        """
        When requesting a version on a non-version factory we should
        just get the highest available version
        
        :return: 
        """
        zoo = Zoo()

        # -- Request a tiger of version 2
        tiger = zoo.factory.request('tiger', version=2)

        # -- Ensure the tiger is valid
        self.assertIsNotNone(
            tiger,
        )

    # --------------------------------------------------------------------------
    def test_identifier_as_method(self):
        """
        Checks to ensure that we can correctly call an identifier when
        it is a method rather than a property
        
        :return: 
        """
        zoo = Zoo()

        # -- Add our test animals
        zoo.factory.add_path(
            os.path.join(
                os.path.dirname(__file__),
                'test_plugins',
            )
        )

        # -- Check that goat is available
        self.assertIn(
            'goat',
            zoo.factory.identifiers(),
        )

        # -- Check that we can access the plugin
        goat = zoo.factory.request('goat')

        # -- Ensure the tiger is valid
        self.assertIsNotNone(
            goat,
        )

    # --------------------------------------------------------------------------
    def test_version_as_method(self):
        """
        Checks to ensure that we can correctly call an identifier when
        it is a method rather than a property

        :return: 
        """
        reader = DataReader()

        # -- Add our test animals
        reader.factory.add_path(
            os.path.join(
                os.path.dirname(__file__),
                'test_plugins',
            )
        )

        # -- Check that goat is available
        self.assertIn(
            'MethodVersionReader',
            reader.factory.identifiers(),
        )

        plugin = reader.factory.request('MethodVersionReader', version=1)

        self.assertIsNotNone(
            plugin
        )

    # --------------------------------------------------------------------------
    def test_accessing_versions(self):
        """
        Checks to see if we can access the available versions of a plugin
        type.
        
        :return: 
        """

        reader = DataReader()

        # -- Add our test animals
        reader.factory.add_path(
            os.path.join(
                os.path.dirname(__file__),
                'test_plugins',
            )
        )

        self.assertEqual(
            reader.factory.versions('JSONReader'),
            [1, 2],
        )

    # --------------------------------------------------------------------------
    def test_accessing_versions_for_non_versioned_factory(self):
        """
        Checks to see if we can access the available versions of a plugin
        type.

        :return: 
        """
        zoo = Zoo()

        self.assertEqual(
            zoo.factory.versions('tiger'),
            [],
        )

    # --------------------------------------------------------------------------
    def test_loading_from_pyc(self):
        """
        Ensures we can load a plugin from a pyc file

        :return: 
        """
        zoo = Zoo()

        zoo.factory.add_path(
            os.path.join(
                os.path.dirname(__file__),
                'test_plugins',
            )
        )

        self.assertIsNotNone(
            zoo.factory.versions('rat'),
        )

    # --------------------------------------------------------------------------
    def test_loading_from_non_package(self):
        """
        Ensures we can load a plugin from a pyc file

        :return: 
        """
        zoo = Zoo()

        zoo.factory.add_path(
            os.path.join(
                os.path.dirname(__file__),
                'test_plugins',
            )
        )

        self.assertIsNotNone(
            zoo.factory.versions('koala'),
        )

    # --------------------------------------------------------------------------
    def test_registering_from_single_file(self):
        """
        Ensures we can load a plugin from a pyc file

        :return: 
        """
        # -- Define our non_package location
        non_package_location = os.path.join(
            os.path.dirname(__file__),
            'test_plugins',
            'non_package',
        )

        # -- Add the folder to our sys path
        sys.path.append(non_package_location)

        # -- Instance our factory
        try:
            zoo = Zoo()

            zoo.factory.add_path(
                non_package_location,
            )

            self.assertIsNotNone(
                zoo.factory.versions('koala'),
            )

        finally:

            # -- Make sure we clean up
            if non_package_location in sys.path:
                sys.path.remove(non_package_location)

    # --------------------------------------------------------------------------
    def test_direct_load_of_pyc(self):
        """
        Ensures we can load a plugin from a pyc file when registering directly

        :return: 
        """
        zoo = Zoo()

        zoo.factory.add_path(
            os.path.join(
                os.path.dirname(__file__),
                'test_plugins',
            ),
            mechanism=zoo.factory.LOAD_SOURCE,
        )

        self.assertIsNotNone(
            zoo.factory.versions('koala'),
        )


# ------------------------------------------------------------------------------
if __name__ == '__main__':
    unittest.main(verbosity=1)
