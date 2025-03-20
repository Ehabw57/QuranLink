import unittest
from random import randint
from modules import Storage
from populat_data import populate_data

MAX_TEST_SURAHS = 5
MIN_TEST_SURAHS = 0


def setUpModule():
    populate_data(MIN_TEST_SURAHS, MAX_TEST_SURAHS)


class TestModels(unittest.TestCase):

    def test_get_surah(self):
        result = Storage.get_surah(1)
        self.assertEqual(result.en_name, 'Al-Fatihah')

    def test_get_surah_worng(self):
        result = Storage.get_surah('x')
        self.assertIsNone(result)

    def test_get_surahs(self):
        result = Storage.get_surahs()
        self.assertEqual(len(result), MAX_TEST_SURAHS - MIN_TEST_SURAHS)

    def test_get_ayah_id(self):
        chapter_id = randint(MIN_TEST_SURAHS, MAX_TEST_SURAHS)
        ayah_number = randint(1, Storage.get_surah(chapter_id).ayahs_count)
        reslut = Storage.get_ayah_id(f'{chapter_id}:{ayah_number}')
        self.assertIsNotNone(reslut)

    def test_get_ayah_id_invaild(self):
        self.assertIsNone(Storage.get_ayah_id('9999:1'))

    def test_get_ayah_by_id(self):
        self.assertIsNotNone(Storage.get_ayah_by_id(1))

    def test_get_ayah_by_id_worng(self):
        self.assertIsNone(Storage.get_ayah_by_id('string'))

    def test_get_ayahs_by_id_range(self):
        result = Storage.get_ayahs_by_id_range(1, 5)
        self.assertEqual(len(result), 5)

    def test_get_ayahs_by_page_range(self):
        result = Storage.get_ayahs_by_page_range(1, 1)
        self.assertEqual(len(result), 7)

    def test_get_ayahs_by_juz_range(self):
        self.assertEqual(len(Storage.get_ayahs_by_juz_range(1, 1)), 148)


if __name__ == "__main__":
    unittest.main()
