import unittest.mock as mock
import unittest

import jbs.inventory as inv

class TestModel(unittest.TestCase):
    def setUp(self):
        self.data = (
            'test_name',
            'test_set',
            'test_artist',
            'test_source',
            'test_source_note',
            True,
            'test_format',
            'test_folder',
            False
        )

        self.result = inv.Model(
            model=self.data[0],
            set=self.data[1],
            artist=self.data[2],
            source=self.data[3],
            source_note=self.data[4],
            supports=self.data[5],
            format=self.data[6],
            folder=self.data[7],
            printed=self.data[8]
            )

    def test_model_is_model(self):
        self.assertIsInstance(self.result, inv.Model)

    def test_model_name(self):
        self.assertEqual(self.result.model, 'test_name')

    def test_model_set(self):
        self.assertEqual(self.result.set, 'test_set')

    def test_model_artist(self):
        self.assertEqual(self.result.artist, 'test_artist')

    def test_model_source(self):
        self.assertEqual(self.result.source, 'test_source')

    def test_model_source_note(self):
        self.assertEqual(self.result.source_note, 'test_source_note')

    def test_model_supports(self):
        self.assertEqual(self.result.supports, True)

    def test_model_format(self):
        self.assertEqual(self.result.format, 'test_format')

    def test_model_folder(self):
        self.assertEqual(self.result.folder, 'test_folder')

    def test_model_printed(self):
        self.assertEqual(self.result.printed, False)

    def test_model_astuple_returns_tuple(self):
        self.assertIsInstance(self.result.astuple(), tuple)

    def test_model_astuple_correct(self):
        self.assertEqual(self.result.astuple(), self.data)


class TestArtist(unittest.TestCase):
    def setUp(self):
        self.data = (
            'test_name',
            'test_website',
            'test_email',
            'test_folder'
        )

        self.result = inv.Artist(
            name=self.data[0],
            website=self.data[1],
            email=self.data[2],
            folder=self.data[3]
            )

    def test_artist_is_artist(self):
        self.assertIsInstance(self.result, inv.Artist)

    def test_artist_name(self):
        self.assertEqual(self.result.name, 'test_name')

    def test_artist_website(self):
        self.assertEqual(self.result.website, 'test_website')

    def test_artist_email(self):
        self.assertEqual(self.result.email, 'test_email')

    def test_artist_folder(self):
        self.assertEqual(self.result.folder, 'test_folder')

    def test_artist_astuple_returns_tuple(self):
        self.assertIsInstance(self.result.astuple(), tuple)

    def test_artist_astuple_correct(self):
        self.assertEqual(self.result.astuple(), self.data)


class TestSource(unittest.TestCase):
    def setUp(self):
        self.data = (
            'test_name',
            'test_website'
        )

        self.result = inv.Source(
            name=self.data[0],
            website=self.data[1]
            )

    def test_source_is_source(self):
        self.assertIsInstance(self.result, inv.Source)

    def test_source_name(self):
        self.assertEqual(self.result.name, 'test_name')

    def test_source_website(self):
        self.assertEqual(self.result.website, 'test_website')

    def test_source_astuple_returns_tuple(self):
        self.assertIsInstance(self.result.astuple(), tuple)

    def test_source_astuple_correct(self):
        self.assertEqual(self.result.astuple(), self.data)


class TestFactory(unittest.TestCase):
    def setUp(self):
        self.factory = inv.ObjectFactory()

        self.model_data = (
            'test_name',
            'test_set',
            'test_artist',
            'test_source',
            'test_source_note',
            True,
            'test_format',
            'test_folder',
            False
        )

        self.artist_data = (
            'test_name',
            'test_website',
            'test_email',
            'test_folder'
        )

        self.source_data = (
            'test_name',
            'test_website'
        )

    def test_model_is_model(self):
        self.model = self.factory.createModel(self.model_data)
        self.assertIsInstance(self.model, inv.Model)

    def test_artist_is_model(self):
        self.artist = self.factory.createArtist(self.artist_data)
        self.assertIsInstance(self.artist, inv.Artist)

    def test_source_is_model(self):
        self.source = self.factory.createSource(self.source_data)
        self.assertIsInstance(self.source, inv.Source)

if __name__ == '__main__':
    unittest.main()