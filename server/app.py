from fastapi import FastAPI
from modules import Storage
from utils.validate_range import validate_range
from data.schema import VerseRespond, SurahRespond, PageRespond
from typing import List
from populat_data import populate_data
from fastapi.middleware.cors import CORSMiddleware

if not Storage.get_surah(1):
    populate_data()


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],
    allow_credentials=True,
)


@app.get("/surahs", response_model=List[SurahRespond])
def get_surahs():
    return Storage.get_surahs()


@app.get("/verses", response_model=List[VerseRespond])
def get_verses(range_type: str, range_value: str):
    start, end = validate_range(range_type, range_value)
    if range_type == 'page':
        return Storage.get_ayahs_by_page_range(start, end)
    if range_type == 'juz':
        return Storage.get_ayahs_by_juz_range(start, end)
    if range_type == 'key':
        return Storage.get_ayahs_by_id_range(start, end)


@app.get("/pages", response_model=List[PageRespond])
def get_pages(pages: str):
    start, end = validate_range("page", pages)
    pairs = []
    for page in range(start, end + 1):
        first_ayah_in_page = Storage.get_ayahs_by_page_range(page, page)[0]
        last_ayah_in_page = Storage.get_ayah_by_id(first_ayah_in_page.id - 1)
        if last_ayah_in_page:
            pairs.append({"question": last_ayah_in_page, "answer": first_ayah_in_page})
    return pairs
