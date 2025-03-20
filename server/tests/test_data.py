import unittest
from random import randint
from modules import Storage
from test_1models import MAX_TEST_SURAHS, MIN_TEST_SURAHS


class TestData(unittest.TestCase):

    def test_lists_length(self):
        start_chapter = randint(MIN_TEST_SURAHS + 1, MAX_TEST_SURAHS)
        end_chapter = randint(start_chapter, MAX_TEST_SURAHS)
        start_id = Storage.get_ayah_id(f"{start_chapter}:1")
        end_id = Storage.get_ayah_id(f"{end_chapter}:2")

        verses = Storage.get_ayahs_by_id_range(start_id, end_id)
        for verse in verses:
            self.assertEqual(len(verse.simple_text), len(verse.text))
