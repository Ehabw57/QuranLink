from pydantic import BaseModel
from typing import List


class SurahRespond(BaseModel):
    id: int
    name: str
    en_name: str
    ayahs_count: int


class VerseRespond(BaseModel):
    id: int
    surah_id: int
    number: int
    glyph_number: str
    text: List[str]
    simple_text: List[str]
    page: int
    juz: int
    rub: int


