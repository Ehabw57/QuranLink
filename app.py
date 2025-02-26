from fastapi import FastAPI
from modules import Storage
from utils.validate_range import validate_range
from data.schema import VerseRespond, SurahRespond, PageRespond
from typing import List

app = FastAPI()


@app.get("/surahs", response_model=List[SurahRespond])
def get_surahs():
    return Storage.get_surahs()


@app.get("/verses", response_model=List[VerseRespond])
def get_verses(range_type: str, range_value: str):
    start, end = validate_range(range_type, range_value)
    return Storage.retrive_range(range_type, start, end)


@app.get("/pages", response_model=List[PageRespond])
def get_pages(pages: str):
    start, end = validate_range("page", pages)
    pairs = []
    for page in range(start, end + 1):
        first_ayah_in_page = Storage.retrive_range("page", page, page)[0]
        last_ayah_in_page = Storage.get_ayah_by_id(first_ayah_in_page.id - 1)
        if last_ayah_in_page:
            pairs.append({"question": last_ayah_in_page, "answer": first_ayah_in_page})
    return pairs
