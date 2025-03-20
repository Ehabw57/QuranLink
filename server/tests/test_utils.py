import unittest
from fastapi import HTTPException
from utils.validate_range import (
    validate_page_range,
    validate_juz_range,
    validate_key_range,
    validate_range)


class Test_utils(unittest.TestCase):

    def test_validate_page_range_valid(self):
        self.assertEqual(validate_page_range(1, 604), (1, 604))

    def test_validate_page_range_invalid(self):
        with self.assertRaises(HTTPException) as ctx:
            validate_page_range(0, 605)
        self.assertEqual(ctx.exception.status_code, 400)

    def test_validate_juz_range_valid(self):
        self.assertEqual(validate_juz_range(1, 30), (1, 30))

    def test_validate_juz_range_invalid(self):
        with self.assertRaises(HTTPException) as ctx:
            validate_juz_range(0, 31)
        self.assertEqual(ctx.exception.status_code, 400)

    def test_validate_key_range_valid(self):
        self.assertEqual(validate_key_range('1:1', '1:3'), (1, 3))

    def test_validate_key_range_invalid(self):
        with self.assertRaises(HTTPException) as ctx:
            validate_key_range('999:1', '1:999')
        self.assertEqual(ctx.exception.status_code, 400)

    def test_validate_range_page_valid(self):
        self.assertEqual(validate_range('page', '1:604'), (1, 604))

    def test_validate_range_page_invalid(self):
        with self.assertRaises(HTTPException) as ctx:
            validate_range('page', '0:605')
        self.assertEqual(ctx.exception.status_code, 400)

    def test_validate_range_juz_valid(self):
        self.assertEqual(validate_range('juz', '1:30'), (1, 30))

    def test_validate_range_juz_invalid(self):
        with self.assertRaises(HTTPException) as ctx:
            validate_range('juz', '0:31')
        self.assertEqual(ctx.exception.status_code, 400)

    def test_validate_range_key_valid(self):
        self.assertEqual(validate_range('key', '1:1-1:3'), (1, 3))

    def test_validate_range_key_invalid_format(self):
        with self.assertRaises(HTTPException) as ctx:
            validate_range('key', '1:1:1:3')
        self.assertEqual(ctx.exception.status_code, 400)

    def test_validate_range_invalid_type(self):
        with self.assertRaises(HTTPException) as ctx:
            validate_range('invalid_type', '1:2')
        self.assertEqual(ctx.exception.status_code, 400)


if __name__ == "__main__":
    unittest.main()
