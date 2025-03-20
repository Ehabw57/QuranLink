from modules.surahs import Surahs
from modules.ayahs import Ayahs
from modules import Storage
import json
import gzip


def populate_data(min=0, max=114):
    with gzip.open('data/hafsChapters_v3-0.json.gz', 'rt') as C:
        surahs = json.load(C)

    for s in surahs[min:max]:
        Storage.new(Surahs(
                name=s['name'].encode('utf-8'),
                en_name=s['en_name'],
                ayahs_count=s['ayahs_count']))
    Storage.save()

    with gzip.open('data/hafsVerses_v3.0.json.gz', 'rt') as V:
        ayahs = json.load(V)

    for a in ayahs:
        Storage.new(Ayahs(
                surah_id=a['surah_id'],
                number=a['number'],
                glyph_number=a['glyph_no'].encode('utf-8'),
                text=a['text'],
                simple_text=a['simple_text'],
                page=a['page'],
                juz=a['juz']))
        print(f"Populated: Verse ({a['number']}) of Chapter ({surahs[a['surah_id'] - 1 ]['en_name']})")
    Storage.save()

    Storage.close


if __name__ == "__main__":
    populate_data()
